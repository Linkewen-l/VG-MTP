"""Recompute paired outcomes, registered counts and training-source joins.

Usage: python analysis/recompute.py [--root PATH] [--output PATH]
Requires NumPy. All CSV inputs use UTF-8 (an optional BOM is accepted).
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import csv
import hashlib
import json
import platform
import re
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
parser.add_argument("--output",type=Path)
args=parser.parse_args()
root=args.root.resolve()
out=(args.output or root/"results/recomputed").resolve()
out.mkdir(parents=True,exist_ok=True)
config=json.loads((root/"configs/statistics.json").read_text(encoding="utf-8"))
SEEDS=config["training_seeds"]
N=config["replicates"]
checks=[]
inputs_used={}

def rows(rel):
    path=root/rel
    inputs_used[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def write(name,data):
    (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")

def writecsv(name,data):
    if not data:return
    with (out/name).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)

def check(table,metric,actual,expected,tolerance=0,level="from_exported_records"):
    if isinstance(actual,(float,int)) and isinstance(expected,(float,int)):
        good=abs(actual-expected)<=tolerance
    else:good=actual==expected
    checks.append(dict(paper_table=table,metric=metric,actual=actual,expected=expected,tolerance=tolerance,
                       status="matched" if good else "mismatch",evidence_level=level))
    return good

def ci(x):
    return np.quantile(x,[.025,.975],method=config["percentile_method"]).tolist()

def integer(row,field):return int(row[field])

main=rows("results/main/paired_task_seed.csv")
task_manifest=rows("manifests/main_eval_tasks.csv")
baseline=rows("results/main/baseline_results.csv")
task_ids=sorted(r["task_id"] for r in task_manifest)
task_index={t:i for i,t in enumerate(task_ids)}
task_info={r["task_id"]:r for r in task_manifest}
keys={(r["task_id"],int(r["training_seed"])) for r in main}
assert len(task_ids)==len(task_index)==240
assert len(main)==len(keys)==1200
assert keys=={(t,s) for t in task_ids for s in SEEDS}
methods=["VG-MTP","LLM-process-full","D-only-full","Final-label-only","Unadapted","Dynamic-rule"]
a=np.full((240,5,len(methods)),np.nan)
for r in main:
    i=task_index[r["task_id"]];j=SEEDS.index(int(r["training_seed"]))
    n=integer(r,"planned_runs")
    assert n==integer(r,"vg_completed")==integer(r,"llm_completed")
    for prefix,method_index in [("vg",0),("llm",1)]:
        k=integer(r,prefix+"_raw_success")
        assert 0<=k<=n
        assert integer(r,prefix+"_majority")==int(2*k>n)
        a[i,j,method_index]=int(2*k>n)
base_keys=set()
for r in baseline:
    key=(r["task_id"],r["method"],r["training_seed"])
    assert key not in base_keys
    base_keys.add(key)
    i=task_index[r["task_id"]];k=methods.index(r["method"]);v=integer(r,"majority_eds")
    assert v in [0,1]
    if r["training_seed"]:
        a[i,SEEDS.index(int(r["training_seed"])),k]=v
    else:
        # Fixed S=1 comparator reused over sampled training seeds. No extra executions are created.
        a[i,:,k]=v
assert np.isfinite(a).all()

def main_bootstrap(values,coarse=False):
    """Shared task/source and seed draws; values shape=(240,5,M)."""
    rng=np.random.Generator(np.random.PCG64(config["random_seed"]))
    seed_draws=rng.integers(0,5,(N,5))
    boot=np.zeros((N,values.shape[-1]))
    source_slices=[("all",1.0)] if coarse else [("KAIST",112/240),("Paderborn",68/240),("HB",60/240)]
    for source,weight in source_slices:
        labels={t:(task_info[t]["source"] if coarse and task_info[t]["source"]!="Paderborn"
                   else task_info[t]["source_group"]) for t in task_ids}
        groups=sorted({labels[t] for t in task_ids if source=="all" or task_info[t]["source"]==source})
        members=[[task_index[t] for t in task_ids if labels[t]==g] for g in groups]
        sizes=np.array([len(m) for m in members])
        sums=np.stack([values[m].sum(axis=0) for m in members])
        draws=rng.integers(0,len(groups),(N,len(groups)))
        sampled=sums[draws].sum(axis=1)/sizes[draws].sum(axis=1)[:,None,None]
        boot+=weight*sampled[np.arange(N)[:,None],seed_draws].mean(axis=1)
    return boot*100

b15=main_bootstrap(a)
b8=main_bootstrap(a,True)
summary=[]
expected_success=[894,873,828,785,136,163]
for k,method in enumerate(methods):
    success=int(a[:,:,k].sum()) if k<4 else int(a[:,0,k].sum())
    den=1200 if k<4 else 240
    summary.append(dict(method=method,successes=success,denominator=den,eds_pct=100*success/den,
                        ci15_low_pct=ci(b15[:,k])[0],ci15_high_pct=ci(b15[:,k])[1],
                        comparator_seed_scope="five training seeds" if k<4 else "fixed S=1"))
    check("4-2;S2",method+" majority successes",success,expected_success[k])
check("4-1;S7","main tasks",len(task_ids),240)
for source,n,groups in [("KAIST",112,4),("Paderborn",68,6),("HB",60,5)]:
    selected=[r for r in task_manifest if r["source"]==source]
    check("4-1;S7",source+" task count",len(selected),n)
    check("S7",source+" source groups",len({r["source_group"] for r in selected}),groups)
pairs=[]
expected_ci15=[[15.26,20.06],[6.72,11.43],[3.78,6.92],[1.00,2.50],[4.50,8.45],[1.75,5.40]]
expected_ci8=[[-14.26,27.56],[-23.72,20.92],[-28.22,18.33],[.63,3.19],[-28.44,18.83],[-30.00,17.11]]
for idx,(i,j) in enumerate([(0,4),(0,3),(0,2),(0,1),(0,5),(1,2)]):
    c15=ci(b15[:,i]-b15[:,j]);c8=ci(b8[:,i]-b8[:,j])
    pairs.append(dict(comparison=methods[i]+" minus "+methods[j],difference_pp=float((a[:,:,i]-a[:,:,j]).mean()*100),
                      ci15_low_pp=c15[0],ci15_high_pp=c15[1],ci8_low_pp=c8[0],ci8_high_pp=c8[1]))
    for k,side in enumerate(["low","high"]):
        check("B5",pairs[-1]["comparison"]+" primary "+side,c15[k],expected_ci15[idx][k],.0051)
        check("B5",pairs[-1]["comparison"]+" sensitivity "+side,c8[k],expected_ci8[idx][k],.0051)
seed_summary=[]
four_way=[]
for j,s in enumerate(SEEDS):
    for k,m in enumerate(methods[:4]):
        seed_summary.append(dict(training_seed=s,method=m,successes=int(a[:,j,k].sum()),tasks=240,eds_pct=float(a[:,j,k].mean()*100)))
    counts=Counter((int(x),int(y)) for x,y in a[:,j,:2])
    four_way.append(dict(training_seed=s,both_pass=counts[1,1],vg_only=counts[1,0],llm_only=counts[0,1],both_fail=counts[0,0]))
paper_b6=rows("docs/supplementary_tables/table_S2.csv")
for r in seed_summary:
    pr=next(p for p in paper_b6 if p["Training seed"]==str(r["training_seed"]))
    check("S2",f"{r['method']} seed {r['training_seed']}",r["eds_pct"],float(pr[r["method"]]),.0051)
counts=Counter((int(x),int(y)) for x,y in a[:,:,:2].reshape(-1,2))
for key,expected in [((1,1),869),((1,0),25),((0,1),4),((0,0),302)]:
    check("S11","paired "+str(key),counts[key],expected)
raw=[]
for prefix,method in [("vg","VG-MTP"),("llm","LLM-process-full")]:
    n=sum(integer(r,"planned_runs") for r in main)
    success=sum(integer(r,prefix+"_raw_success") for r in main)
    task_equal=100*np.mean([integer(r,prefix+"_raw_success")/integer(r,"planned_runs") for r in main])
    raw.append(dict(method=method,planned_runs=n,raw_success=success,pooled_eds_pct=100*success/n,task_equal_raw_eds_pct=float(task_equal)))
check("A.2","VG pooled raw count",raw[0]["raw_success"],7188)
check("A.2","VG planned executions",raw[0]["planned_runs"],9900)
check("A.2","VG task-equal raw EDS",raw[0]["task_equal_raw_eds_pct"],74.25,1e-9)
writecsv("main_eds.csv",summary);writecsv("main_comparisons.csv",pairs)
writecsv("main_by_seed.csv",seed_summary);writecsv("main_four_way.csv",four_way);writecsv("main_raw_aggregation.csv",raw)

abl=rows("results/reporting_ablation/paired_task_seed.csv")
assert {(r["task_id"],integer(r,"training_seed")) for r in abl}==keys and len(abl)==1200
ab=np.zeros((240,5,2))
for r in abl:
    i=task_index[r["task_id"]];j=SEEDS.index(integer(r,"training_seed"));n=integer(r,"planned_runs")
    for k,prefix in enumerate(["full","no_binding"]):
        assert integer(r,prefix+"_completed")==n
        value=int(2*integer(r,prefix+"_raw_success")>n)
        assert value==integer(r,prefix+"_majority")
        ab[i,j,k]=value
assert np.array_equal(ab[:,:,0],a[:,:,0])
abc=Counter((int(x),int(y)) for x,y in ab.reshape(-1,2))
abb=main_bootstrap(ab);abci=ci(abb[:,0]-abb[:,1])
ab_result=dict(pairs=len(abl),full_success=int(ab[:,:,0].sum()),no_binding_success=int(ab[:,:,1].sum()),
    difference_full_minus_no_binding_pp=float((ab[:,:,0]-ab[:,:,1]).mean()*100),ci95_full_minus_no_binding_pp=abci,
    ci95_no_binding_minus_full_pp=[-abci[1],-abci[0]],four_way={str(k):v for k,v in sorted(abc.items())})
check("4-12;4-12","no-binding successes",ab_result["no_binding_success"],826)
check("4-12","no-binding paired counts",[abc[1,1],abc[1,0],abc[0,1],abc[0,0]],[826,68,0,306])
check("4.4.1","full minus no-binding CI low",abci[0],4.55,.0051)
check("4.4.1","full minus no-binding CI high",abci[1],6.61,.0051)
write("reporting_ablation.json",ab_result)

records=rows("manifests/sqv_records_windows.csv")
sqv=rows("results/sqv/paired_results.csv")
included={r["record_id"]:r for r in records if r["included"]=="1"}
groups=sorted({r["source_group"] for r in included.values()})
record_order={g:sorted(r["record_id"] for r in included.values() if r["source_group"]==g) for g in groups}
assert len(groups)==7 and all(len(x)==6 for x in record_order.values())
q=np.full((7,6,2,5,2),np.nan)
sqv_keys=set()
for r in sqv:
    key=(r["task_id"],r["training_seed"]);assert key not in sqv_keys;sqv_keys.add(key)
    g=groups.index(r["source_group"]);rec=record_order[r["source_group"]].index(r["record_id"])
    p=0 if r["phase"]=="steady" else 1;s=SEEDS.index(integer(r,"training_seed"))
    q[g,rec,p,s,:]=[integer(r,"full_eds"),integer(r,"alternative_eds")]
assert np.isfinite(q).all() and np.isin(q,[0,1]).all()
phase_means=q.mean(axis=(0,1,3))*100
rng=np.random.Generator(np.random.PCG64(config["random_seed"]))
qboot=np.zeros((N,2,2))
for k in range(N):
    gd=rng.integers(0,7,7);sd=rng.integers(0,5,5)
    qboot[k]=q[gd][:,:,:,sd,:].mean(axis=(0,1,3))*100
gains=qboot[:,:,0]-qboot[:,:,1]
interaction_ci=ci(gains[:,1]-gains[:,0])
sqv_seed=[]
def macro_f1(rs):
    classes=sorted({r["reference_class"] for r in rs})
    f1=[]
    for c in classes:
        tp=sum(r["reference_class"]==c and r["full_prediction"]==c for r in rs)
        fp=sum(r["reference_class"]!=c and r["full_prediction"]==c for r in rs)
        fn=sum(r["reference_class"]==c and r["full_prediction"]!=c for r in rs)
        f1.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0)
    return 100*np.mean(f1)
for i,s in enumerate(SEEDS):
    v=q[:,:,:,i,:].mean(axis=(0,1))*100
    sqv_seed.append(dict(training_seed=s,steady_full_pct=v[0,0],steady_alt_pct=v[0,1],
                         decel_full_pct=v[1,0],decel_alt_pct=v[1,1],
                         interaction_pp=(v[1,0]-v[1,1])-(v[0,0]-v[0,1]),
                         macro_f1_pct=macro_f1([r for r in sqv if integer(r,"training_seed")==s])))
sqv_result=dict(candidate_records=len(records),included_records=len(included),tasks=len(sqv_keys)//5,
    paired_rows=len(sqv),total_executions=len(sqv)*2,full_success=int(q[:,:,:,:,0].sum()),
    alternative_success=int(q[:,:,:,:,1].sum()),full_eds_pct=float(q[:,:,:,:,0].mean()*100),
    steady_full_success=int(q[:,:,0,:,0].sum()),decel_full_success=int(q[:,:,1,:,0].sum()),
    steady_gain_pp=float(phase_means[0,0]-phase_means[0,1]),decel_gain_pp=float(phase_means[1,0]-phase_means[1,1]),
    steady_ci95_pp=ci(gains[:,0]),decel_ci95_pp=ci(gains[:,1]),interaction_ci95_pp=interaction_ci,
    interaction_pp=float((phase_means[1,0]-phase_means[1,1])-(phase_means[0,0]-phase_means[0,1])),
    macro_f1_seed_mean_pct=float(np.mean([r["macro_f1_pct"] for r in sqv_seed])),
    macro_f1_pooled_pct=float(macro_f1(sqv)))
for field,expected in [("candidate_records",52),("included_records",42),("tasks",84),("total_executions",840),
                       ("full_success",378),("alternative_success",354),("steady_full_success",191),("decel_full_success",187)]:
    check("4-9;4-18;S3;S4",field,sqv_result[field],expected)
check("4-9","SQV interaction CI low",interaction_ci[0],5.24,.0051)
check("4-9","SQV interaction CI high",interaction_ci[1],14.29,.0051)
check("4-18","SQV Macro-F1 seed mean",sqv_result["macro_f1_seed_mean_pct"],93.08,.0051)
for r in included.values():
    assert abs(float(r["steady_end_s"])-float(r["steady_start_s"])-2)<1e-9
    assert abs(float(r["decel_end_s"])-float(r["decel_start_s"])-2)<1e-9
write("sqv.json",sqv_result);writecsv("sqv_by_seed.csv",sqv_seed)

term=rows("results/terminal/registered_summary.csv")
terminal=[]
for r in term:
    terminal.append(dict(method=r["method"],diagnosis_accuracy_pct=100*integer(r,"diagnosis_correct_n")/integer(r,"answer_required_n"),
                         macro_f1_pct=100*float(r["macro_f1"]),coverage_pct=100*integer(r,"accepted_n")/integer(r,"task_seed_results"),
                         unsafe_acceptance_pct=100*integer(r,"unsafe_accept_n")/integer(r,"abstention_required_n"),
                         evidence_level="arithmetic_from_registered_aggregate_counts"))
vg=next(r for r in terminal if r["method"]=="VG-MTP")
for field,expected in [("diagnosis_accuracy_pct",80.72),("macro_f1_pct",78.15),("coverage_pct",89.00),("unsafe_acceptance_pct",13.33)]:
    check("4-7",field,vg[field],expected,.0051,"registered_aggregate_arithmetic")
writecsv("terminal_arithmetic.csv",terminal)
hb=rows("results/hb/target_prior_withheld.csv")
hb_ids=sorted({r["task_id"] for r in hb})
hb_groups=sorted({r["setting_group"] for r in hb})
hvg={(r["task_id"],integer(r,"training_seed")):integer(r,"majority_eds") for r in hb if r["condition_id"]=="HB415_VG"}
hu={r["task_id"]:integer(r,"majority_eds") for r in hb if r["condition_id"]=="HB415_U"}
hb_d=np.array([[[hvg[t,s]-hu[t] for s in SEEDS] for t in hb_ids if "-".join(t.split("-")[:-1])==g] for g in hb_groups])
assert hb_d.shape==(20,3,5)
rng=np.random.Generator(np.random.PCG64(config["random_seed"]));hboot=[]
for _ in range(N):
    gd=rng.integers(0,20,20);sd=rng.integers(0,5,5)
    hboot.append(float(hb_d[gd][:,:,sd].mean()*100))
hb_result=dict(vg_success=sum(hvg.values()),vg_denominator=len(hvg),unadapted_success=sum(hu.values()),
               unadapted_denominator=len(hu),difference_pp=float(hb_d.mean()*100),ci95_pp=ci(hboot))
check("4-16","HB VG successes",hb_result["vg_success"],210)
check("4-16","HB Unadapted successes",hb_result["unadapted_success"],29)
write("hb_prior_withheld.json",hb_result)

# Provenance joins and corpus checks are checked from the supplied data, not reconstructed.
lineage=rows("provenance/candidate_lineage.csv")
task_inputs=rows("provenance/task_inputs.csv")
samples=rows("provenance/corpus_sample_map.csv")
candidates={r["candidate_id"]:r for r in lineage}
train_tasks={r["task_id"] for r in task_inputs}
assert len(candidates)==len(lineage)==1280
assert {r["task_id"] for r in lineage}==train_tasks
assert all(r["partition"]=="Train" for r in task_inputs)
assert all(len(r["physical_file_sha256"])==64 for r in task_inputs)
for r in samples:
    parent=candidates[r["parent_candidate_id"]]
    assert r["parent_task_id"]==parent["task_id"]
corpus_stats=[]
visible_counts=Counter()
visible_patterns={
    "HB_or_KAIST":r"\b(?:HB|KAIST)\b",
    "quota_field_name":r'"(?:stratum|substratum|source_group|s2_label)"\s*:',
    "specified_dev_test_bearing_id":r"(?<![A-Za-z0-9])(?:K00[1-6]|KA16|KA22|KA30|KI01|KI03|KI04|KI05|KI07|KI08|KI14|KI16|KI17|KI18|KI21)(?![A-Za-z0-9])",
}
grouped=defaultdict(list)
for r in samples:grouped[r["corpus_file"]].append(r)
assert len(grouped)==20
for file,ms in sorted(grouped.items()):
    path=root/"training/sft_corpus"/file
    inputs_used[path.relative_to(root).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    index={int(r["corpus_line"]):r for r in ms}
    parents=set();epochs=Counter();tokens=0
    with path.open(encoding="utf-8-sig") as f:
        for i,line in enumerate(f,1):
            record=json.loads(line);m=index[i]
            assert record["sample_id"]==m["sample_id"] and str(record["epoch"])==m["epoch"]
            assert record["parent_candidate_id"]==m["parent_candidate_id"]
            assert record["parent_trajectory_id"]==m["parent_trajectory_id"]
            content=record["content"]
            text=json.dumps(content,ensure_ascii=False)
            visible_counts["records_checked"]+=1
            for label,pattern in visible_patterns.items():
                visible_counts[label]+=bool(re.search(pattern,text))
            instruction=str(content.get("instruction",""))
            visible_counts["registered_record_key_in_instruction"]+=candidates[record["parent_candidate_id"]]["record_key"] in instruction
            visible_counts["task_id_in_instruction"]+=record["parent_task_id"] in instruction
            visible_counts["terminal_field_absent"]+=("terminal" not in content and "terminal_report" not in content and "response" not in content)
            parents.add(record["parent_candidate_id"]);epochs[record["epoch"]]+=1;tokens+=record["token_count"]
    assert i==3072==len(ms) and len(parents)==1024 and epochs=={1:1024,2:1024,3:1024}
    corpus_stats.append(dict(corpus_file=file,instances=i,distinct_parents=len(parents),epochs=len(epochs),nominal_token_total=tokens))
traj={}
for path in sorted((root/"training/trajectories").glob("*.jsonl")):
    with path.open(encoding="utf-8-sig") as f:
        for i,line in enumerate(f,1):
            r=json.loads(line)
            assert r["candidate_id"] not in traj
            parent=candidates[r["candidate_id"]]
            assert r["task_id"]==parent["task_id"] and r["record_key"]==parent["record_key"]
            traj[r["candidate_id"]]=r["trajectory_id"]
assert set(traj)==set(candidates)
for r in samples:assert r["parent_trajectory_id"]==traj[r["parent_candidate_id"]]
screen={}
for file in ["d_screen.jsonl","llm_panel.jsonl","vg_screen.jsonl"]:
    with (root/"training/screening"/file).open(encoding="utf-8-sig") as f:
        data=[json.loads(l) for l in f]
    expected_keys=set(candidates) if file=="d_screen.jsonl" else {
        r["candidate_id"] for r in screen["d_screen.jsonl"] if r["decision"]=="d_pass"}
    assert {r["candidate_id"] for r in data}==expected_keys and len(data)==len(expected_keys)
    screen[file]=data
screen_counts=dict(d_pass=sum(r["decision"]=="d_pass" for r in screen["d_screen.jsonl"]),
                   llm_eligible=sum(r["decision"]=="eligible" for r in screen["llm_panel.jsonl"]),
                   vg_eligible=sum(bool(r["v200_pass"]) for r in screen["vg_screen.jsonl"]))
provenance=dict(candidates=len(lineage),tasks=len(train_tasks),input_entries=len(task_inputs),
                recording_keys=len({r["record_key"] for r in task_inputs}),
                physical_files=len({r["physical_file"] for r in task_inputs}),corpora=len(grouped),
                corpus_mappings=len(samples),complete_trajectories=len(traj),screening=screen_counts,
                registered_datasets=dict(Counter(r["record_key"].split("/")[0] for r in {r["record_key"]:r for r in task_inputs}.values())),
                scope="Registered candidate, task, input and corpus joins; file identities and selection counts.")
for field,value in [("candidates",1280),("tasks",252),("input_entries",504),("recording_keys",168),("corpora",20),("corpus_mappings",61440)]:
    check("B.9;S8",field,provenance[field],value)
for field,value in [("d_pass",1096),("llm_eligible",1063),("vg_eligible",1030)]:
    check("B6",field,screen_counts[field],value)
strata=[]
for s in ["A","B","C"]:
    rs=[r for r in lineage if r["stratum"]==s]
    strata.append(dict(stratum=s,candidates=len(rs),tasks=len({r["task_id"] for r in rs}),
                        records=len({r["record_key"] for r in rs}),selected=sum(int(r["selected"]) for r in rs)))
for r,expected in zip(strata,[[598,120,84,478],[320,64,33,256],[362,68,51,290]]):
    for name,value in zip(["candidates","tasks","records","selected"],expected):
        check("S8",r["stratum"]+" "+name,r[name],value)
write("training_provenance.json",provenance);writecsv("corpus_summary.csv",corpus_stats);writecsv("training_strata.csv",strata)
write("model_visible_scope.json",dict(counts=dict(visible_counts),searched_patterns=visible_patterns,
    inspected_object="content only; sample metadata outside content is excluded",
    scope="Limited literal-field scan. Record keys and task IDs remain visible. A missing terminal field is structural absence, not evidence of a conflicting terminal label. This scan does not exclude every possible shortcut or cue."))

expert=rows("audits/expert/claim_cross_counts.csv")
expert_summary=[]
for r in expert:
    aa,ab,ba,bb=[int(r[c]) for c in ["自动1／专家1","自动1／专家0","自动0／专家1","自动0／专家0"]]
    n=aa+ab+ba+bb
    expert_summary.append(dict(condition=r["报告条件"],claims=n,automated_ucr_pct=100*(aa+ab)/n,
                               expert_ucr_pct=100*(aa+ba)/n,agreement_pct=100*(aa+bb)/n,
                               recall_pct=100*aa/(aa+ba),precision_pct=100*aa/(aa+ab)))
for r,expected in zip(expert_summary,[97.05,97.62,98.57]):
    check("4-13",r["condition"]+" agreement",r["agreement_pct"],expected,.0051,"aggregate_cross_counts")
writecsv("expert_claim_arithmetic.csv",expert_summary)
pass3=rows("results/main/pass3_registered.csv")[0]
check("4-3;A.2","registered actual Pass3 arithmetic",100*int(pass3["all_three_success"])/int(pass3["prompt_episode_triplets"]),
      61.39,.0051,"registered_actual_count_arithmetic")
c6=rows("docs/paper_tables/table_C4.csv")
counts={r["统计量"]:float(r["精确计数"].replace(",","").rstrip("%")) for r in c6}
check("C4","proposed equals dispatched + blocked + undecided",counts["实际派发／适用分母"]+counts["阻断 CALL"]+counts["未完成派发判定"],
      counts["提出 CALL"],level="manuscript_summary_arithmetic")
check("C4;4-3","dispatch mean",counts["实际派发／适用分母"]/counts["原始运行"],6.49,.0051,"manuscript_summary_arithmetic")

writecsv("checks.csv",checks)
result=dict(passed=sum(r["status"]=="matched" for r in checks),mismatches=[r for r in checks if r["status"]!="matched"],
    python=platform.python_version(),numpy=np.__version__,rng=config,input_sha256=inputs_used,
    scope="Paired outcome aggregation and bootstrap intervals; training-source joins and corpus counts; arithmetic from registered terminal, expert and call summaries.")
write("validation.json",result)
print(json.dumps({"checks_matched":result["passed"],"mismatches":result["mismatches"],
                  "main_vg_eds":summary[0]["eds_pct"],"ablation":ab_result,"sqv":sqv_result,
                  "provenance":provenance},ensure_ascii=False,indent=2))
if result["mismatches"]:raise SystemExit(1)
