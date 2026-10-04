# Assignment 2 Runbook: run these in order

Project files (src/*.py, params.yaml, dvc.yaml, .gitignore, README.md) are in `fashion-ann-pipeline/`.
**Take a screenshot after every command marked 📸.** Never squash commits.

## Setup
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r fashion-ann-pipeline/requirements.txt
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
Create an empty GitHub repo `fashion-ann-pipeline` (no README).

## Part A: Git
**A1**
```bash
mkdir fashion-ann-pipeline-work && cd fashion-ann-pipeline-work   # your working repo
cp ../fashion-ann-pipeline/{README.md,.gitignore,requirements.txt} .
git init -b main
git add . && git commit -m "Initial commit: README, .gitignore, requirements"
git remote add origin https://github.com/<you>/fashion-ann-pipeline.git
git push -u origin main
```
**A2**: all of B–D on `dev`, one commit per file:
```bash
git checkout -b dev
mkdir src
cp ../fashion-ann-pipeline/src/prepare.py src/    && git add src/prepare.py    && git commit -m "Add prepare.py"
cp ../fashion-ann-pipeline/src/preprocess.py src/ && git add src/preprocess.py && git commit -m "Add preprocess.py"
cp ../fashion-ann-pipeline/src/train.py src/      && git add src/train.py      && git commit -m "Add train.py"
# evaluate.py goes to the repo ROOT for now (used in A8 for git mv)
cp ../fashion-ann-pipeline/src/evaluate.py ./evaluate.py && git add evaluate.py && git commit -m "Add evaluate.py (root, to be moved)"
cp ../fashion-ann-pipeline/params.yaml . && git add params.yaml && git commit -m "Add params.yaml"
echo "scratch" > scratch_notes.txt && git add scratch_notes.txt && git commit -m "Add scratch notes"
```
**A8** (git mv / git rm):
```bash
git mv evaluate.py src/evaluate.py && git commit -m "Move evaluate.py into src/"
git rm scratch_notes.txt && git commit -m "Remove obsolete scratch file"
```
**A3** 📸
```bash
git log --oneline --graph --all
git log --stat -3
git log -p -1
git log main..dev
```
**A4** 📸
```bash
echo "# tweak" >> src/train.py && git diff          # (a) unstaged
git add src/train.py && git diff --staged           # (b) staged
git commit -m "Add comment to train.py"
git diff main..dev ; git diff main...dev            # (c)
```
**A5** stash 📸
```bash
echo "# wip" >> src/preprocess.py
git stash
git checkout main && git checkout dev
git stash list
git stash pop
git checkout src/preprocess.py     # discard the wip line afterwards
```
**A6** rebase 📸 (make a conflict on purpose: edit README line 1 on both hotfix and dev)
```bash
git checkout dev && echo "dev edit" >> README.md && git commit -am "README edit on dev"
git checkout main && git checkout -b hotfix
sed -i '1s/.*/# fashion-ann-pipeline (fixed typo)/' README.md
git commit -am "Hotfix: README title" && git checkout main && git merge hotfix
git log --oneline --graph --all                   # BEFORE
git checkout dev && git rebase main
#   conflict in README.md -> edit file, remove <<<< ==== >>>> markers
git add README.md && git rebase --continue
git log --oneline --graph --all                   # AFTER
```
**A7** reset 📸
```bash
git checkout -b scratch
echo a > a.txt && git add a.txt && git commit -m "throwaway 1"
echo b > b.txt && git add b.txt && git commit -m "throwaway 2"
git reset --soft HEAD~1 && git status             # b.txt staged, still on disk
git commit -m "throwaway 2 again"
git reset --hard HEAD~1 && git status ; ls        # b.txt gone completely
git checkout dev && git branch -D scratch
```

## Part C: DVC (on `dev`)
Do the GCP OAuth setup from your guide (Desktop app client, add yourself as **Test user**).
```bash
dvc init && git commit -m "Initialize DVC"
dvc remote add -d gdrive_storage gdrive://<FOLDER_ID>
dvc remote modify gdrive_storage gdrive_client_id <CLIENT_ID>
dvc remote modify gdrive_storage gdrive_client_secret <CLIENT_SECRET>
```
⚠ Client secret is written to `.dvc/config`. Put it in `.dvc/config.local` instead so it isn't pushed:
`dvc remote modify --local gdrive_storage gdrive_client_secret <CLIENT_SECRET>`
```bash
git add .dvc/config && git commit -m "Configure Google Drive remote"
# generate data so there is something to track (v1)
python src/prepare.py && python src/preprocess.py && python src/train.py && python src/evaluate.py
dvc push          # browser OAuth opens (C4); then:
git status        # confirm no credential file listed
dvc add data/raw data/processed models
git add data/raw.dvc data/processed.dvc models.dvc data/.gitignore .gitignore
git commit -m "Track data and models with DVC (v1 artifacts)"
dvc push          # 📸 then screenshot the Drive folder in your browser
```

## Part D: Pipeline
**Required fix:** `dvc.yaml` outputs overlap the `.dvc` files from C5, so remove those first:
```bash
dvc remove data/raw.dvc data/processed.dvc models.dvc
cp ../fashion-ann-pipeline/dvc.yaml .
git add -A && git commit -m "Replace .dvc files with dvc.yaml pipeline"
dvc repro                       # 📸 D3: all four stages run; dvc.lock created
git add dvc.lock metrics.json .gitignore && git commit -m "First pipeline run (v1 metrics)"
cp metrics.json metrics_v1.json                 # keep for the comparison table
```
**D4:** change `dense_units: 128` to `256` in params.yaml
```bash
dvc repro                       # 📸 
```
Expected: `prepare` and `preprocess` **skipped** (their scripts, inputs and `preprocess.*` params are unchanged, so hashes match dvc.lock). `train` and `evaluate` **rerun** (`train.dense_units` changed, and evaluate depends on the new `models/model.h5`).

**D5**
```bash
git add params.yaml dvc.yaml dvc.lock metrics.json
git commit -m "v2: dense_units=256" && git tag v2
dvc push
dvc metrics diff HEAD~1      # source for v1-vs-v2 table
```
Merge into main so v1 and v2 exist there: `git checkout main && git merge dev && git push origin main dev --tags`

## Part E: Conflicts
In `preprocess.py` the normalization line is `x_train = train["x"].astype("float32") / 255.0` (same for x_test).
```bash
# E1
git checkout main && git checkout -b teammate-sim
#   edit: x = (x - 0.5) / 0.5        (scale to [-1,1])  after the /255.0 lines
dvc repro preprocess && git add -A && git commit -m "teammate: [-1,1] normalization"
dvc push
# E2
git checkout main
#   edit: x = (x - mean) / std        (standardize with training mean/std)
dvc repro preprocess && git add -A && git commit -m "main: standardization"
dvc push
# E3 📸 both conflicts
git merge teammate-sim
```
**Heads-up:** because the stages are managed by `dvc.yaml`, the "two hashes" conflict shows up in **`dvc.lock`** (the `data/processed` md5), not a separate `.dvc` file. This is the same type of conflict. If your instructor insists on a `.dvc` pointer, say so in the report.
```bash
# E4: fix preprocess.py by hand (keep ONE reconciled approach, e.g. standardization)
git checkout --ours dvc.lock               # or --theirs; pick the authoritative side
git add src/preprocess.py dvc.lock
dvc checkout                               # sync working dir to resolved pointer
# E5
dvc status                                 # 📸 "Data and pipelines are up to date."
git commit -m "Merge teammate-sim: reconcile normalization"
dvc repro                                  # 📸 re-run from merged state
git add dvc.lock metrics.json && git commit -m "Re-run pipeline after merge"
git push origin main && dvc push
```
(If `dvc status` is not clean, run `dvc repro` first, then `dvc status`.)

## Submission checklist
- [ ] GitHub link, unsquashed history  - [ ] Drive folder shared with instructor
- [ ] `dvc.lock` committed at final state  - [ ] PDF report (use REPORT_TEMPLATE.md)
