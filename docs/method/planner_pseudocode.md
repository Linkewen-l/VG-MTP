# Planner specification

Normative pseudocode for the learned planner executor and the fixed dynamic-rule comparator. Both use canonical v2.0.0, the same tool contracts, dispatch budget and terminal rules.

下列伪代码分别表示规划器动作、派发前检查、真实执行和终态门控。g_req 始终不变；skip 和 blocked 保存本次执行内禁用的工具或调用签名。预算以实际派发次数计，提出和阻断次数单独记账。

```text
MAIN(task):
    L, trace, ctx = empty
    g_req = task.requested_granularity
    g_try = g_req; g_min = task.minimum_granularity
    dispatched = 0; blocked = empty; skip = empty
    start episode clock
    loop:
        if elapsed >= 180 s: return BUDGET_FAILURE
        S = STATE(L, task.spec, g_try, current_budget)
        a = PLAN(S, task.request, allowed_tools, ctx, blocked, skip)
        if elapsed >= 180 s: return BUDGET_FAILURE
        if a is CALL(tool, args):
            if dispatched >= 12: return BUDGET_FAILURE
            if same blocked call and no substantive repair:
                record blocked feedback; continue
            v = VERIFY_PRE(tool, args, S)
            if v fails:
                record proposal and block in trace
                update blocked and ctx; continue
            dispatched += 1
            o = EXECUTE(tool, args, timeout = 30 s)
            append executed status, outputs and provenance to L
            append dispatched event to trace
            if o is unrecoverable: return EXECUTION_FAILURE
            if o is timeout:
                record one structured repair feedback
                do not repeat this actual execution
                return BUDGET_FAILURE
            if elapsed >= 180 s: return BUDGET_FAILURE
            continue
        if a is DOWNGRADE(g):
            require g_min <= g < g_try
            g_try = g; continue
        if a is STOP or ABSTAIN:
            d = TERMINALIZE(L, task.spec, g_req, g_try, g_min)
            if elapsed >= 180 s: return BUDGET_FAILURE
            return d
```

到达 12 次派发后仍可执行不调用工具的终态检查，但不能再派发第 13 次调用。不可恢复错误和超时先于接受判定处理；其运行保留在 EDS 分母且记 0。工具超时后的结构化修复反馈记录失败原因，不以再次执行后的成功替换本次失败。

```text
TERMINALIZE(L, spec, g_req, g_try, g_min):
    if normal label is permitted and N1 through N4 all hold:
        candidates = [health]
    else:
        candidates = [g_try, g_try-1, ..., g_min]
    for g in candidates:
        S = STATE(L, spec, g, current_budget)
        if required evidence for g is incomplete: continue
        if critical claims fail any of the four checks: continue
        if g is forbidden by the request: continue
        if a relevant P1 conflict remains: continue
        c = SCORE(S, g, fixed_request = g_req)
        if c >= 0.72: return ACCEPT(g, verified_claims)
        return SELECTIVE_ABSTENTION
    return EVIDENTIAL_ABSTENTION(reason_codes, confirmed_evidence)
```

此处 ACCEPT 包括被请求允许的正常结论、目标粒度诊断和较粗粒度诊断。只有通过证据门的候选才可进入接受评分。最低允许粒度仍因证据、声明、粒度约束或相关 P1 冲突失败时，统一返回 ⊥evid，并保留具体原因。

C.5 动态规则规划器

动态规则规划器无学习参数，评测前冻结分支规则，与 VG-MTP 共享工具、输入、运行时验证、12 次派发预算和超时设置。修复反馈优先于常规路径选择；被跳过的工具和相关依赖持续保存在本次执行状态中，不能被后续 ORDER 路径选择覆盖。PROPOSE 对所有调用出口执行同一禁用检查，包含初次质量检查、转速复核和声明检查。

```text
PROPOSE(call):
    if call is skipped or unchanged in blocked: return ABSTAIN
    return CALL(call)

DYN_PLAN(S, request, ctx, blocked, skip):
    if calls_remaining == 0 or time_remaining < 30 s: return STOP
    feedback = latest unhandled repair feedback
    if feedback is SPEED_SOURCE_CONFLICT:
        if tachometer recheck not performed:
            return PROPOSE((signal_qc, tachometer_recheck))
        add all calls depending on disputed speed to skip
    if feedback is TACH_QUALITY_LOW or APPLICABILITY_FAILURE:
        add failed tool and its dependent calls to skip
    if feedback is GEOMETRY_INCOMPLETE or GEOMETRY_ILLEGAL:
        if g_try > g2 and g_min <= g2: return DOWNGRADE(g2)
        add geometry-dependent calls to skip
    mark feedback handled
    if initial signal_qc not performed:
        return PROPOSE((signal_qc, initial_inputs))
    if no tachometer or tach_q < 0.80 or speed calls are skipped:
        path = SPECTRAL
    elif window speed range > max(10 rpm, 1%): path = ORDER
    else: path = SPECTRAL
    ORDER calls = [fft_envelope, tachometer_recheck,
                   order_resample, order_spectrum, bearing_order]
    SPECTRAL calls = [fft_envelope,
                     stft if E2.2 is unresolved,
                     bearing_order if required by the candidate]
    for call in selected path:
        if not performed and not skipped and not blocked:
            return PROPOSE(call)
    if current candidate has not been claim-checked:
        return PROPOSE((claim_checker, current_report))
    if evidence gate for current candidate passes: return STOP
    if g_try > g_min: return DOWNGRADE(g_try-1)
    return ABSTAIN
```

路径中的 call 表示工具与按当前状态构造的规范化参数二元组。signal_qc 的初次检查和转速复核按不同调用目的登记。转速复核仍存在冲突时，不重提依赖该来源的调用。正常候选也执行 N4 所需的理论特征检查。每次降级按新的候选重新检查证据和声明。

无修复时，ORDER 路径含初次质量检查、包络分析、转速复核、角域重采样、阶次谱、理论匹配和声明检查，共 7 次。SPECTRAL 基本路径为质量检查、包络分析和声明检查，按证据缺口增加 STFT 或理论匹配，通常为 3–5 次。动态规则规划器平均调用 6.0 次；VG-MTP 在 9,900 次计划执行中派发 64,210 次，均值为 6.49。调用均值不能单独区分探索、复核和修复的占比。对应 EDS 为 67.92% 和 74.50%，配对比较见表 4-4。
