# 字段与计数口径

CSV为UTF-8（带BOM），每张数据表第一行是列名。JSON/JSONL为UTF-8。空白表示未提供或不适用，不表示0。百分比字段以`_pct`结尾时取0–100；`_pp`表示百分点；`*_eds`、`*_majority`、`included`为0/1。源文件中的原比例字段（例如`macro_f1`）取0–1。

| 文件 | 一行的单位与唯一键 | 核心字段 |
|---|---|---|
| `manifests/main_eval_tasks.csv` | 基础任务；task_id | source_group为15组主统计分组；file_group_as_registered保留源表文件组，两者不可混同。窗口为半开区间，单位秒。 |
| `results/main/paired_task_seed.csv` | 任务×训练种子；task_id + training_seed | planned_runs包含失败/超时；VG和LLM原始成功数分别保留；strict majority为成功数>计划数/2，平票失败。日志字段是定位字符串。 |
| `results/main/baseline_results.csv` | 方法×任务×种子 | Unadapted/Dynamic-rule种子留空表示固定S=1，不能复制后计成五次独立评测。 |
| `results/reporting_ablation/paired_task_seed.csv` | 任务×训练种子 | difference_full_minus_no_binding为完整减无强制引用；论文 B.10 与复算输出统一采用完整减无强制引用。多数结果由原始计数计算，不依赖Excel公式缓存。 |
| `manifests/sqv_records_windows.csv` | 候选记录；record_id | 52行全部保留；included=1为42条；稳速/降速各2秒；排除说明保留。 |
| `results/sqv/paired_results.csv` | 一个任务×种子的两流程结果 | 420行是840次执行；full_prediction是实际登记预测，不能从EDS反推；Macro-F1按每种子先算再平均。 |
| `results/terminal/registered_summary.csv` | 每方法已登记的汇总计数 | 诊断正确率除以answer_required_n；覆盖率除以task_seed_results；危险接受除以abstention_required_n。不等同于逐任务终态。 |
| `provenance/candidate_lineage.csv` | 候选；candidate_id | task_id连接训练输入；dataset、record_key表示实际来源；stratum/substratum及quota_label_registered表示配额模板。保留原v104字段，不用它定义论文配置。 |
| `provenance/task_inputs.csv` | 任务的一种输入用途；task_id + input_role | 振动与转速/派生输入分别登记；physical_file是可移植标识；physical_file_sha256来自S09物理文件登记。 |
| `provenance/corpus_sample_map.csv` | 语料样本在一个epoch中的实例；corpus_file + epoch + sample_id | corpus_line为实际JSONL一基行号；parent_candidate_id和parent_task_id连回来源链；token_count是登记的样本token数。 |
| `paper_map.csv` | 论文或仓库中的结果位置 | result_files 为包内路径；reproduction_entry 为复算入口；scope 说明指标和计算单位。 |
| `manifests/source_exports.csv` | 一个选取或复制的文件 | source_id、source_locator定位源材料；evidence_level区分原始提供文件、计数、汇总和论文快照；sha256校验导出文件。 |

`source_row`是原工作表的一基行号，不是CSV中的数据行号。`source_id`通过`sources.csv`查原文件名与身份哈希；私人绝对路径保留在包外。

主评测74.50%为多数EDS，74.25%为任务等权原始EDS，7,188/9,900为直接合并原始EDS。它们采用不同聚合规则。Pass³=2,026/3,300=61.39%作为已确认的实际结果登记；脚本按登记的实际成功组数与分母核算该比例。

所有列的文件、名称与推断存储类型见 `manifests/column_dictionary.csv`。论文快照中保留展示字符串和原列名，不将区间、N/A或组合计数强行转换为数值。
