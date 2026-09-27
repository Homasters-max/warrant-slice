# Tasks

## 1. Значение секунд

- [ ] 1.1 В `_finite_seconds` отклонять `int`, которое double не представляет точно (`seconds == value`, design D-1;
  `REQ-RL-001`, `UNK-RL-002`); проверка — тест pytest с токеном `SCN-RL-007` проходит
- [ ] 1.2 Обновить docstring `_finite_seconds` под правило «значения секунд»; проверка — тесты pytest с токенами
  `SCN-RL-004` и `SCN-RL-006` по-прежнему проходят

## 2. Проверка

- [ ] 2.1 Прогнать `warrant check rate-limiter-precision tests-passed` и `warrant verify rate-limiter-precision`;
  проверка — оба завершаются успешно
