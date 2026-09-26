# warrant-slice

Sample-проект vertical slice MVP [WARRANT](https://github.com/Homasters-max/SRA)
([ADR-0039](https://github.com/Homasters-max/SRA/blob/main/docs/adr/WARRANT-ADR-0039-vertical-slice.md)): библиотека
`rate_limiter` на Python + pytest, каждое изменение — Change OpenSpec под `warrant` (процесс — `AGENTS.md`).

- CLI: `warrant` той же версии, что pin в `.github/workflows/warrant.yml`; OpenSpec 1.13.1.
- Тесты: `python -m pytest` (check `tests-passed` — `.warrant/local/checks/`).
- Сессия агента — Claude Code в корне репозитория: hooks `warrant guard` из `.claude/settings.json`.
