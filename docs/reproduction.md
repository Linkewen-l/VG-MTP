# Statistical reproduction

## Inputs and outputs

| Analysis | Input | Output under `results/recomputed_local/` |
|---|---|---|
| Primary EDS and seed variation | `results/main/paired_task_seed.csv`, `baseline_results.csv`, main task manifest | `main_eds.csv`, `main_by_seed.csv`, `main_raw_aggregation.csv` |
| Paired comparisons and grouping sensitivity | The same matched task keys and source groups | `main_comparisons.csv`, `main_four_way.csv` |
| Mandatory-binding ablation | `results/reporting_ablation/paired_task_seed.csv` | `reporting_ablation.json` |
| SQV workflows and diagnosis | `results/sqv/paired_results.csv`, SQV manifest | `sqv.json`, `sqv_by_seed.csv` |
| HB target-prior withholding | `results/hb/target_prior_withheld.csv` | `hb_prior_withheld.json` |
| Training-source and corpus checks | `provenance/`, `training/` | `training_provenance.json`, `training_strata.csv`, `corpus_summary.csv` |
| Registered count arithmetic | Terminal summaries, expert cross-counts and manuscript call counts | `terminal_arithmetic.csv`, `expert_claim_arithmetic.csv`, `checks.csv` |

Paths in the input column are relative to the repository root; output paths are chosen by `--output`.

## Aggregation

Join primary outcomes on `(task_id, training_seed)`. A strict majority requires five successes among nine planned runs for sealed tasks, or four among six for HB tasks. Ties and failures are retained. Average equally over the 240 tasks and five training seeds. Fixed Unadapted and Dynamic-rule outcomes retain S = 1 when paired with sampled training seeds.

The task-equal raw EDS and the pooled raw success fraction have distinct weights. The script exports both. For SQV, 420 paired rows describe 840 executions. Macro-F1 is calculated over the fixed normal, inner-race and outer-race classes within each seed and then averaged across seeds.

## Bootstrap settings

Use 10,000 replicates, NumPy PCG64 seed 20261013 and linear 2.5th/97.5th percentiles. The primary analysis draws four KAIST, six Paderborn and five HB groups within their sources and retains all tasks within sampled groups. Source weights remain 112/240, 68/240 and 60/240. Five training seeds are resampled, with identical draws for paired methods.

Generate the entire seed-index array first, then group arrays in KAIST, Paderborn and HB order using sorted group labels. The eight-group sensitivity analysis restarts the generator, samples five seeds and eight pooled groups, and uses the sampled task-weighted mean. Its source composition can vary.

SQV samples seven state groups and five seeds per replicate, in that order, retaining both phases and workflows and all six records per group. Compute phase gains and their interaction before percentiles. The HB comparison draws 20 health-state × speed-setting groups and five seeds, retaining all three trials.

## Run and compare

```bash
python -m pip install -r analysis/requirements.txt
python analysis/recompute.py --output results/recomputed_local
```

The recorded statistical run uses Python 3.12.14 and NumPy 2.3.5. The experiment's training environment is separately recorded in `environment/manuscript_environment.json`.

The script verifies input keys, counts, paired outcomes, selection totals and published rounded values. The reference `validation.json` contains 112 matched checks and the SHA-256 of each statistical input. Output floats retain full precision; round only for presentation. Four-way main counts are 869/25/4/302; full/no-binding counts are 826/68/0/306.

The scan in `model_visible_scope.json` records the exact literal patterns checked within corpus content. Registered source joins, field visibility and numerical result checks are reported as separate operations.
