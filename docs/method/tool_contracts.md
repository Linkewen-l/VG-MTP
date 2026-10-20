# Tool contracts

全部八个工具使用 v1.0，并向可比较的 Agent 提供相同接口。每条实际派发调用保留输入、输出、单位、前提、错误状态、容差、版本、来源哈希和成本，对应式（3-6）。接口中的信号字段引用已有输入窗，工具返回值保留其真实输出来源。expert_cls 为 expert_classifier 的日志别名，按同一 call_id 计为一次派发；表 C4 的调用总数已包含该工具，不能再重复加入。

Repository Table S10. Tool inputs outputs and prerequisite checks.

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

expert_classifier 的适用域分数由输入窗口特征与 C.3 的冻结均值、协方差及 d_ref 计算，区别于分类置信度 conf；派发前检查不以待生成的分类概率作为前提。输出中的 adom 记录该输入检查的分数，最终引用仍须通过相应证据与依赖检查。运行时与离线物理复核共享同一原精度判定输入，见 C.9。

bearing_order 的输入结构为 geometry = {n, d_ball, D_pitch, alpha}、speed = {value, source}、observed_peaks 和 target。几何字段须完整、数值有限、单位一致，滚动体数为正整数，直径为正且滚动体直径小于节圆直径；角度按声明单位转换后计算。观测峰可用频率或阶次表达，但必须标明单位和来源。输出包含 BPFO、BPFI、BSF、FTF，以及理论频率与匹配偏差。若前提失败，返回错误代码，不生成可引用的理论匹配成功记录。

除式（3-10）和（3-11）外，BSF 阶次为 [D_pitch/(2d_ball)]·[1 − (d_ball·cos(alpha)/D_pitch)²]，FTF 阶次为 [1 − (d_ball/D_pitch)cos(alpha)]/2。理论频率等于相应阶次乘轴频；匹配检查先统一单位，再比较 0.05 order 或 max(0.5 Hz, 1%) 容差。

在表 C3 的实际调用中，bearing_order 收到 speed = {value: 1480, source: file} 和 target = BPFI；当时账本同时保存 1812 rpm 的转速计估计，ρ > 0.10，因此前置验证返回 SPEED_SOURCE_CONFLICT，调用没有派发。该例展示了输入字段、前提、错误状态与计数的对应关系。signal_qc 与 fft_envelope 的输出支持拒答报告中的已确认事实；终态验证器按拒答规范核验这些事实及缺口，该内部判定不增加派发调用。辅助专家模型另受 adom ≥ 0.70 的引用约束，其概率不能直接替代机理证据。
