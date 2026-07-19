# 本轮修改列表（内部，合作者审阅用）

> 主文件：`GRB210704A-kilonova_v3_songxy.tex`（PRD 版，LQ20255/Zou）。只列本轮（Claude 协助）新做的修改；v2→v3 已完成的修改不在此列（可编译 `diff.tex` 查看）。
> 本轮全部修改可在 **`GRB210704A-kilonova_v3_changes.pdf`**（latexdiff：修改前 vs 修改后，蓝=新增、红/小字=删除）逐处查看。
> 另：此前误将 LIV_v2.tex 当作主文件时也做了一轮修订（见文末第二部分），这些修改同样是真实的错误修正与润色，已保留，可按需取舍。

## 第一部分：GRB210704A-kilonova_v3_songxy.tex（主文件）

### 0. 按审稿意见落实的修改（收到正确的 response.docx 后）

对照两位审稿人意见与回复信草稿，发现回复信声称"已加入修改稿"的几处内容在 tex 中尚未落实，本轮补齐：

0.1 **多成分/替代解释的排除段写入正文**（Response 3 & 8 承诺"added in lines 82-102/93-99"，但 tex 中整段仍是注释）：在 E′_gap 公式之后、"Resonant Nuclide Absorption"之前新增一段，内容按回复信：(i) 内禀 γγ 吸收造成 sub-GeV 截止——τγγ≳1 在 R~10¹¹ cm 处要求 Γ≲170，远低于 500–900 的估计；(ii) 以 γγ 产生中心 ~1 GeV 的吸收特征需要 Γ≈3000；(iii) GeV 光子非外激波起源——Barniol Duran & Kumar (2011) 预言 GeV 相对 100 MeV 延迟 ~0.5 t_d，与观测同时到达矛盾，另引 Liu & Wang 2011、He et al. 2011、Maxham et al. 2011，并指出 GeV 与 sub-GeV 包络的相关性难以用外激波解释；(iv) 双成分喷流与 KN 压低不能产生带流量恢复的缺口。段末接"Therefore, we turn to photon-matter interactions."。旧的矛盾注释块（Γ<2000@10¹² 等旧数字）已删除。**注意：γγ 的具体数字（170/3000）取自回复信 Response (3)，但 Response (4) 明言 Γ 估计正在重做，tex 中已留 TODO 注释，请最终定稿时核定。**

0.2 **gtlike 数值写入脚注**（Referee B 要求"报告参数"）：连续 PL：−log(likelihood)=39.18、index=1.73±0.13；带缺口 [0.64, 1.17] GeV 的 PL：−log(likelihood)=34.53、index=1.70(+0.13/−0.12)；并注明该无 bin 似然比较下 ΔAIC=ΔBIC。原脚注中的"0.6 to 1.2 GeV"按回复信改为 [0.64, 1.17] GeV。

0.3 **新增"为何不用 gabs 线型拟合"脚注**（Referee B 问"Have the authors tried fitting e.g. a line profile?"）：缺口附近统计量不足、线参数无法约束（过拟合），且缺口中心能量随时间变化，需时间分辨分析——内容取自 Response (2)/(5)。

0.4 **恢复被 \iffalse 关闭的附录小节"Estimate of the lower limit of Γ with the photon with the highest energy"**（Response 4 称"These details are added in the Appendix C"，且正文 Γ≳500 的说法此前无任何推导支撑）：恢复 4 个公式；修正 R_γγ 公式中 (1+z) 应在分母（原文误乘）；f(E) 归一化单位 cm⁻¹ → cm⁻²；补结论句：16.09 GeV 光子的 τγγ<1 在 R~10¹¹ cm 给出 Γ≳500，且该方法 Γ∝(1+z)，共动能量几乎不受红移选择影响。**小节开头留 TODO：Response (4) 中"one-zone model/compactness 下限有问题、正在整体重做"的部分尚未写完，最终数字请团队核定。**

0.5 **附录解释部分补齐**（Response 1 & 7）：解释 1) 补 CCF 时滞检验括注（<20 keV 与 50–100 keV 相关，时滞 ≈0）；解释 2) 补 SSC 情形的电子洛伦兹因子论证（γ_e,p≳10^3.5 → R~10¹⁴ cm → τγD≪1，与本方案矛盾）；结论处补"MeV 峰成分的辐射机制几乎不影响计算与结论"（L_γ,keV-GeV=1.0e54 erg/s ≈ 2.6×L_γ,peak，L_K 由前者估计）。

0.6 **response.docx**：末尾空置的 "We also made other modifications." 一节已填入 (a)–(e) 五段英文说明（对应上述 0.1–0.5 及第 A/B 节的错误修正）。注意：回复信中 **Response (4) 的"In current modified version:"仍为空、句子在"It is always"处中断**，需要作者补写；文末孤立的"While"疑为残句，未动。

## 第一部分（续）

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

### E. 双区（two-zone）洛伦兹因子致密性计算（新增，按邹老师指示）

按"GeV 与 MeV 来自不同内激波（GeV 更靠外）"的双区模型，用致密性问题计算了两个区的洛伦兹因子下限：

