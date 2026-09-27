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
  - список команд, которые пишут record, += `unknown`;
  - UNKNOWN — только в `PROPOSED` и `SPECIFIED`: `warrant unknown add <change> --area <AREA> --text <вопрос> [--blocking]`;
    открытый blocking UNKNOWN — `warrant status` `WAIT` (next `clarify`): агент останавливается и ждёт решения
    maintainer'а;
  - решение — комментарий автора из `roles.maintainer` в spec-PR Change: issue comment `…/pull/<N>#issuecomment-<id>` или
    review `…/pull/<N>#pullrequestreview-<id>` (не комментарий к строке `#discussion_r…`), текст которого содержит id
    UNKNOWN; затем `warrant unknown resolve <change> <UNK> --as decision --text <ответ> --ref <URL комментария>`; автора,
    текст и PR проверяет `warrant ci`; не-blocking закрывается и `--as fact | assumption`; исправить до `APPROVED` —
    `--replace`;
  - вопрос реализации — строка `I-N` в `design.md` с решением maintainer'а, не `warrant unknown`;
  - правка spec после approval — только по решению maintainer'а: внутри Run `implement` строка `I-N` в `design.md` и
    правка delta spec (`proposal.md` вне `write_scope`); `warrant waive <change> spec-approved --reason "<I-N>: …"
    --risk … --control … --owner human:<maintainer> --expires …` создаёт waiver в `PROPOSED`; активирует maintainer —
    сам или словом в PR, по которому агент выполняет `warrant waive --activate <WAV> --by <maintainer>` и коммитит в
    ветку impl-PR до merge (без `ACTIVE` waiver job `warrant` красный: `GATE_NOT_PASSED` `spec-approved`);
  - `transition MERGED --ref <URL impl-PR>` — без `--by` (ADR-0040 п. 5), кроме Change, у которого effective policy
    ставит gate `human-approval` на `VERIFYING->MERGED` (risk `HIGH`): `warrant` отвечает `USAGE`, и `--by <maintainer>`
    передаётся (BL-74 фабрики).

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
