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

### D-2. Без spec

`skip_specs: true`: библиотека не меняется, а требования к процессу проекта держат текст правила и `warrant` фабрики.
Gate `required-artifacts-present` засчитывает `skipped` для `specs`. Отвергнуто: capability процесса с тестами pytest,
читающими конфигурацию, — дублирует проверки `warrant validate` и `sync --check`, и новая AREA требует правки
`.warrant/local/areas.json`, недоступной spec-PR.

### D-3. `--by` у `MERGED`

Правило процесса называет `--by <maintainer>` только для случая, когда `warrant transition` его требует: у Change с
`blast_radius: SYSTEM` (этот Change) effective policy может ставить gate `human-approval` на `VERIFYING->MERGED`, а у
`rate-limiter` его не было. `warrant` сам называет нехватку `--by` ошибкой `USAGE` (BL-74 фабрики).

### D-4. Классификация

`factory-change` (policy-пути в diff impl-PR), `blast_radius: SYSTEM` — floor pack для `.warrant/**`; остальные измерения —
как у безопасной правки конфигурации: откат — revert PR. `--propose` в spec-PR: diff spec-PR ещё не содержит policy-путей.

## Risks / Trade-offs

- [CLI 0.8 судит impl-PR, база которого на lock kernel 0.7] → `warrant ci` выводит требования из базы (ADR-0038); если
  CLI 0.8 откажет на lock базы — остановка и строка backlog фабрики, pin не обходится.
- [Агент правит policy-пути без guard] → ADR-0041: человеческие акты — одобрение и merge PR; diff impl-PR виден целиком.

## Migration Plan

1. spec-PR — артефакты, `classify`, review spec, `SPECIFIED` по слову maintainer'а.
2. impl-PR — D-1; вердикт — job `warrant` на `v0.8.0`.
3. archive-PR — `ci fetch`, `MERGED`, `archive`.
4. Откат — revert impl-PR: lock и схемы возвращаются к kernel 0.7.
