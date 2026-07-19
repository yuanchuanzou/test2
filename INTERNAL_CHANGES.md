# 本轮修改列表（内部，合作者审阅用）

> 主文件：`GRB210704A-kilonova_v3_songxy.tex`（PRD 版）。只列本轮（Claude 协助）新做的修改；v2→v3 已完成的修改不在此列（可编译 `diff.tex` 查看）。
> 本轮全部修改可在 **`GRB210704A-kilonova_v3_changes.pdf`**（latexdiff：修改前 vs 修改后，蓝=新增、红/小字=删除）逐处查看。
> 另：此前误将 LIV_v2.tex 当作主文件时也做了一轮修订（见文末第二部分），这些修改同样是真实的错误修正与润色，已保留，可按需取舍。

## 第一部分：GRB210704A-kilonova_v3_songxy.tex（主文件）

### A. 遗留矛盾与断裂内容的修复（重点核对）

1. **"hundreds of seconds" 遗留矛盾**：Timescales 段引语仍写 "The dynamical time in the comoving frame is extremely short, on the order of hundreds of seconds"，但紧随其后的新公式给出 t′_dyn ~ 0.1 s。已改为 "only a fraction of a second"。
2. **内激波半径公式左右不一致**：R ≃ 2Γ²cδt ≃ 6×10¹² Γ²₂.₅ δt₋₃/(1+z) cm —— 左边解析式缺 (1+z)，右边数值式有。已统一为 R ≃ 2Γ²cδt/(1+z) ≃ …，并加 \label{eq:Ris}。
3. **断裂的 LaTeX：`T_{\rm dur,\\lab}`**（两处，`\\` 在数学模式中是换行）→ `T_{\rm dur,lab}`。
4. **断裂的 LaTeX：`\ \\\rm{cm}^{2}`**（σ_γγ 公式）→ `\ {\rm cm}^{2}`。
5. **n′_p 的 eqnarray 全行 \nonumber**：带 \label{eq:nbp} 却无编号，且缺对齐符。改为规范的单行 equation（保留编号）。
6. **重复标签**：`eq:sigmaKN-GBM` 同时用于 σ_KN 和 τ_KN 两个公式 → τ_KN 处改为 `eq:tauKN-GBM`，消除 multiply-defined 警告。
7. **未写完的小节**："Estimation based on statistical correlation" 只有半句 "There are empirical correltions between Γ and E_iso and L_iso:"（含拼写错误）就没了。已整体注释掉，并留 TODO 注释：若要补全，建议采用 Liang et al. 2010 (ApJ 725, 2209)、Lü et al. 2012 (ApJ 751, 49) 的 Γ₀–E_iso / Γ₀–L_iso 关系（**这两条文献目前不在 LIV.bib**，需先补充）；否则就删除该小节。
8. **量纲混用**：Discussion 中 "The total energy … estimated by the radiative E_γ,iso" 而公式为 E_tot,iso = E_γ,iso/ε_γ，随后却用 L_K ≲ (1−ε_γ)L_tot,iso（L_tot,iso 未定义）且数值全部用光度（L_γ,iso = 1e54 erg/s）。已统一为光度形式：L_tot,iso = L_γ,iso/ε_γ。
9. **误挂引文**："plus a PL function~\citep{1993ApJ...413..281B}"——Band et al. (1993) 是 BAND 函数文献，挂在 PL 后面是 v2 改 v3 时的残留。已移除该处引用（mBB 的引文保留）。
10. **附录 C 图题/正文与子图顺序不符**：图 (a)=mBB+PL、(b)=BAND+PL、(c)=mBB+BAND（按文件名核对），但正文与 caption 均写 "mBB+BAND, mBB+PL and BAND+PL"。已按 (a)(b)(c) 顺序改正并在 caption 中标注子图号。
11. **语义错误句**："The estimations above show that the GeV photons at the gap should be absorbed…"——被吸收的是缺口能段的光子，不是 GeV 光子。已改为 "the photons falling in the resonant band should be absorbed by the deuterium, while the other photons are able to escape…"。
12. **激活被注释的余辉一致性句**（附录 D 末尾）："Γ determined from the modeling with a specific model (e.g., a top-hat afterglow model; see Pieterse et al. 2026) is about 1000±600, … consistent with…"——原为注释，内容与正文互证有用，已启用并润色。
13. **激活被注释的 "Even with Γ=900, the range is 1.2–2.2 MeV" 句**：使 Γ=300 与估计范围 500–900 之间的论证链条完整（共振能量反过来把 Γ 定在 ~300 附近）。
14. **病句重写**："If the resonant deuterium absorption almost fix the Lorentz factor being around 300, we choose Γ=10^2.5…" → "If the gap indeed arises from resonant deuterium absorption, the resonance energy in turn almost fixes the Lorentz factor to be around 300; we therefore choose Γ = 10^2.5 as a typical value in the following."

### B. 术语与表述

