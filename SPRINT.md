# First Time Contributor Guide

This guide shows you how to make your **first contribution to Dift**.

You only need to follow these steps:

**Fork > Clone > Setup > Branch > Change > Test > Push > Pull Request**


## 1. Fork the Repository

Go to the Dift repository on GitHub and click **Fork**.

This creates your own copy of Dift.


## 2. Clone Your Fork

Copy the URL of **your fork**, then run:

```bash
git clone https://github.com/YOUR_USERNAME/Dift.git
cd Dift
```

Add the original Dift repository:

```bash
git remote add upstream https://github.com/ReginaldErzoah/Dift.git
```


## 3. Set Up Dift

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

**Windows Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

Install Dift:

```bash
pip install -e ".[dev]"
```

Check that it works:

```bash
dift --help
```


## 4. Create Your Branch

First make sure your `main` is up to date:

```bash
git checkout main
git fetch upstream
git pull upstream main
```

Create a branch for your issue:

```bash
git checkout -b my-issue
```

For example:

```bash
git checkout -b feat/chunk-processing
```


## 5. Make Your Changes

Open the files mentioned in the GitHub issue.

Make the required changes.

**Don't change unrelated files.**


## 6. Test Your Changes

First run the tests related to your change.

For example:

```bash
pytest tests/test_chunk_processing.py
```

Then run all tests:

```bash
pytest
```

Finally check the code:

```bash
ruff check .
```

Your goal is:

```text
All tests pass
ruff check . passes
```


## 7. Commit Your Changes

Check what you changed:

```bash
git status
```

Add your changes:

```bash
git add .
```

Commit:

```bash
git commit -m "feat: add chunk processing"
```

Examples:

```bash
git commit -m "fix: correct drift threshold"
```

```bash
git commit -m "test: add connector tests"
```

```bash
git commit -m "docs: update performance guide"
```


## 8. Push Your Branch

```bash
git push origin my-issue
```


## 9. Create Your Pull Request

Go to **your Dift fork on GitHub**.

GitHub should show:

**Compare & pull request**

Click it.

Make sure the Pull Request is going:

```text
from: YOUR_USERNAME/Dift
        
to: ReginaldErzoah/Dift - main
```

Explain briefly:

* What you changed
* Which issue it fixes
* How you tested it

If the issue number is `#25`, you can write:

```text
Closes #25
```


# If Your Branch Is Behind

Sometimes other contributors will update Dift while you are working.

If GitHub says your branch is **behind `main`**, run:

```bash
git fetch upstream
git rebase upstream/main
```

Then:

```bash
git push origin my-issue --force-with-lease
```


## If You Get a Conflict

Run:

```bash
git status
```

Open the file with the conflict and fix it.

Then:

```bash
git add .
git rebase --continue
```

When finished:

```bash
git push origin my-issue --force-with-lease
```

If you get stuck:

```bash
git rebase --abort
```

This cancels the rebase.


### Quick command reference

| Step              | Command                                                              |
| ----------------- | -------------------------------------------------------------------- |
| Clone             | `git clone https://github.com/YOUR_USERNAME/Dift.git`                |
| Enter Dift        | `cd Dift`                                                            |
| Add upstream      | `git remote add upstream https://github.com/ReginaldErzoah/Dift.git` |
| Install           | `pip install -e .[dev]`                                            |
| Create branch     | `git checkout -b my-issue`                                           |
| Test              | `pytest`                                                             |
| Lint              | `ruff check .`                                                       |
| Commit            | `git commit -m "type: description"`                                  |
| Push              | `git push origin my-issue`                                           |
| Rebase            | `git fetch upstream && git rebase upstream/main`                     |
