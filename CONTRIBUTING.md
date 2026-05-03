# Contributing to Dift

Thanks for your interest in contributing to Dift.

We welcome thoughtful contributions that improve the project for real users.

## Our Goal

Dift is an open-source tool for comparing datasets and building trust in data changes.

We value contributions that improve usability, reliability, performance, documentation clarity, test coverage, and developer experience.

## Ways to Contribute

### Code
- Bug fixes
- New comparison features
- Performance improvements
- File format support
- Better CLI UX
- Better reports

### Documentation
- Improve README clarity
- Add examples
- Improve installation guides
- Fix incorrect docs

### Quality
- Add tests
- Improve CI workflows
- Refactor maintainable code

---

## How to Contribute to Dift

- Fork the repository
- Clone your fork
- Create a new branch
- Set up the project (venv + install)
- Make your changes
- Test your changes (pytest, ruff)
- Commit your work
- Push to your fork
- Open a Pull Request

---

## Keep Your Branch Up-to-Date

Before opening a Pull Request, make sure your branch is up-to-date with the latest version of `main`.

This helps prevent merge conflicts and ensures your changes work with the current codebase.

```bash
git checkout main
git pull upstream main

git checkout your-branch
git rebase upstream/main