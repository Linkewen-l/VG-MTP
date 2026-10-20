# Original signals and file selection

Obtain signals from the data providers cited in the manuscript and select records with the accompanying manifests.

| Source | Provider | Selection |
|---|---|---|
| KAIST | Mendeley Data identifiers `vxkj334rzv`, `x3vhp8t6hg`, `j8d8pfkvj2`, version 7 | `manifests/main_eval_tasks.csv`, Table S1 |
| Paderborn | [Bearing DataCenter](https://mb.uni-paderborn.de/en/kat/research/bearing-datacenter) | Main task manifest, training input register, Table S6 |
| HUST | Mendeley Data identifier `cbv7jyx4p9`, version 3 | `provenance/task_inputs.csv` |
| Huang–Baddour | Mendeley Data identifier `v43hmbwxpm`, version 2 | HB entries of the main task manifest |
| SQV | [SQ dataset with variable speed](https://github.com/shenliuuu/SQ-dataset-with-variable-speed-for-fault-diagnosis) | `manifests/sqv_records_windows.csv`, Tables S4 and S5 |

The signal-selection identifiers are portable paths. `manifests/physical_file_hashes.csv` records the 168 training-input file hashes. `checksums.sha256` identifies the files distributed in this reproducibility package. These inventories have different verification targets.

Statistical reproduction uses the included outcomes and corpus records through `analysis/recompute.py`.
