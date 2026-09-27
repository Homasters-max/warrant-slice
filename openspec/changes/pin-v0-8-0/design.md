# Design

## Context

Проект закреплён на CLI `v0.7.0`: тег в `.github/workflows/warrant.yml`, `kernel: "0.7"` в `.warrant/warrant.json`, lock
записан kernel `0.7.0`. Фабрика выпустила `v0.8.0` (ADR-0040): `warrant unknown`, проверка решения UNKNOWN в `warrant ci`
через комментарий PR, `write_scope` `implement` с `design.md` и `specs/**`, `MERGED` без `--by`. Pin-Change проводит агент
сессии фабрики по решению maintainer'а (ADR-0041), без guard проекта; человеческие акты — одобрение и merge каждого PR.

## Goals / Non-Goals

**Goals:**
- Судья CI и локальный CLI — `v0.8.0`; `warrant validate`, `sync --check` зелёные на kernel 0.8.
- Текст процесса агента исполним на `v0.8.0`: blocking UNKNOWN, путь waiver, `MERGED`.

**Non-Goals:** — proposal, Non-goals.

## Decisions

### D-1. Порядок в impl-PR

Первый коммит — переходы `APPROVED` и `IMPLEMENTING` CLI 0.7.0: lock базы — kernel 0.7, CLI 0.8 на нём даёт
`LOCK_MISMATCH` до `warrant sync`. Затем правка `warrant.json` и `warrant.yml`, `warrant sync` CLI 0.8.0 (lock, схемы,
сгенерированные файлы) и текст `process.json` с повторным `sync`. Последний коммит — `verify` и `VERIFYING` CLI 0.8.0.
Отвергнуто: `sync` до `APPROVED` — spec-PR не может трогать policy-пути.

Два CLI: глобальный `warrant` — 0.8.0; 0.7.0 — сборка тега в отдельном каталоге (`git worktree add --detach <dir> v0.7.0`
в репозитории фабрики, `npm ci`, `npm run build`, вызов `node <dir>/packages/cli/dist/bin/warrant.js`).

Проверка до push impl-PR: `warrant ci` 0.8.0 локально на merge-коммите, собранном как в job (`origin/main` + head ветки,
`git merge --no-ff`, `GITHUB_REPOSITORY` задан). Ожидаемый исход — нарушений нет, кроме `BLOCKED` gates L1 с
`ATTESTATION_REQUIRED` (evidence вне CI, код 1); `LOCK_MISMATCH`, `RECORD_MISMATCH`, `USAGE` или код 3 — отказ CLI 0.8 на
базе kernel 0.7. По коду фабрики этого не ждём: lock проверяет только `validate`, а pack `0.3.4`, которого нет в lock
базы, `warrant ci` принимает при `factory-change` в классификации (REQ-VER-011). Отказ — остановка: запасной путь —
исправление фабрики (`v0.8.1`) и повтор impl-PR этого же Change на новом теге.

### D-2. Без spec

`skip_specs: true`: библиотека не меняется, а требования к процессу проекта держат текст правила и `warrant` фабрики.
Gate `required-artifacts-present` засчитывает `skipped` для `specs`. Отвергнуто: capability процесса с тестами pytest,
читающими конфигурацию, — дублирует проверки `warrant validate` и `sync --check`, и новая AREA требует правки
`.warrant/local/areas.json`, недоступной spec-PR.

### D-3. `--by` у `MERGED`

Правило процесса называет `--by <maintainer>` только для случая, когда `warrant transition` его требует. Risk `HIGH`
(этот Change: `blast_radius: SYSTEM`) — overlay `risk-high` ставит gate `human-approval` на `VERIFYING->MERGED`, поэтому
`MERGED` этого Change — с `--by`; у `rate-limiter` (risk не `HIGH`) gate не было. `warrant` сам называет нехватку `--by`
ошибкой `USAGE` (BL-74 фабрики); ADR-0040 п. 5 («без `--by`») верен для Change без этого gate.

### D-4. Классификация

`factory-change` (policy-пути в diff impl-PR), `blast_radius: SYSTEM` — floor pack для `.warrant/**`, `compatibility:
BREAKING` — локальный CLI 0.7 на lock kernel 0.8 даёт `LOCK_MISMATCH`. `reversibility: EASY`: откат — такой же pin-Change
обратно на `v0.7.0` (PR, трогающий `.warrant/**` и `.github/workflows/**` без Change `factory-change`, отклоняется,
ADR-0038 п. 3), данных не теряет. `--propose` в spec-PR: diff spec-PR ещё не содержит policy-путей.

## Risks / Trade-offs

- [CLI 0.8 судит impl-PR, база которого на lock kernel 0.7] → `warrant ci` выводит требования из базы (ADR-0038); если
  CLI 0.8 откажет на lock базы — остановка и строка backlog фабрики, pin не обходится.
- [Агент правит policy-пути без guard] → ADR-0041: человеческие акты — одобрение и merge PR; diff impl-PR виден целиком.

## Migration Plan

1. spec-PR — артефакты, `classify`, review spec, `SPECIFIED` по слову maintainer'а.
2. impl-PR — D-1; вердикт — job `warrant` на `v0.8.0`.
3. archive-PR — `ci fetch`, `MERGED --ref <URL impl-PR> --by <maintainer>` (D-3), `archive`.
4. Откат — pin-Change обратно на `v0.7.0` (D-4).