15. **"high-enthalpy winds" → "high-entropy winds"**：v2 原文为 high-entropy（标准术语，中微子驱动高熵风/火球），v3 改成了 enthalpy，疑为笔误。**如是有意改动请告知并改回。**
16. "outflow ejected from a merger" → "ejected from the central engine"（正文已采用 z=2.34/collapsar 基线，核合成段不宜再限定 merger）。
17. 前身星句子重写："Arguments from previous work … are presented." → "The unusual stellar progenitor of GRB 210704A has been debated in previous work…"；"by confirming Ly α absorption from line-stacking analysis with afterglow spectrum" → "by confirming Ly-α absorption through a line-stacking analysis of the afterglow spectrum"。
18. r-process 排版统一为 $r$-process（摘要 3 处、引言 1 处）；"binary neutron stars (BNS) mergers" → "binary neutron star (BNS) mergers"；"rapid neutron capture process" → "rapid neutron-capture process"。
19. "Lorentz Factor" → "Lorentz factor"（多处）；"up to Lanthanides" → "lanthanides"。
20. "0.1 s is too short…" 句首数字 → "a timescale of ∼0.1 s is far too short…"。
21. gtlike 脚注整理：弯引号 "FileFunction" → ``FileFunction''；文字破折号 "–log(likelihood)" → 数学 $-\log(\rm likelihood)$；"+/-0.5" → $\pm0.5$；"a parameter scanning is performed for each parameter (index of power-law) and extract…" 语法理顺；正文 ΔBIC 公式排版规范化。
22. ``zone of avoidance" 右引号补全为 ''。
23. Q_s = Q/10^s 量纲约定从 n′_p 公式处前移到首次使用处（半径公式），原处删除重复说明。
24. 结论段："Interpreting this as … for the first time" 语序调整；"nucleosynthesis ingredients in the r-process" → "the ingredients of $r$-process nucleosynthesis"；"create conditions" → "creates the conditions"（并把两句衔接改顺）。
25. 其他语法/格式："freely escaped" → "escape freely"；"with assuming local electrical neutrality" → "assuming local electric neutrality"；"the key point is… second…" → "the first key point is… second…"；"resonant regions" → "resonant region"；"Ref.~\citep[][]" → \citep[see…in][]；"(e.g., see Refs.~\citep…)" → \citep[e.g.,][]；"consist the upper envelope" → "constitute the upper boundary"；"is consistent well" → "is well consistent"；时间延迟句语序（(1+z)R_ph/(2cΓ²) 加括号并前置说明对象）；"integrating the intensity over the emitting~\citep" 缺词 → "over the emitting surface"；"Therefore,this approach is extended  based" 空格；"correltions"、"The ranges of Γ is"、"Eq~(" → "Eq.~("、"change on BIC" → "change in BIC"、"χ² to the degree of freedom" → "χ² over the degrees of freedom"、log10(E_p)=…keV → $\log_{10}(E_p/{\rm keV})$、"spearman" → "Spearman"、FIG.\ref → FIG.~\ref、附录小节标题大小写与介词等。
26. 地址/机构："Luoyu road" → "Luoyu Road"；"Institute of high-energy Physics" → "Institute of High Energy Physics"。

### C. 编译验证

- `pdflatex + bibtex + pdflatex ×2`：**通过**，无错误、无未定义引用/引文、无重复标签警告（修改前有 1 处 multiply-defined 警告）。共 7 页。
- 需要的宏包：环境中补装了 fontawesome（texlive-fonts-extra）才能编译，供本地复现参考。
- `diff.tex`（查看 v2→v3 已做修改）已用 `pdflatex -shell-escape` 编译为 diff.pdf（9 页；latexdiff 对个别公式标记有少量可恢复报错，不影响阅读）。

### D. 需作者决策 / 未处理

- **response.docx 与本论文不符**：其内容是另一篇论文（AAS73042，jet-break 论文，Xin/Yi/Zou 致 ApJ）的回复信，**未做改动**。本轮修改的审稿人-facing 英文说明另存 `response_additions.docx`，供并入本文真正的回复信；如需我按真实审稿意见逐条撰写回复，请提供该报告。
- A7 的统计关系小节：补全还是删除，请定；若补全需向 LIV.bib 添加 Liang 2010 / Lü 2012。
- B15 的 entropy/enthalpy 请确认。
- τ_γD ≈ 1.4 Y_D L_K,55 R₁₂⁻¹ Γ₂.₅⁻³ 在 Y_D=0.3、R≈2×10¹² cm、Γ=300 下约为 0.25–0.5，正文靠 "L_K for each pulse is even larger" 支撑 τ_γD ≳ 1，论证略紧，审稿人可能追问，可考虑再加一句定量说明。
- v3 中 \iffalse 的 "Note added"（FBOT 再增亮与中子衰变时间膨胀）未启用，如需请告知。

## 第二部分：LIV_v2.tex（AASTeX/ApJ 版，此前一轮所做，保留备用）

该文件按同一修订方向完成了"双红移假设"改写与自审修正，主要包括：启用双起源摘要/引言/红移段（原文注释保留）、修正 z=2.43 笔误、补 gtlike 佐证段、时标论证改为 R/(Γc)~0.1 s（半径公式含 (1+z) 并前移）、σ_γD 更新为 2.5×10⁻²⁷ cm²@4.48 MeV（τ_γD 系数 1.1→1.3，**请核对**）、γγ 排除论证补强、α 散裂补充、E_K 单位 erg s⁻¹→erg、图 1(b)→图 2(b) 交叉引用修正、重复标签修复、作者名 Wei-Tina→Wei-Tian、UAT 关键词 639→629、大量语法/拼写修正（Thompson→Thomson、envelop→envelope 等）。
全部修改见 `LIV_v2_changes.pdf`（latexdiff）。编译通过、无警告。
