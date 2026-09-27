# Tasks

## 1. Судья CI и kernel

- [ ] 1.1 `.github/workflows/warrant.yml`: тег `v0.8.0` в шаге установки CLI, `permissions` += `issues: read`; проверка —
  `git diff` называет только эти строки
- [ ] 1.2 `.warrant/warrant.json`: `kernel: "0.8"`; `warrant sync` CLI 0.8.0 — lock, схемы, сгенерированные файлы;
  проверка — `warrant validate` и `warrant sync --check` CLI 0.8.0 зелёные
- [ ] 1.3 До push impl-PR — `warrant ci` CLI 0.8.0 на локальном merge-коммите (design D-1); проверка — нарушений нет, кроме
  `ATTESTATION_REQUIRED` gates L1; иначе остановка

## 2. Процесс агента

- [ ] 2.1 `.warrant/local/rules/process.json`: blocking UNKNOWN и решение maintainer'а (`warrant unknown add | resolve`),
  вопрос реализации — `I-N`, путь waiver `spec-approved`, `MERGED` без `--by`, кроме требования `warrant`; `warrant sync`
  перегенерирует `AGENTS.md` и `CLAUDE.md`; проверка — `warrant sync --check` зелёный; `AGENTS.md` содержит
  `warrant unknown add`, `--as decision`, `#issuecomment-`, `#pullrequestreview-`, `warrant waive`, `--activate`, а `--by`
  у `MERGED` — только с условием gate `human-approval`

## 3. Проверка

- [ ] 3.1 `warrant check pin-v0-8-0 tests-passed` и `warrant verify pin-v0-8-0` CLI 0.8.0; проверка — оба завершаются
  успешно
