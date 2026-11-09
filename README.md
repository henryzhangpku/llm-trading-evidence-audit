# A pre-registered evidence audit of 91 LLM trading papers

Data, code and paper for **"Short Windows, Unmodelled Costs, Unknown Cutoffs: A
Pre-Registered Evidence Audit of 91 LLM Trading Papers"** by Henry Zhang
([`main.pdf`](main.pdf)).

Papers on LLM trading agents and alpha mining report Sharpe ratios that would
be remarkable anywhere else in empirical finance. This audit codes the evidence
behind them: the length of the test window, whether trading costs are deducted,
whether the test can overlap the model's training data, and whether the size of
the search is reported. Of the 75 papers with a trading test, 51% deduct no
costs, and the median test window is 12 months.

## What is here

| File | What it is |
|---|---|
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | Population rule, coding fields and hypotheses H1–H5, written before any paper was coded |
| [`population.json`](population.json) | The 91 paper IDs, fixed before coding |
| [`papers.jsonl`](papers.jsonl) | Title, year and link for each paper in the population |
| [`RUBRIC.md`](RUBRIC.md) | The coding rubric |
| [`codes.jsonl`](codes.jsonl) | One coded record per paper. Every code carries the verbatim quote it rests on |
| [`codes_second_pass.jsonl`](codes_second_pass.jsonl) | The blind second pass on a random 18 papers |
| [`corrections_pre_results.jsonl`](corrections_pre_results.jsonl) | The two coding fixes made before results were read |
| [`DEVIATIONS.md`](DEVIATIONS.md) | Every change made after coding began |
| [`analyze.py`](analyze.py) | Quote check, coder agreement and the pre-registered tests. Every number in the paper comes from it |
| `results.json`, `results_dedup.json`, `results_run1.json` | Script output. `results_run1.json` is the first run, kept after the H4 fix described in `DEVIATIONS.md` |
| `main.tex`, `author-note.tex`, `main.pdf` | The paper |

## History

The audit was run in a private working repository. The first four commits here
replay its commits with their original dates. They show the pre-registration
and population (2 Nov 2026, 11:31 PST) and the rubric and script (11:33)
committed before the codes (11:45). The commit hashes differ from the working
repository's. The last commit adds the paper and the files as they stand at
release.

The coders were language models, as the paper says (Design and Limitations sections). That is why
coding took minutes. The quote check is what makes the codes trustworthy: every
quote must appear verbatim in the paper's text, and none failed.

The working repository's commit hashes, referred to in `PREREGISTRATION.md` and
`DEVIATIONS.md`, are not public. The paper corpus is the author's private index
of LLM trading research. The population and every record needed to check the
counts are here.

## Reproducing

```bash
python3 analyze.py codes.jsonl codes_second_pass.jsonl
```

The tests and agreement figures need only the files here; without a corpus the
quote check is reported as skipped. The quote check needs each paper's full text, which is not redistributed. To run it, download
the papers from the links in `papers.jsonl`, extract their text, and put it in
a folder laid out as `papers.jsonl` describes (`text_path`). Then point the
script at that folder:

```bash
EVIDENCE_AUDIT_CORPUS=/path/to/corpus python3 analyze.py codes.jsonl codes_second_pass.jsonl
```

Text extraction differs between tools, so a handful of quotes may need
whitespace or ligature normalization to match.

## Licence

[CC BY 4.0](LICENSE). The quotes in `codes.jsonl` are short excerpts from the
audited papers, used for criticism and review. Copyright in them stays with
their authors.

Research only. This is a study of published research, not investment advice.
