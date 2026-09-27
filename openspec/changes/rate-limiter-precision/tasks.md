# Tasks

## 1. Значение секунд

- [ ] 1.1 В `_finite_seconds` отклонять `int`, которое double не представляет точно (`seconds == value`, design D-1;
  `REQ-RL-001`, `UNK-RL-002`), и обновить её docstring под правило «значения секунд»; проверка — тест pytest с токеном
  `SCN-RL-007` проходит
- [ ] 1.2 Переписать тесты, закрепляющие прежнее прочтение с округлением (design D-2/D-3 Change rate-limiter; здесь — design D-2): из
  `test_scn_rl_004_window_in_float_range_accepted` убрать W = 2^53 + 1 (он переходит в `SCN-RL-007` как `ValueError`);
  `test_scn_rl_006_clock_value_float_reading` переписать так, чтобы значение источника 2^53 + 1 давало `ValueError` без
  изменения состояния, а точно представимые значения за 2^53 принимались; убрать комментарий о прочтении design D-2/D-3
  Change rate-limiter; проверка — тесты pytest с токенами `SCN-RL-004`, `SCN-RL-006` и `SCN-RL-007` проходят, ни один тест
  не ожидает, что 2^53 + 1 принимается как W или значение источника

## 2. Проверка

- [ ] 2.1 Прогнать `warrant check rate-limiter-precision tests-passed` и `warrant verify rate-limiter-precision`;
  проверка — оба завершаются успешно
