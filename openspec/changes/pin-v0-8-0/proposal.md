# Proposal

## Why

Судья CI проекта — CLI WARRANT, закреплённый тегом в `.github/workflows/warrant.yml` (`v0.7.0`). В `v0.8.0` (Change
`slice-fixes` фабрики, ADR-0040) появились команда `warrant unknown add | resolve` с проверкой решения maintainer'а в
`warrant ci`, правка spec в Run `implement` по пути waiver и `MERGED` без обязательного `--by`. Без перехода на `v0.8.0`
второй Change проекта (`rate-limiter-precision`) не может записать blocking UNKNOWN и не проверит путь waiver. Pin-Change
проводит агент сессии фабрики по решению maintainer'а (ADR-0041): агент проекта под guard не пишет policy-пути.

## What Changes

- Судья CI — тег `v0.8.0` в `.github/workflows/warrant.yml`; права job += `issues: read` (решение UNKNOWN — комментарий PR,
  ресурс issues API).
- `.warrant/warrant.json`: `kernel: "0.8"`; lock, копии схем и сгенерированные файлы — `warrant sync` CLI 0.8.0. Диапазон
  pack `core-sdd` `^0.3.3` уже покрывает `0.3.4`.
- Текст процесса агента `.warrant/local/rules/process.json` (и сгенерированные из него `AGENTS.md`, `CLAUDE.md`):
  - blocking UNKNOWN в spec-PR — `warrant unknown add --blocking`, ожидание решения maintainer'а комментарием в spec-PR,
    `warrant unknown resolve --as decision --ref`;
  - вопрос реализации — строка `I-N` в `design.md`; правка spec после approval — в Run `implement` строка `I-N` и правка
    delta spec, waiver `spec-approved` через `warrant waive`, активирует maintainer;
  - `transition MERGED` — без `--by`, кроме случая, когда `warrant` требует его (gate `human-approval` на переходе).

## Capabilities

### New Capabilities

Нет.

### Modified Capabilities

Нет: поведение библиотеки не меняется, меняются судья CI и процесс проекта (`skip_specs: true`).

## Impact

- Policy-пути проекта: `.github/workflows/warrant.yml`, `.warrant/warrant.json`, `.warrant/warrant.lock.json`,
  `.warrant/schemas/**`, `.warrant/local/rules/process.json`; сгенерированные `AGENTS.md`, `CLAUDE.md`, файлы frontend.
- Код `src/` и тесты `tests/` не меняются.
- **BREAKING** для локальной работы: CLI 0.7 на проекте с lock kernel 0.8 — `LOCK_MISMATCH`; установить `v0.8.0`
  (`npm pack github:Homasters-max/SRA#v0.8.0` → `npm i -g ./<tgz>`).

## Non-goals

- Изменение guard агента проекта: операции записи для `.warrant/local/**` и `.github/workflows/**` нет (ADR-0040, BL-56).
- Второй Change проекта `rate-limiter-precision` — отдельно, после этого.
