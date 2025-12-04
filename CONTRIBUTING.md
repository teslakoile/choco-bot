# Contributing to ChocoBot

We welcome contributions that improve the bot, its infrastructure, or the surrounding documentation. This guide outlines the workflow and expectations for making changes.

## Getting Started
- Review the existing [README](README.md) to understand the project purpose, setup steps, and how the bot is run.
- Open an issue for bugs or feature requests so discussion and alignment can happen before implementation.
- For questions or quick proposals, start a discussion on the issue tracker to gather feedback.

## Development Workflow
1. **Fork and branch**: Fork the repository and create a feature branch with a descriptive name (for example, `feature/youtube-pagination` or `fix/discord-timeout`).
2. **Set up the environment**: Create a virtual environment and install dependencies via `pip install -r requirements.txt`.
3. **Implement changes**: Keep commits focused and descriptive (conventional commits are welcome, e.g., `fix: resolve discord timeout`). Include tests or examples when applicable.
4. **Lint and sanity checks**: Install the hooks with `pip install pre-commit` (if you haven't already) and run `pre-commit run --all-files` to execute the configured formatters and linters. Ensure the bot still runs with `python bot.py` after your changes.
5. **Pull request**: Open a PR against the `main` branch. In the description, summarize the problem, the approach you took, and any follow-up work that may be needed.

## Code Guidelines
- Prefer clear, self-documenting code and meaningful variable names.
- Add or update docstrings and comments when behavior is not obvious.
- Keep configuration (tokens, IDs, secrets) outside the codebase; rely on environment variables where needed.
- Update documentation (including this file and the README) whenever you add new features or change behavior that affects users.

## Reporting Issues
When filing an issue, provide the following to help with triage:
- A concise description of the bug or feature request.
- Steps to reproduce, expected results, and actual results.
- Any relevant logs, error messages, or stack traces.
- Environment details such as Python version and OS, if applicable.

## Getting Help
If you are unsure about an approach or need guidance, feel free to open a draft issue or pull request. Early feedback helps keep efforts aligned and reduces rework.
