# Supplementary tables

Tables S1–S11 provide the detailed records and specifications cited by the accompanying manuscript. The statistics guide identifies the data and scripts used for numerical recomputation.

## Table S1

KAIST variable-speed file groups.

[Download CSV](table_S1.csv)

| Group | Health state | Filename key s | File indices k | Records | Nominal duration (s) |
| --- | --- | --- | --- | --- | --- |
| K01 | Normal | normal | 0, 1, 2 | 3 | 900 |
| K02 | Normal | normal | 3, 4, 5, 6 | 4 | 1,200 |
| K03 | Inner-race fault | inner | 0, 1, 2 | 3 | 900 |
| K04 | Inner-race fault | inner | 3, 4, 5, 6 | 4 | 1,200 |
| K05 | Outer-race fault | outer | 0, 1, 2 | 3 | 900 |
| K06 | Outer-race fault | outer | 3, 4, 5, 6 | 4 | 1,200 |
| K07 | Ball fault | ball | 0, 1, 2 | 3 | 900 |
| K08 | Ball fault | ball | 3, 4, 5, 6 | 4 | 1,200 |
| Total | Four health states | — | 0–6 per state | 28 | 8,400 |

## Table S2

Seed-level EDS for the primary 240-task evaluation.

[Download CSV](table_S2.csv)

| Training seed | VG-MTP | D-only-full | LLM-process-full | Final-label-only | Unadapted | Dynamic rule |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 72.08 | 67.50 | 70.42 | 64.58 | — | — |
| 23 | 74.17 | 69.17 | 72.50 | 66.25 | — | — |
| 37 | 75.83 | 70.42 | 74.17 | 63.75 | — | — |
| 53 | 73.75 | 67.92 | 71.67 | 65.00 | — | — |
| 71 | 76.67 | 70.00 | 75.00 | 67.50 | — | — |
| Mean (S = 5) | 74.50 | 69.00 | 72.75 | 65.42 | — | — |
| Reference (S = 1) | — | — | — | — | 56.7 | 67.9 |

## Table S3

SQV EDS by training seed and the speed-phase × workflow interaction.

[Download CSV](table_S3.csv)

| Training seed | Steady / full | Steady / alternative | Decel. / full | Decel. / alternative | Interaction (pp) |
| --- | --- | --- | --- | --- | --- |
| 11 | 90.48 | 90.48 | 88.10 | 80.95 | 7.14 |
| 23 | 90.48 | 88.10 | 88.10 | 73.81 | 11.90 |
| 37 | 90.48 | 90.48 | 88.10 | 78.57 | 9.52 |
| 53 | 90.48 | 88.10 | 90.48 | 78.57 | 9.52 |
| 71 | 92.86 | 92.86 | 90.48 | 80.95 | 9.52 |
| Mean | 90.95 | 90.00 | 89.05 | 78.57 | 9.52 |

## Table S4

SQV source groups and included recordings.

[Download CSV](table_S4.csv)

| Public group | Diagnosis | Included record IDs | Local record IDs | Records / tasks |
| --- | --- | --- | --- | --- |
| NC | Normal | REC3642–REC3647 | SQV001–SQV006 | 6 / 12 |
| IF_1 | Inner race | REC3597–REC3602 | SQV010–SQV015 | 6 / 12 |
| IF_2 | Inner race | REC3619–REC3621; REC3623–REC3625 | SQV020–SQV025 | 6 / 12 |
| IF_3 | Inner race | REC3532–REC3537 | SQV029–SQV034 | 6 / 12 |
| OF_1 | Outer race | REC3513–REC3518 | SQV035–SQV040 | 6 / 12 |
| OF_2 | Outer race | REC3494–REC3499 | SQV041–SQV046 | 6 / 12 |
| OF_3 | Outer race | REC3476–REC3481 | SQV047–SQV052 | 6 / 12 |

## Table S5

Actual SQV window starts relative to the beginning of each recording.

[Download CSV](table_S5.csv)

