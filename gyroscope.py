import numpy as np


def form_row(raw_dim):
    """
    Данная функция составляет усреднённую строку со значениями, считанными с
    датчика, находящегося в одном из положений.
    :param raw_dim: Матрица Nx3, где N - количество измерений для одного
        положения датчика. Типом данных может быть Python list.
    :return: Возвращает <numpy.ndarray> 1x3 для данного положения датчика.
    """
    row = np.mean(raw_dim, axis=0)
    return row


def form_raw_data(rows_list):
    """
    Данная функция составляет матрицу сырых данных путём преобразования списка
    значений для каждого положения к матрице 6x3. Данную функцию необходимо
    использовать, когда rows_list содержит в себе строки для каждого из 6
    измерений.
    :param rows_list: Список измерений для каждого положения датчика. Внутри
        него находятся row из функции "form_row".
    :return: Функция возвращает <numpy.ndarray> 6x3, который в дальнейшем
        является матрицей "raw" данных.
    """
    raw_data = np.array(rows_list)
    return raw_data


def validate_raw_data(raw_data, sensor_threshold):
    """
    Данная функция проверяет факт соответствия сырых данных на входе ожидаемым
    данным. Пример: идём по матрице raw данных 6х3 и смотрим, нет ли аномальных
    отклонений от нуля в её строках.
    Функция выводит строки, которые не соответствуют ожидаемым.
    :param raw_data: Это массив numpy.ndarray размерностью 6x3, полученный из
        функции "form_raw_data".
    :param sensor_threshold: Допуск для данного типа датчика. Значение в
        пределах которого могут различаться входные данные и ожидаемые. Тип
        данных - float.
    :return: Возвращает boolean переменную, которая обозначает результат
        проверки.
    """
    flag = False
    check_result = False
    for idx, row in enumerate(raw_data):
        if np.abs(row[0]) > sensor_threshold:
            flag = True
        if np.abs(row[1]) > sensor_threshold:
            flag = True
        if np.abs(row[2]) > sensor_threshold:
            flag = True
        if flag:
            print(
                f"Данные в измерении №{idx + 1} {row} не соответствуют "
                f"ожидаемым, необходимо считать их снова!"
            )
            check_result = True
        flag = False

    return check_result


def calibrate_gyroscope(raw_data, error_threshold, sens_thrsh):
    """
    Данная функция производит математическую обработку raw данных для получения
    матрицы калибровки. Затем происходит проверка полученной матрицы - проходят
    ли откалиброванные raw данные допуск "error_threshold", введённый
    пользователем.
    :param raw_data: Массив raw данных <numpy.ndarray> размерностью 6x3.
    :param error_threshold: Допустимая погрешность калибровки, вводимая
        пользователем. Тип данных - float.
    :param sens_thrsh: Допуск для данного типа датчика. Значение в
        пределах которого могут различаться входные данные и ожидаемые. Тип
        данных - float.
    :return: Возвращает <numpy.ndarray> калибровочную матрицу размерностью 4x3.
    """
    err_expected_data = validate_raw_data(raw_data, sens_thrsh)
    if err_expected_data:
        print(
            'Проверка входных данных закончилась с ошибкой, '
            'дальнейшая калибровка невозможна!'
        )
    else:
        shift_vec_temp = []
        compare_vector = [0.0, 0.0, 0.0]
        flag = False
        calibration_matrix = np.eye(3)
        for row in raw_data:
            shift_vec_temp.append(np.abs(row) - np.abs(compare_vector))
        shift_vector = np.mean(shift_vec_temp, axis=0)
        calibration_matrix = np.vstack([calibration_matrix, shift_vector])
        raw_data = np.append(raw_data, [[1], [1], [1], [1], [1], [1]], axis=1)
        calibrated_data = raw_data.dot(calibration_matrix)
        for row in calibrated_data:
            if np.abs(row[0]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {row}, '
                    f'элемент {row[0]}'
                )
            if np.abs(row[1]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {row}, '
                    f'элемент {row[1]}'
                )
            if np.abs(row[2]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {row}, '
                    f'элемент {row[2]}'
                )
        if not flag:
            print('Погрешность калибровки находится в пределах допустимой.')

        return calibration_matrix


def gyr_input_validation(calib_matrix, raw_dimensions, error_threshold):
    """
    Данная функция проверяет все входные значения для гироскопа на предмет
    аномальных выбросов, которые могли бы повлиять на точность калибровки.
    Функция идёт по списку всех измерений и проверяет, попадает ли данное
    измерение в допуск после произведения на матрицу калибровки.
    :param calib_matrix: Калибровочная матрица <numpy.ndarray>
        размерностью 4x3, полученная после математической обработки.
    :param raw_dimensions: Список всех измерений для каждого положения датчика.
        Структура: [[Значения для положения №1], [Значения для положения №2],
        ..., [Значения для положения №6]].
    :param error_threshold: Допустимая погрешность калибровки, вводимая
        пользователем. Тип данных - float.
    :return: Возвращает boolean переменную, которая описывает результат
        проверки.
    """
    flag = False
    for idx, dim in enumerate(raw_dimensions):
        # print(f'Dimension {idx}:\n {dim}')
        for row in dim:
            row_check = np.append(row, [1], axis=0)
            if (abs(row_check.dot(calib_matrix)[0]) - 0.0 > error_threshold or
                abs(row_check.dot(calib_matrix)[1]) - 0.0 > error_threshold or
                    abs(row_check.dot(calib_matrix)[2]) -
                    0.0 > error_threshold):
                print(
                    'Значения во входных измерениях содержат '
                    'аномальные выбросы!'
                    f'Значения в строке {row} после калибровки '
                    f'сильно отличаются от [0.0, 0.0, 0.0].'
                )
                flag = True
    if not flag:
        print('Измерения во входных данных не содержат аномальных выбросов!')

    return flag
