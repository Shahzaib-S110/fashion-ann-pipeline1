# Assignment 2 Report: End-to-End ML Versioning (Name, Roll No.)
GitHub: <link> | Drive remote: <link or dvc push output>

## Part A: Git
Screenshots: A3 (4 log variants), A4 (diffs), A5 (stash list), A6 (graph before/after), A7 (reset), A8 (mv/rm).

**A3: what each variant adds over plain `git log`**
- `--oneline --graph --all`: compact one-line commits drawn as a branch/merge graph across all branches, not just the current one.
- `--stat -3`: files changed and insertions/deletions per commit, for the last 3 commits.
- `-p -1`: the full patch (line-by-line diff) of the latest commit.
- `main..dev`: only the commits reachable from dev but not from main, i.e. what dev adds.

**A4: two-dot vs three-dot**
`git diff main..dev` compares the tips of the two branches directly (includes changes made on main since dev branched, shown in reverse). `git diff main...dev` compares dev's tip against the common ancestor (merge base), showing only the changes dev introduced.

**A7: soft vs hard reset**
`--soft HEAD~1` moves HEAD back but keeps changes staged and on disk. `--hard HEAD~1` moves HEAD back and discards both index and working-tree changes. (Add what you observed.)

## Part B: Pipeline
Brief description of the four scripts; test accuracy: ____ (target ≥ 85%).

## Part C: DVC + Google Drive
Screenshots: `dvc push` output, Drive folder contents, `git status` showing no credentials committed.

## Part D: Pipeline
Final `params.yaml` and `dvc.yaml` (paste). D3 repro log (screenshot). D4 log (screenshot).

**Which stages reran?** `train` and `evaluate` reran; `prepare` and `preprocess` were skipped. DVC compares hashes of each stage's deps, params and cmd with dvc.lock. Changing `train.dense_units` only affects the train stage's params; evaluate reran because its dependency `models/model.h5` changed. The earlier stages' inputs were identical, so cached results were reused.

**v1 vs v2**
| Version | dense_units | test_loss | test_accuracy |
|---|---|---|---|
| v1 | 128 | | |
| v2 (tag v2) | 256 | | |

## Part E: Conflicts
Screenshots: E3 conflict markers in preprocess.py and in dvc.lock/.dvc pointer. Explain how you reconciled the code, which data version you chose and why, `dvc status` clean, final `dvc repro`.
