# VG-MTP 论文配套复现材料

本材料提供主评测、报告消融和 SQV 验证的配对数据，训练轨迹及来源映射，以及可直接运行的统计复算脚本。论文保留核心定义、统计方法和关键证据；详细记录与实现规范通过本目录查询。

**代码和模型权重即将发布（coming soon）。**

## 建议阅读顺序

1. 查看 [论文与文件对应表](paper_map.csv)，定位所需结果。
2. 查看 [补充表 S1–S20](docs/supplementary_tables/README.md)，浏览逐种子结果、文件窗口、训练分层以及图 4-1 至图 4-5 的来源数值表。
3. 按 [复算说明](docs/reproduction.md) 运行脚本，对照 `results/recomputed/`。
4. 通过 [训练说明](training/README.md) 核对候选、任务、物理输入和语料实例的关联。

## 可以复算的主要结果

| 内容 | 结果 |
|---|---|
| 主评测 | VG-MTP 74.50%，LLM-process-full 72.75%；差 1.75 个百分点，95% 区间 [1.00, 2.50] |
| 报告消融 | 无强制引用 68.83%；完整方法提高 5.67 个百分点，[4.55, 6.61] |
| SQV | 42 条记录、84 个任务、840 次执行；完整流程 EDS 90.00%，Macro-F1 93.08% |
| 来源链 | 1,280 候选、252 任务、168 记录；20 份语料、61,440 条实例映射 |

在本目录运行：

```text
python -m pip install -r analysis/requirements.txt
python analysis/recompute.py --output results/recomputed_local
python analysis/verify_checksums.py
```

结果解释遵循论文附录 A 的分母和聚合规则。主评测采用任务等权的多数 EDS；SQV 的 Macro-F1 先按训练种子计算再平均。终态计数、专家交叉计数和调用汇总各自按对应分母核算。
