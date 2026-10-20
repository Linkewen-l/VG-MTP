# SQV recording and window protocol

SQV [45] records motor-bearing vibration and tachometer pulses on a SpectraQuest test rig with an NSK6203 drive-end bearing. The seven public state directories NC, IF_1–IF_3 and OF_1–OF_3 define the source groups used here. IF and OF states are pooled into inner-race and outer-race diagnosis classes; no ball-fault class is included. All SQV records belong to the frozen-method evaluation partition, with none assigned to this study’s training or development data. Repository Table S4 lists the included public and local record IDs in matching ascending order.

Repository Table S4. SQV source groups and included recordings.

| Public group | Diagnosis | Included record IDs | Local record IDs | Records / tasks |
| --- | --- | --- | --- | --- |
| NC | Normal | REC3642–REC3647 | SQV001–SQV006 | 6 / 12 |
| IF_1 | Inner race | REC3597–REC3602 | SQV010–SQV015 | 6 / 12 |
| IF_2 | Inner race | REC3619–REC3621; REC3623–REC3625 | SQV020–SQV025 | 6 / 12 |
| IF_3 | Inner race | REC3532–REC3537 | SQV029–SQV034 | 6 / 12 |
| OF_1 | Outer race | REC3513–REC3518 | SQV035–SQV040 | 6 / 12 |
| OF_2 | Outer race | REC3494–REC3499 | SQV041–SQV046 | 6 / 12 |
| OF_3 | Outer race | REC3476–REC3481 | SQV047–SQV052 | 6 / 12 |

Note: Every group contains six recordings and 12 window tasks, giving 42 recordings and 84 tasks. For group g and record RECxxxx, the paired files are g/RECxxxx_ch2.txt and g/RECxxxx_ch3.txt in repository [45]. Local IDs map to the public recording IDs in Repository Table S4. Appending _S or _V to the local record ID identifies the steady-speed or deceleration task; training seed and workflow identify its individual execution.

The 52-record candidate manifest includes ten excluded records. NC/REC3648–REC3650 (SQV007–SQV009), IF_1/REC3604–REC3606 (SQV017–SQV019) and IF_2/REC3626–REC3628 (SQV026–SQV028) have no qualifying 2 s stable segment. IF_1/REC3603 (SQV016) is 1.48 s long and has no valid tachometer pulses. Both phase windows must qualify for a record to enter the paired experiment. No total-record-duration threshold is imposed, and no padding, concatenation or synthetic extension is used. Included recordings have actual durations of 18 s (12 records), 20 s (9) or 30 s (21).

Windowing uses ch2 vibration in g and ch3 tachometer pulses in V at the header sampling rate of 25,600 Hz. The two channels share the acquisition start and window boundaries. Speed follows the pulse-edge convention in the author’s SpeedExtraction.py [45]: one pulse per revolution, a downward voltage change below −1.7 V with the new sample below −4 V, and more than 200 samples between accepted edges. The first data sample is time zero; sample indices divided by the header sampling rate define time, avoiding rounded text timestamps. Successive edge intervals give 60fs/Δk rpm, assigned to the later edge, followed by a centered nine-point median filter with edge padding.

Let p be the maximum filtered speed. The stable segment is the longest contiguous segment with speed at least 0.95p; the steady-speed 2 s window is centered within it. The deceleration window starts at that segment’s final speed timestamp and spans 2 s. Both start times are rounded to 0.01 s; the windows are half-open [start, start + 2 s), each containing 51,200 signal samples. The deceleration window must drop by at least 0.10p, with no successive filtered-speed increase greater than 5 rpm. Both channels must be present and compatible, and both windows must fit completely within the recording. Repository Table S5 gives the actual start times, so window membership does not depend on reinterpretation of the rule.

Before diagnostic evaluation, the inclusion criteria and window-selection rules above were fixed and applied uniformly to all candidate recordings. Both workflows and all five seeds used the resulting record and window manifest. The method, checkpoints and execution settings remained fixed throughout this unseen-source evaluation.

The bearing-model sources [46,47] provide the geometry used by bearing_order to calculate theoretical fault orders. Display rounding is applied after computation.

## Exact window boundaries

Use [the candidate and window manifest](../../manifests/sqv_records_windows.csv). The signal source is [SQ dataset with variable speed](https://github.com/shenliuuu/SQ-dataset-with-variable-speed-for-fault-diagnosis). Repository Tables S4 and S5 provide the readable selections. Source references [45–47] follow the manuscript bibliography.
