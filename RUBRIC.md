# Coding rubric (from the pre-registration; do not change it)

For each paper in your chunk file, read its full text at `text_path` (use grep/sed on
the file; read the abstract, experimental setup, results tables and conclusion).
Code the paper's MAIN reported trading/backtest experiment (the one in the abstract).

Output one JSON object per line to your output file, with these fields:

- id, title
- test_months: number. The length of the reported out-of-sample / test / backtest
  evaluation window in months (round to 0.5). null if the paper reports no trading test or doesn't state it.
- test_end: "YYYY-MM" last month of that window, or null
- n_assets: integer number of tradable assets in the main test, or null
- costs: "none" | "flat" (a stated fee/commission/bps rate) | "realistic" (spread, impact or borrow modelled from data) | "na" (no trading test)
- leakage: "none" | "acknowledged" (look-ahead/training leakage discussed but not controlled) | "post_cutoff" (test window stated to be after the LLM's training cutoff) | "live" (forward/live evaluation) | "chrono" (chronologically consistent model) | "na"
- trials: "none" | "mentioned" (multiple testing/data snooping discussed) | "count" (number of strategies/configs/runs tried is reported) | "adjusted" (deflated Sharpe, reality check, FDR or similar applied to a headline result)
- baseline_bh: true/false, a buy-and-hold or index baseline is reported
- sharpe: number or null, the headline Sharpe ratio of the proposed method as stated in abstract/conclusion (if several, the one the abstract highlights; if only per-asset, the best one shown in abstract or the average if the paper gives one)
- sharpe_flags: list from ["excess","gross","net","daily_unannualized","relative_improvement"], as applicable
- code: true/false, a public code repository link for the method
- llm: main LLM(s) used, short string
- llm_cutoff_before_test: "y" | "n" | "unknown"
- quotes: an object mapping EACH non-null field above (except id, title, llm, llm_cutoff_before_test) to a VERBATIM quote of 5-30 words copied exactly from the text file that supports the code. For a "none"/false code, quote is "" (absence). Copy quotes exactly as they appear in the text file (including odd spacing or hyphenation); a script will substring-check them against the text with whitespace collapsed.
- notes: one short sentence for anything ambiguous.

Rules: judge only from the paper text. Don't guess; use null/"unknown". Be strict:
"costs" is "none" unless the paper states costs are deducted in the main test.
"trials":"count" needs an actual number of strategies/configs/seeds tried for the reported result.
