# Deviations and corrections

Every change made after coding began, in order.

1. **Before results: two coding fixes for consistency** (`corrections_pre_results.jsonl`).
   - 2605.05580 leakage changed from live to acknowledged. The rubric codes the main
     experiment, which is a backtest the paper says may overlap the training data;
     the live phase is a separate experiment.
   - 2605.12532 test_months changed from 0 to 0.5. Any window shorter than two weeks
     is coded 0.5, as for 2604.14199.
2. **After the first run: H4 implementation fixed to match the pre-registration.**
   The script selected the H4 subset by its leakage code, which made the share
   1.0 by construction. The pre-registration defines the subset by the training
   cutoff (`llm_cutoff_before_test` not "y"). The script now uses that. No codes
   changed. The first run's output is kept in `results_run1.json`.
