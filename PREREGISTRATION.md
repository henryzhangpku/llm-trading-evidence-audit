# Pre-registration: an evidence audit of LLM trading papers

Written 2026-11-02, before any paper in the population was coded. Committed to git
before coding starts, so the commit hash timestamps this plan.

## Population (fixed)

There are 91 papers in the llm-trading-papers corpus at SHA `3922a878…` plus the
2026-11-02 harvest. A paper is in the population if its theme is one of 00–07, it is
an LLM agent or alpha-mining paper, or it reports a headline Sharpe ratio or annual
return, and its full text is available. The list is
`evidence-audit/population.json`. Papers added to the corpus later are not added
to this audit.

## Coding (per paper, each code backed by a verbatim quote from the text)

| Field | Values |
|---|---|
| test_months | length of the reported out-of-sample / test window, in months (null if not stated) |
| test_end | last month of the test window (YYYY-MM) |
| n_assets | number of tradable assets in the test |
| costs | none · stated flat rate · realistic (spread/impact/borrow modelled) |
| leakage | none · acknowledged only · test after model training cutoff · live/forward · chronologically consistent model |
| trials | none · mentioned · count reported · multiplicity-adjusted result (deflated Sharpe, reality check, FDR) |
| baseline_bh | reports a buy-and-hold or index baseline (y/n) |
| sharpe | headline Sharpe as the abstract or conclusion states it; flags: excess, gross/net |
| code | public code link (y/n) |
| llm_cutoff_before_test | whether the main LLM's training cutoff is known to precede the test window (y/n/unknown) |

## Hypotheses (directions fixed now)

- **H1 (trial counts):** fewer than 10% of papers report how many strategies or
  configurations were tried, and fewer than 5% report a multiplicity-adjusted
  result.
- **H2 (short windows):** the median test window is 12 months or less.
- **H3 (window vs Sharpe):** the headline Sharpe is negatively rank-correlated with
  test-window length. Spearman ρ < 0, one-sided p < 0.05, among papers that report
  both.
- **H4 (look-ahead):** among papers whose test window does not lie wholly after
  the main LLM's training cutoff, a majority do not address training leakage
  (leakage = none or acknowledged only).
- **H5 (costs):** papers that model costs report lower headline Sharpe than papers
  that do not. One-sided Mann–Whitney, p < 0.05.

Secondary, descriptive only: code-release rate, buy-and-hold baseline rate, and the
share of papers with live or forward evaluation.

## Rules

- **Every code has a quote.** A quote that is not a verbatim substring of the
  paper's extracted text is a coding error and is redone. This is checked by
  script.
- **Two passes.** Every paper gets a first pass. A second blind pass on a random
  20% gives agreement rates, which are reported.
- **No re-coding after results.** Once H1–H5 are computed, codes can change only to
  fix an error found by the quote check. Every change is logged.
- **Failed hypotheses are reported** as failed.
