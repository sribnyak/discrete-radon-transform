# Discrete Radon Transform for Line Detection

1. В файле `dradon.py` реализован алгоритм дискретного преобразования Радона для распознавания прямых. Пример использования - в файле `example_usage.py`.
2. В файле dradon_tests.py реализованы тесты для dradon.py. В тесте генерируются случайные картинки с прямыми в случайном количестве. Прямые трех типов (горизонтальные, вертикальные и диагональные) и для каждого из типов смотрится как хорошо алгоритм находит прямые на изображениях разного размера. Получается, что горизонтальные прямые алгоритм всегда находит правильно, диагональные иногда угадывает, в вертикальных всегда ошибается.

