# VG-MTP manuscript appendices

These appendices accompany **VG-MTP: Verifier-Guided Tool Planning for Rotating Machinery Fault Diagnosis with Compact Language Models**. They retain the scientific content and original labels of Appendices A–C from the complete manuscript. The main submission presents the core method and results; the detailed protocols and supporting records are available here.

- [Read the complete appendices as PDF](Appendices_A-C_20261102.pdf)
- [Download the editable Word document](Appendices_A-C_20261102.docx)
- [Section and table index](section_index.csv)

Version: 2 November 2026. Equations remain native, editable Word equations, and tables remain editable. The PDF provides a reading copy with the same content. Citations retain the source-manuscript reference numbers; the seven cited entries are reproduced at the end. References to main-text sections, figures and tables refer to the accompanying paper. A label such as **Repository Table B.5** in the paper denotes **Table B.5** in these appendices.

## Appendix A Evaluation and supervision details

- A.1 Evaluation units and terminal decisions
- A.2 Metric aggregation
- A.3 Trajectory supervision and runtime checks

## Appendix B Experimental settings and supplementary results

- B.1 Data sources and partition scope
- B.2 Model and execution settings
- B.3 Paired statistical analysis
- B.4 Tolerances and perturbation settings
- B.5 Training scale and expert audit design
- B.6 Results by training seed
- B.7 SQV recording manifest and window protocol
- B.8 Main evaluation mapping and partition audit
- B.9 Training sources and process filtering control
- B.10 Runtime and reporting ablations

## Appendix C Execution rules and call audit

- C.1 Required evidence by diagnostic granularity
- C.2 Evidence state and conflict handling
- C.3 Acceptance scoring from quality and applicability
- C.4 Main loop and terminal decisions
- C.5 Dynamic rule-based planner
- C.6 Fixed parameters for the full and alternative pipelines
- C.7 Tool contracts and call examples
- C.8 Complete trajectory under conflicting speed information
- C.9 Call accounting and consistency checks
- C.10 Paired outcomes for VG-MTP and LLM-process-full
- C.11 Equivalent evidence paths and threshold checks

## Relation to other repository materials

The appendices complement the [statistical reproduction guide](../reproduction.md), [method specifications](../method/README.md), [training records](../../training/README.md), and [Tables S1–S20](../supplementary_tables/README.md). Numerical source tables and underlying records remain at their existing paths. The [paper-to-file index](../../paper_map.csv) includes current manuscript locations and preserves older locations in a separate column.

The current manuscript uses Figures 2–6 for the earlier Figures 4-1–4-5, and Tables 2–11 for the earlier Tables 4-1–4-10. Appendix labels A–C and repository table labels S1–S20 are unchanged.

**Code and model weights: coming soon.** This update publishes the manuscript appendices and navigation; it does not change the available model or code release status.
