# VG-MTP 论文配套复现材料

本材料对应《Verifier-guided tool planning for evidence-grounded engineering decisions with compact language models》。研究关注小模型如何在领域约束下规划工具、获取证据并形成受支持的结论，机械诊断作为工程验证场景。

**规划器与执行系统代码、模型权重即将发布（coming soon）。** 统计复算脚本已提供。

## 内容与稿件对应

附录 A–C 已恢复在当前手稿中。[仓库附录副本](docs/manuscript_appendices/README.md)提供匿名元数据的 Word 和 PDF 版本。附录 C.12 保存从方法正文移出的信号分析关系式；主文公式编号及交叉引用同步更新。

当前关键词为 Compact language models、Tool planning、Domain constraints、Process supervision、Evidence verification 和 Engineering decision support。

1. 查看[论文与文件对应表](paper_map.csv)，定位结果与材料。
2. 查看[支撑表 S1–S20](docs/supplementary_tables/README.md)，浏览逐种子记录、窗口、训练分层和图 2–6 的来源数值表。
3. 按[复算说明](docs/reproduction.md)运行脚本，对照 `results/recomputed/`。
4. 通过[训练说明](training/README.md)核对候选、任务、输入和语料实例的关联。

## 主要复算结果

| 内容 | 结果 |
|---|---|
| 主评测 | 240 项任务、5 个训练种子；VG-MTP 74.50%，LLM-process-full 72.75%；差 1.75 个百分点，95% 区间 [1.00, 2.50] |
| 报告消融 | 1,200 对完整/无强制绑定结果；无强制绑定 68.83%；完整方法提高 5.67 个百分点，[4.55, 6.61] |
| SQV | 42 条记录、84 个任务、840 次流程执行；完整方法 EDS 90.00%，种子均值 Macro-F1 93.08% |
| 训练来源 | 1,280 个候选、252 项任务、168 条记录；20 份语料、61,440 条实例映射 |

在仓库根目录运行：

```text
python -m pip install -r analysis/requirements.txt
python analysis/recompute.py --output results/recomputed_local
python analysis/verify_checksums.py
```

结果解释遵循附录 A 的分母和聚合规则。主评测采用任务等权的严格多数 EDS；SQV 的 Macro-F1 先按训练种子计算，再平均。终态计数、专家交叉计数和调用汇总各自按对应分母核算。现有结果、数据划分、模型设置和统计口径保留。
