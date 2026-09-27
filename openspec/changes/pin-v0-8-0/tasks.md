# Tasks

## 1. Судья CI и kernel

- [x] 1.1 `.github/workflows/warrant.yml`: тег `v0.8.0` в шаге установки CLI, `permissions` += `issues: read`; проверка —
  `git diff` называет только эти строки
- [x] 1.2 `.warrant/warrant.json`: `kernel: "0.8"`; `warrant sync` CLI 0.8.0 — lock, схемы, сгенерированные файлы;
  проверка — `warrant validate` и `warrant sync --check` CLI 0.8.0 зелёные

## 2. Процесс агента

- [x] 2.1 `.warrant/local/rules/process.json`: blocking UNKNOWN и решение maintainer'а (`warrant unknown add | resolve`),
  вопрос реализации — `I-N`, путь waiver `spec-approved`, `MERGED` без `--by`, кроме требования `warrant`; `warrant sync`
  перегенерирует `AGENTS.md` и `CLAUDE.md`; проверка — `warrant sync --check` зелёный; `AGENTS.md` содержит
  `warrant unknown add`, `--as decision`, `#issuecomment-`, `#pullrequestreview-`, `#discussion_r` (как запрет),
  `roles.maintainer`, `PROPOSED` и `SPECIFIED` (состояния `unknown`), открытие spec-PR при blocking UNKNOWN,
  `warrant waive`, `--activate` — только maintainer'ом, а `--by` у `MERGED` — только с условием gate `human-approval`

## 3. Проверка

- [ ] 3.1 `warrant check pin-v0-8-0 tests-passed` и `warrant verify pin-v0-8-0` CLI 0.8.0; проверка — оба завершаются
  успешно
- [ ] 3.2 После коммита `VERIFYING`, до push — `warrant ci` CLI 0.8.0 на локальном merge-коммите (design D-1); проверка —
  код 1 только с `GATE_NOT_PASSED` gates L1 (`ATTESTATION_REQUIRED`) и `human-approval` в `deferred[]`; иначе остановка