- **方法**：遵循 Zou, Fan & Piran (2011, ApJ 726, L2) 框架 + Gao & Zou (2023, ApJL 956, L38) 的修正（该文 T 区 = 本文 GeV 区）。因本暴 MeV 峰成分低能指数极硬（α=−0.06），式 (17) 中"方括号取 1"的近似失效，故不直接套式 (17)，而是**数值积分**光学深度（精确 γγ 截面、精确阈值、实测 BAND 谱），物理与式 (16)(17) 完全一致。代码：`twozone_gamma_min.py`（已用 2011 文表 1 验证：080916C 得 187 vs 文中 193；其余 3 个暴在因子 ≲2 内，差异源于其全模型的角度平均与已被 2023 文修正的归一化）。
- **结果**（16.09 GeV 光子，t=0.96 s，z=2.34，MeV 靶场 = BAND 峰成分 L=3.7e53）：
  - Γ_G,min ≈ **312**（η=1，R_G≈1.7×10¹⁵ cm）；η=0.01 → 566；η=0.001 → 744。靶场加入 PL 成分的 MeV 段后各升高 10–20%（342/666/875）。
  - τ(Γ_G=300)=1 要求 **R_G ≈ 2.1×10¹⁵ cm**（BAND 靶）/ 3.7×10¹⁵（BAND+PL 靶）。
  - 缺口上边界的恢复光子：1.21 GeV 只需 Γ_G ≳ 165；4.39 GeV 需 ≳ 209。
  - 内区 Γ_M 的双区在轴约束（2011 文式 15 的几何）在 R_G~2e15 时**极弱**（Γ_M,min ~ O(1)）；Γ_M 的实际下限来自其自身 ~0.6 GeV 光子的逃逸。
- **写入位置**：Appendix C 新增小节 "Two-zone constraints on the Lorentz factors"（在"Estimate of the lower limit of Γ..."之后）；response.docx 的 Response (4) 空置的 "In current modified version:" 处已填入对应英文说明；Gao & Zou (2023) 条目已加入 LIV.bib。
- **⚠️ 关键自洽性问题（需邹老师决断，tex 中留有 TODO）**：Γ_G≈300 只有在 **R_G ≳ 2×10¹⁵ cm** 时才被允许；而正文 Discussion 中氘光解 τ_γD~1 的估计用的是 R≈2×10¹² cm（1 ms 变率）。二者相差 3 个量级——**在双区图像下，氘共振吸收只能发生在内区**（内区 Γ_M≈300、R_M≈2×10¹² cm，正文所有 τ_γD、τ_KN 数值天然归属内区），而外区（R_G≳2e15）只负责发出 ≥1.21 GeV 的恢复光子（该处 τ_γD 可忽略，故不被氘吸收，与观测一致）。这个分工其实让整个图像更自洽，但正文 "If the gap indeed arises from resonant deuterium absorption... fixes the Lorentz factor"（指 GeV 区）与 Comoving Frame Energetics 的表述需要相应改为指内区 Γ_M；被吸收的 [0.62,1.21] GeV 光子及 sub-GeV 包络应明确归属内区。请确认后我再统一改正文。
- 另：若 GeV 区半径改用毫秒变率（η~10⁻³，R_G~10¹³），则 Γ_G,min≈740–880，与 Γ≈300 不相容——η 的取值等价于确定外区半径，请确认 η≈1（对应约 1 s 的抛射间隔）符合你的设想。

### D. 需作者决策 / 未处理

- **Response (4) 未写完**：回复信中关于 Γ 估计的关键段落在 "The key problem of such estimate is the one-zone model. The lower limit given by compactness problem should never output a reasonable value. It is always" 处中断，"In current modified version:" 一节为空，"We also modified it totally…" 是占位。这是物理层面的未定项，只能由作者补写；tex 中相关位置（正文替代解释段、附录 Γ 下限小节）均已留 TODO 注释。回复信中若干占位图（resid 分布、似然扫描图）也需作者插入。
- **数值差异待核**：Response (1) 说峰成分低能光子指数约 −0.06，Response (5) 与 tex 均写约 −0.1（附录 BAND+PL 参数表中 α=−0.06）；L_γ,peak 在回复信中一处 3.7e53、一处 4e53。请统一。
- A7 的统计关系小节：补全还是删除，请定；若补全需向 LIV.bib 添加 Liang 2010 / Lü 2012。
- B15 的 entropy/enthalpy 请确认（本轮已按标准术语改回 high-entropy）。
- τ_γD ≈ 1.4 Y_D L_K,55 R₁₂⁻¹ Γ₂.₅⁻³ 在 Y_D=0.3、R≈2×10¹² cm、Γ=300 下约为 0.25–0.5，正文靠 "L_K for each pulse is even larger" 支撑 τ_γD ≳ 1，论证略紧，审稿人可能追问，可考虑再加一句定量说明。
- v3 中 \iffalse 的 "Note added"（FBOT 再增亮与中子衰变时间膨胀）未启用，如需请告知。
- `response_additions.docx` 已删除（其内容并入 response.docx 的 "We also made other modifications." 一节）。

## 第二部分：LIV_v2.tex（AASTeX/ApJ 版，此前一轮所做，保留备用）

该文件按同一修订方向完成了"双红移假设"改写与自审修正，主要包括：启用双起源摘要/引言/红移段（原文注释保留）、修正 z=2.43 笔误、补 gtlike 佐证段、时标论证改为 R/(Γc)~0.1 s（半径公式含 (1+z) 并前移）、σ_γD 更新为 2.5×10⁻²⁷ cm²@4.48 MeV（τ_γD 系数 1.1→1.3，**请核对**）、γγ 排除论证补强、α 散裂补充、E_K 单位 erg s⁻¹→erg、图 1(b)→图 2(b) 交叉引用修正、重复标签修复、作者名 Wei-Tina→Wei-Tian、UAT 关键词 639→629、大量语法/拼写修正（Thompson→Thomson、envelop→envelope 等）。
全部修改见 `LIV_v2_changes.pdf`（latexdiff）。编译通过、无警告。
