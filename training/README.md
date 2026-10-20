# Training data and provenance

The supplied candidate trajectories, screening records, corpora, configurations and logs are preserved byte for byte.

| Material | Content |
|---|---|
| `trajectories/` | Three JSONL files containing 1,280 candidate trajectories |
| `screening/` | D decisions on 1,280 candidates; LLM and VG decisions on 1,096 D-passing candidates |
| `sft_corpus/` | Four methods × five seeds; 20 corpora, each with 1,024 distinct parent candidates and 3,072 epoch instances |
| `training_logs/` | Twenty training configuration and log sets |
| `checkpoints/` | Twenty checkpoint registration JSON files |
| `genlogs/` | Fifteen candidate-generation log files |
| `source_registry/` | Supplied pool specification and source inventory |

## Follow a sample to its source

Join `provenance/corpus_sample_map.csv` by `(corpus_file, epoch, sample_id)`. `corpus_line` is a one-based JSONL line number. Follow `parent_candidate_id` into `provenance/candidate_lineage.csv`, then `task_id` into `provenance/task_inputs.csv`. Each physical input has a registered file identifier, role, channel or nominal-speed input, window, partition and physical-file hash.

The 168 training records comprise 99 HUST and 69 Paderborn files. Candidate-pool labels such as HB and KAIST identify quota templates; physical datasets are given by `dataset` and `record_key`. In evaluation data, HB denotes Huang–Baddour.

Paderborn vibration is registered as `Y(Name = vibration_1).Data`, with X as the time axis. Available measured-speed channels and nominal-speed inputs have separate entries. Original corpus fields are preserved; `provenance/channel_field_mapping.csv` supplies their correspondence to the revised input register.

## Budget correspondence

Each method uses the registered 192 optimizer updates. Corpus token totals, packing capacity and tokens consumed have different meanings and retain their original fields. The 1,024-trajectory scale condition reuses the primary VG-MTP evaluation. The source register describes the content and joins of the supplied training files.
