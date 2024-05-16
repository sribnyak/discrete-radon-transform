# Discrete Radon Transform for Line Detection

Запуск скрипта: `poetry run dradon --radon_img temp/radon.png --lines_img temp/lines.png examples/geometry_test.png`

Запуск тестов и пр. `nox -r`

Запуск отдельной сессии `nox`: `nox -rs black`

Run hooks: `pre-commit run --all-files`

---

В файле `src/dradon/core.py` реализован алгоритм дискретного преобразования Радона для распознавания прямых. Пример использования - в файле `example_usage.py`.

В файле `tests/test_core.py` реализованы тесты для dradon.py. В тесте генерируются случайные картинки с прямыми в случайном количестве. Прямые трех типов (горизонтальные, вертикальные и диагональные) и для каждого из типов смотрится как хорошо алгоритм находит прямые на изображениях разного размера. Получается, что горизонтальные прямые алгоритм всегда находит правильно, диагональные иногда угадывает, в вертикальных всегда ошибается.