| Record ID | Steady (s) | Decel. (s) | Record ID | Steady (s) | Decel. (s) | Record ID | Steady (s) | Decel. (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SQV001 | 7.54 | 11.73 | SQV022 | 7.91 | 12.08 | SQV039 | 12.45 | 17.82 |
| SQV002 | 7.51 | 11.69 | SQV023 | 12.69 | 18.04 | SQV040 | 12.46 | 17.82 |
| SQV003 | 7.66 | 11.84 | SQV024 | 12.58 | 17.97 | SQV041 | 7.52 | 11.71 |
| SQV004 | 13.12 | 18.49 | SQV025 | 13.17 | 18.55 | SQV042 | 7.84 | 12.00 |
| SQV005 | 13.03 | 18.42 | SQV029 | 8.22 | 12.40 | SQV043 | 7.78 | 11.94 |
| SQV006 | 12.72 | 18.10 | SQV030 | 7.51 | 11.69 | SQV044 | 13.14 | 18.51 |
| SQV010 | 7.57 | 11.77 | SQV031 | 7.78 | 11.96 | SQV045 | 13.01 | 18.39 |
| SQV011 | 7.68 | 11.86 | SQV032 | 12.87 | 18.23 | SQV046 | 13.24 | 18.61 |
| SQV012 | 7.72 | 11.89 | SQV033 | 12.73 | 18.13 | SQV047 | 7.68 | 11.85 |
| SQV013 | 11.89 | 17.26 | SQV034 | 12.88 | 18.26 | SQV048 | 8.51 | 12.68 |
| SQV014 | 12.86 | 18.25 | SQV035 | 7.74 | 11.93 | SQV049 | 9.03 | 13.20 |
| SQV015 | 13.60 | 18.98 | SQV036 | 7.64 | 11.82 | SQV050 | 12.89 | 18.27 |
| SQV020 | 7.59 | 11.79 | SQV037 | 7.72 | 11.89 | SQV051 | 12.97 | 18.35 |
| SQV021 | 7.90 | 12.08 | SQV038 | 12.89 | 18.27 | SQV052 | 13.37 | 18.74 |

## Table S6

Registered recording selection by partition.

[Download CSV](table_S6.csv)

| Partition / source | Recording selection | Records |
| --- | --- | --- |
| Train / HUST | Local keys C01–C33; each has suffix _2000_0.mat, _3000_2.mat and _4000_4.mat. | 99 |
| Train / Paderborn | b = KA01, KA03, KA04, KA05, KA06, KA07: i = 1–8; b = KA08, KA09, KA15: i = 1–7. | 69 |
| Dev / Paderborn | b = K001–K006, KI01, KI03, KI04, KI05, KI07, KI08, KI16, KI17; i = 1–4. | 56 |
| Sealed / Paderborn | b = KA16, KA22, KA30, KI14: i = 1–12; b = KI18, KI21: i = 1–10. | 68 |
| Sealed / KAIST | vibration_{s}_{k}.csv and rpm_{s}_{k}.csv; s = normal, inner, outer, ball; k = 0–6. | 28 |
| External / HB | {h}-{v}-{r}.mat; h = H, I, O, B, C; v = A–D; r = 1–3. | 60 |

## Table S7

Main-evaluation groups and task counts.

[Download CSV](table_S7.csv)

| Source group | Record indices / file labels | Records | Tasks |
| --- | --- | --- | --- |
| KAIST / normal | K01/K02; k = 0–6 | 7 | 28 |
| KAIST / inner | K03/K04; k = 0–6 | 7 | 28 |
| KAIST / outer | K05/K06; k = 0–6 | 7 | 28 |
| KAIST / ball | K07/K08; k = 0–6 | 7 | 28 |
| Paderborn / KA16 | i = 1–12 | 12 | 12 |
| Paderborn / KA22 | i = 1–12 | 12 | 12 |
| Paderborn / KA30 | i = 1–12 | 12 | 12 |
| Paderborn / KI14 | i = 1–12 | 12 | 12 |
| Paderborn / KI18 | i = 1–10 | 10 | 10 |
| Paderborn / KI21 | i = 1–10 | 10 | 10 |
| HB / H | A–D; trials 1–3 | 12 | 12 |
| HB / I | A–D; trials 1–3 | 12 | 12 |
| HB / O | A–D; trials 1–3 | 12 | 12 |
| HB / B | A–D; trials 1–3 | 12 | 12 |
| HB / C | A–D; trials 1–3 | 12 | 12 |
| Total | 15 source groups | 156 | 240 |

## Table S8

Matching strata and registered training sources.

[Download CSV](table_S8.csv)

| Matching stratum | Physical trainingrecords | Basetasks | Poolsize | D / LLMeligible | VG eligible | FinalSFT |
| --- | --- | --- | --- | --- | --- | --- |
| A: MultiCond | HUST 66 +Paderborn 18 | 120 | 598 | 512 / 497 | 481 | 478 |
| B: WideVar (“HB”) | HUST 33 | 64 | 320 | 274 / 265 | 258 | 256 |
| C: BenchTransfer | Paderborn 51 | 68 | 362 | 310 / 301 | 291 | 290 |
| Total | 168 | 252 | 1,280 | 1,096 / 1,063 | 1,030 | 1,024 |

## Table S9

Frozen signal processing parameters.

[Download CSV](table_S9.csv)

| 操作 | 参数值 | 用途与计算方式 |
| --- | --- | --- |
| STFT | 2,560 点；75% 重叠；hop 640；Hann 窗 | 两流程共用。在 25.6 kHz 下窗长为 0.1 s；其他采样率按实际 fs 换算时间。 |
| 脊线提取 | 帧内最大幅值的 0.6 倍；20 Hz 连接容差；持续 ≥ 0.5 s | 保留达阈值的显著峰，跨帧连接，多条脊按平均幅值排序，主脊提供 f(t)。 |
| 分段 FFT | 2,560 点；50% 重叠；Hann 窗 | ALT 频谱路径；输出各段平均幅度谱。 |
| 包络谱 | 希尔伯特平方包络；FFT 长度 16,384 | 显著峰突出度 ≥ 中位数 + 6σ，且位于轴承特征频带。 |
| 角域重采样 | 每转 128 点；三次样条；低通截止 0.45 × 采样率 | 有效脉冲沿插值得到转速序列；先滤波再重采样；最高分析阶次 64。 |
| 阶次谱 | FFT 长度取 2 的幂 | 在每转 128 点的角域网格上，第 k 个 FFT 频点对应 128k/N_FFT order；输出阶次、幅值、突出度。 |
| SNR | 10log10(P_sig/P_noise)；低能量帧分位 5% | P_noise 为窗内能量最低 5% 帧的平均功率；P_sig 为窗平均功率减 P_noise。 |
| 瞬时阶次 | o(t) = 60f(t)/n(t) | ALT 的变速定位路径；以窗内中位阶次进行理论匹配。 |

## Table S10

Tool inputs outputs and prerequisite checks.

[Download CSV](table_S10.csv)

| 工具 | 输入与输出 | 前提与错误状态 |
| --- | --- | --- |
| signal_qc | 输入信号窗、fs、通道标识和可选 tach；输出 qsig、裁剪比例、SNR、tach_q、转速和警告。 | 文件可解析且 fs 已声明；FILE_PARSE、SAMPLING_MISMATCH、NO_PULSE、SPEED_SOURCE_CONFLICT。 |
| stft | 输入信号窗；输出时频图和脊线瞬时频率。 | signal_qc 有效；APPLICABILITY_FAILURE。 |
| fft_envelope | 输入信号窗；输出频率、幅值和突出度。 | signal_qc 有效；沿用仓库补充表 S9 参数。 |
| order_resample | 输入信号和已验证转速；输出角域序列及其每转采样数。 | tach_q ≥ 0.80、转速连续且无相关冲突；TACH_QUALITY_LOW、SPEED_SOURCE_CONFLICT、NONPHYSICAL_JUMP。 |
| order_spectrum | 输入角域序列；输出阶次峰、幅值和突出度。 | order_resample 成功。 |
| bearing_order | 输入几何、转速值与来源、可选观测峰、目标部位；输出理论阶次、故障频率和匹配偏差。 | 几何完整合法，所用转速来源无冲突；GEOMETRY_INCOMPLETE、GEOMETRY_ILLEGAL、SPEED_SOURCE_CONFLICT。 |
| claim_checker | 输入带逐条引用的报告；输出 source_ok、numeric_ok、semantic_ok、dependency_ok。 | 报告可解析；DANGLING_REFERENCE、NUMERIC_OUT_OF_TOL、UNIT_CONFLICT、SEMANTIC_UNSUPPORTED。 |
| expert_classifier | 输入信号窗、fs、传感器模态和安装方向；输出 class_probs、置信度 conf 与输入适用域分数 adom。检查点 exp_resnet1d_trn_v1 仅在仓库补充表 S6 训练分区拟合。 | signal_qc 有效且输入 adom ≥ 0.70；未达阈值返回 APPLICABILITY_FAILURE。分类概率不能单独替代 g₃ 机理证据。 |

## Table S11

Paired majority outcomes by training seed.

[Download CSV](table_S11.csv)

| Training seed | Bothpass | VGonly | LLMonly | Bothfail | VG / LLMsuccesses | Net gain(pp) |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 168 | 5 | 1 | 66 | 173 / 169 | +1.67 |
| 23 | 173 | 5 | 1 | 61 | 178 / 174 | +1.67 |
| 37 | 177 | 5 | 1 | 57 | 182 / 178 | +1.67 |
| 53 | 172 | 5 | 0 | 63 | 177 / 172 | +2.08 |
| 71 | 179 | 5 | 1 | 55 | 184 / 180 | +1.67 |
| All five seeds | 869 | 25 | 4 | 302 | 894 / 873 | +1.75 |
