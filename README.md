# VG-MTP reproducibility materials

Materials accompanying **VG-MTP: Verifier-Guided Mechanism-Aware Tool Planning for Evidence-Grounded Rotating-Machinery Fault Diagnosis**.

This repository provides paired evaluation outcomes, exact task and window manifests, training trajectories and corpus provenance, experimental specifications, and scripts that reproduce the statistical results below.

| Analysis | Data | Recomputed result |
|---|---|---|
| Main matched comparison | 240 tasks and 5 training seeds; 1,200 paired outcomes | VG-MTP 74.50%; LLM-process-full 72.75%; gain 1.75 pp, 95% interval [1.00, 2.50] |
| Reporting ablation | 1,200 full/no-binding pairs | No-binding 68.83%; full-minus-no-binding gain 5.67 pp, [4.55, 6.61] |
| SQV evaluation | 42 recordings, 84 tasks and 840 workflow executions | Full EDS 90.00%; seed-mean Macro-F1 93.08%; phase interaction 9.52 pp, [5.24, 14.29] |
| Training provenance | 1,280 candidates, 252 tasks, 168 records and 20 corpora | 99 HUST and 69 Paderborn records; 61,440 corpus-instance mappings |

[中文阅读说明](README_CN.md) · [Paper-to-file index](paper_map.csv) · [Statistical guide](docs/reproduction.md) · [Supplementary Tables S1–S11](docs/supplementary_tables/README.md)

## Recompute the results

Run from the repository root:

```bash
python -m pip install -r analysis/requirements.txt
python analysis/recompute.py --output results/recomputed_local
```

The script uses the included CSV and JSONL files. It produces task and seed summaries, paired confidence intervals, training-source checks and count-based audits. The reference output is in [results/recomputed](results/recomputed/); `validation.json` records the environment, input hashes and 112 matched checks.

Check the supplied files:

```bash
python analysis/verify_checksums.py
```

## Find the material

| Directory | Contents |
|---|---|
| `manifests/` | Main task selection, SQV records and windows, registered training-signal hashes |
| `results/` | Main, reporting-ablation, SQV and HB outcomes; registered terminal counts; recomputed outputs |
| `provenance/` | Candidate, task, physical-input and corpus-instance mappings |
| `training/` | Candidate trajectories, screening records, SFT corpora, training configurations and logs |
| `configs/` | Experiment correspondence, statistical settings and canonical v2.0.0 parameter registry |
| `docs/` | Reproduction instructions, supplementary tables and method specifications |
| `audits/` | Expert claim cross-counts |
| `analysis/` | Portable statistical recomputation and file verification |

## Interpretation

Primary EDS uses strict majorities within tasks, equal task weights and then equal training-seed weights. Untrained references use S = 1. SQV Macro-F1 is computed separately within each seed and then averaged. Source-group and seed resampling preserves the pairing; the eight-group sensitivity analysis also permits source weights to change.

The full condition of the reporting ablation and the 1,024-trajectory training-scale condition reuse the corresponding primary evaluations. They are recorded as reuse relationships in [the experiment registry](configs/experiment_registry.csv).

Terminal, expert-claim and call summaries are identified as count-based arithmetic checks. Method documents contain the registered rules and normative pseudocode. [The data dictionary](data_dictionary.md) defines each file's unit and fields; [signal selection](docs/data_access.md) identifies the original datasets.
