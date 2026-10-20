# Training and execution settings

Canonical v2.0.0 defines the registered experimental specification. The following settings give the complete configuration behind manuscript Tables B2 and B3.

| Item | Frozen value |
| --- | --- |
| Planner backbone | Qwen/Qwen3.5-9B (open weights). |
| Model revision | c202236235762e1c871ad0ccb60c8ee5ba337b9a. |
| Training software | Python 3.11.9, PyTorch 2.9.1, Transformers 5.0.0, PEFT 0.18.0, and Accelerate 1.12.0. |
| Inference software | vLLM 0.28.0, CUDA 12.8, and an OpenAI-compatible API. |
| Quantization | None; the model weights, LoRA weights, and KV cache all use bf16. |
| Conversation template | chat_template.jinja bundled with the model repository; enable_thinking=false; qwen3_coder as the tool parser. |
| Context and output limits | max_model_len=32768; max_new_tokens=1024. |
| Decoding configuration | Temperature 0.2, top-p 0.8, repetition penalty 1.05; evaluation random seeds are jointly determined by the training seed and episode ID. |
| Adaptation method | LoRA supervised fine-tuning. |
| LoRA rank / scaling factor α | 16 / 32. |
| LoRA dropout | 0.05. |
| Optimizer | AdamW; β1=0.9, β2=0.95, weight decay 0.01, and gradient clipping 1.0. |
| Learning rate and schedule | Peak learning rate 1×10⁻⁴; cosine decay after 3% linear warmup. |
| Batch configuration | Per-GPU microbatch 1, accumulation 16; effective batch 16 packed sequences. Length-grouped concatenation with sample-boundary attention masking; gradient checkpointing enabled. |
| Training sequence length | 8,192 tokens; overlength trajectories are truncated at tool-call boundaries, whereas terminal reports are never truncated. |
| Training epochs and precision | Nominal corpus budget: up to three epochs; stop at max_steps = 192 optimizer updates per seed; bf16. Packing prevents interpreting 192 × 16 / 1,024 as completed corpus epochs. |
| Training seeds | 11, 23, 37, 53, 71. |
| Maximum tool calls | At most 12 calls are dispatched per evaluation episode. |
| Primary candidate trajectory pool | 1,280 trajectories. |
| Primary SFT trajectories | 1,024 trajectories each for Final-label-only, D-only-full, LLM-process-full and VG-MTP. |
| Matching variables | Physical training source, target matching stratum, fault class, speed regime, path length and teacher source. |
| Token-budget balance | Full-trajectory controls share optimizer updates and a maximum of 25,165,824 consumed token positions per seed. Nominal corpus totals differ by at most 0.181%; B.9 separately reports consumed tokens for seed 37. |
| Shared runtime controls | Tool registry, runtime verifier, call budget, timeouts, prompt version, and paired decoding random seeds. |

The cost-efficient frontier baseline is gpt-5-mini-2025-08-07. The high-capability baseline and teacher use gpt-5-2025-08-07. Both use the Responses API with medium reasoning effort. The shared registry comprises signal_qc, stft, fft_envelope, order_resample, order_spectrum, bearing_order, claim_checker and expert_classifier, all at v1.0. The auxiliary classifier uses frozen checkpoint exp_resnet1d_trn_v1, fitted only on the Repository Table S6 training partition; its applicability calibration is defined in C.3 and its contract in Repository Table S10.

Each trainable method has 180 × 3 × 3 + 60 × 2 × 3 = 1,980 primary executions per training seed, giving 9,900 across five seeds. These yield 1,200 task–seed summaries under the strict-majority rule in Appendix A. Timeouts and executions without a legal terminal state remain in the planned denominator with EDS = 0. Table 4-5 uses a different denominator: base-episode incidence counts tasks with at least one timeout or budget exhaustion. Untrained comparators use S = 1.

SQV uses the five frozen VG-MTP checkpoints and the settings in Tables B2–B3. It uses one prompt and one execution per task, seed and workflow: 42 records × two phases × five seeds × two workflows = 840 executions. ALT disables only order_resample and order_spectrum, retaining the other six tools without retraining. Expert classification remains subject to the same cross-bench applicability guard; g₃ localization uses mechanistic evidence. Both workflows can produce location-level diagnoses (C.6); the same 420 full-method executions supply Table 4-18. Failed outcomes are not replaced by successful retries.

## Numerical tolerances

| Control | Frozen value | Operational specification |
| --- | --- | --- |
| Maximum number of dispatched tool calls | 12 | Dispatch at most 12 calls. After the twelfth call, only a terminal decision without an additional tool call is allowed; an attempted thirteenth dispatch fails the budget gate. |
| Theoretical–observed order-matching tolerance | 0.05 order | The deviation in case_vs_median_017 is 0.03 order. |
| Relative-difference threshold for speed sources | 0.10 | Values above this threshold trigger SPEED_SOURCE_CONFLICT. |
| Tachometer-quality threshold | 0.80 | If the quality score is below this value, a speed-synchronous tool may not be used to form a diagnosis at the target granularity. |
| Expert-model applicability threshold | 0.70 | If the normalized applicability-domain score is below this value, expert-model output may not be cited in a terminal state. |
| Numerical tolerance for speed | max(10 rpm, 1%) | Used for recomputing speed fields and checking claims. |
| Numerical tolerance for frequency | max(0.5 Hz, 1%) | Used for frequency peaks and fault-frequency claims. |
| Tolerance for probabilities and normalized scores | 0.01 | Used for probabilities, quality scores, and applicability-domain scores. |
| Relative amplitude tolerance | 2% | Amplitudes are compared only under the same preprocessing chain and in the same unit. |
| Acceptance threshold θ* | 0.72 | Frozen on the development set; test-time scanning is used only for the risk–coverage curve. |
| Timeout per tool call | 30 s | Record one structured repair feedback after timeout without repeating that actual execution. The timed-out run remains a failure. |
| Total timeout per evaluation episode | 180 s | A timeout or failure to form a legal terminal state returns a budget failure and sets EDS = 0. |

Time is measured in seconds, frequency in hertz and speed in rpm, with explicit unit conversions. Order is dimensionless. Unit compatibility is checked before numerical tolerance. Relative disagreement between speed sources is measured symmetrically.

ρₙ = |nmeta − ntach| / max(nmeta, ntach).

The acceptance score uses grouped five-fold logistic calibration on training/development data with regularization λ = 1. Its frozen intercept is b = −2.0 and weights are (1.0, 0.6, 1.2, 0.8, 0.5, 0.3, −1.5), in the feature order below. The operating threshold is θ* = 0.72. Score only candidates that pass the evidence gate. REC retains the requested-granularity reference; Ξₑ(g) contains conflicts relevant to the candidate. Appendix C.3 defines the features and C.4 gives the decision order.

cₑ(g) = σ(b + wᵀzₑ(g)),    zₑ(g) = (qsig, adom, REC, NF, PC, pplan, I[Ξₑ(g) ≠ ∅]).

Per-method and per-seed training configuration files are in [training/training_logs](../training/training_logs/).
