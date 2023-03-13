import numpy as np
from numpy import sin, cos, pi


def form_ideal_matrix(magnetic_declination):
    """
    Данная функция создаёт матрицу идеальных данных, используя магнитное
    отклонение, введённое пользователем.
    :param magnetic_declination: Величина магнитного отклонения в точке,
        где происходит калибровка.
    :return: Возвращает матрицу идеальных данных <numpy.ndarray>
        размерностью 24x3
    """
    # Test magnetic_declination = 58.0
    b_gs = 1.0
    rad_angle = magnetic_declination * (pi / 180)
    ideal_matrix = np.array([
        [b_gs * sin(rad_angle), b_gs * cos(rad_angle), 0.0],  # X – вниз, Y –
        # север, Z - восток
        [b_gs * sin(rad_angle), 0.0, -b_gs * cos(rad_angle)],  # X – вниз, Y –
        # восток, Z - юг
        [b_gs * sin(rad_angle), -b_gs * cos(rad_angle), 0.0],  # X – вниз, Y –
        # юг, Z - запад
        [b_gs * sin(rad_angle), 0.0, b_gs * cos(rad_angle)],  # X – вниз, Y –
        # запад, Z - север
        [-b_gs * sin(rad_angle), b_gs * cos(rad_angle), 0.0],  # X – вверх, Y –
        # север, Z - запад
        [-b_gs * sin(rad_angle), 0.0, b_gs * cos(rad_angle)],  # X – вверх, Y –
        # восток, Z - север
        [-b_gs * sin(rad_angle), -b_gs * cos(rad_angle), 0.0],  # X – вверх, Y
        # – юг, Z - восток
        [-b_gs * sin(rad_angle), 0.0, -b_gs * cos(rad_angle)],  # X – вверх,
        # Y – запад, Z - юг
        [0.0, b_gs * sin(rad_angle), b_gs * cos(rad_angle)],  # X – восток, Y –
        # вниз, Z - север
        [-b_gs * cos(rad_angle), b_gs * sin(rad_angle), 0.0],  # X – юг, Y –
        # вниз, Z - восток
        [0.0, b_gs * sin(rad_angle), -b_gs * cos(rad_angle)],  # X – запад, Y –
        # вниз, Z - юг
        [b_gs * cos(rad_angle), b_gs * sin(rad_angle), 0.0],  # X – север, Y –
        # вниз, Z - запад
        [0.0, -b_gs * sin(rad_angle), b_gs * cos(rad_angle)],  # X – запад, Y –
        # вверх, Z - север
        [b_gs * cos(rad_angle), -b_gs * sin(rad_angle), 0.0],  # X – север, Y –
        # вверх, Z - восток
        [0.0, -b_gs * sin(rad_angle), -b_gs * cos(rad_angle)],  # X – восток,
        # Y – вверх, Z - юг
        [-b_gs * cos(rad_angle), -b_gs * sin(rad_angle), 0.0],  # X – юг, Y –
        # вверх, Z - запад
        [b_gs * cos(rad_angle), 0.0, b_gs * sin(rad_angle)],  # X – север, Y –
        # восток, Z - вниз
        [0, -b_gs * cos(rad_angle), b_gs * sin(rad_angle)],  # X – восток, Y –
        # юг, Z - вниз
        [-b_gs * cos(rad_angle), 0.0, b_gs * sin(rad_angle)],  # X – юг, Y –
        # запад, Z - вниз
        [0.0, b_gs * cos(rad_angle), b_gs * sin(rad_angle)],  # X – запад, Y –
        # север, Z - вниз
        [b_gs * cos(rad_angle), 0.0, -b_gs * sin(rad_angle)],  # X – север, Y –
        # запад, Z - вверх
        [0.0, b_gs * cos(rad_angle), -b_gs * sin(rad_angle)],  # X – восток,
        # Y – север, Z - вверх
        [-b_gs * cos(rad_angle), 0.0, -b_gs * sin(rad_angle)],  # X – юг, Y –
        # восток, Z - вверх
        [0.0, -b_gs * cos(rad_angle), -b_gs * sin(rad_angle)],  # X – запад,
        # Y – юг, Z - вверх
    ])

    return ideal_matrix


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
    значений для каждого положения к матрице 24x3. Данную функцию необходимо
    использовать, когда rows_list содержит в себе строки для каждого из 24
    измерений.
    :param rows_list: Список измерений для каждого положения датчика. Внутри
        него находятся row из функции "form_row".
    :return: Функция возвращает <numpy.ndarray> 24x3, который в дальнейшем
        является матрицей "raw" данных
    """
    raw_data = np.array(rows_list)
    return raw_data


def validate_raw_data(raw_data, ideal_data, sensor_threshold):
    """
    Данная функция проверяет факт соответствия сырых данных на входе ожидаемым
    данным. Функция выводит строки, которые не соответствуют ожидаемым.
    :param raw_data: Это массив numpy.ndarray размерностью 24x3, полученный из
        функции "form_raw_data".
    :param ideal_data: Матрица идеальных данных размерностью 24x3.
    :param sensor_threshold: Допуск для данного типа датчика. Значение в
        пределах которого могут различаться входные данные и ожидаемые. Тип
        данных - float.
    :return: Возвращает boolean переменную, которая обозначает результат
        проверки.
    """
    flag = False
    check_result = False
    for idx, row in enumerate(raw_data):
        if (np.abs(np.abs(row[0]) - np.abs(ideal_data[idx][0]))
                > sensor_threshold):
            flag = True
        if (np.abs(np.abs(row[1]) - np.abs(ideal_data[idx][1]))
                > sensor_threshold):
            flag = True
        if (np.abs(np.abs(row[2]) - np.abs(ideal_data[idx][2]))
                > sensor_threshold):
            flag = True
        if flag:
            print(
                f"Данные в измерении №{idx + 1}: {row} не соответствуют "
                f"ожидаемым {ideal_data[idx]}, необходимо считать их снова!"
            )
            check_result = True
        flag = False

    return check_result


def calibrate_magnetometer(raw_data, ideal_matrix, error_threshold, sens_thrsh):
    err_expected_data = validate_raw_data(raw_data, ideal_matrix, sens_thrsh)
    if err_expected_data:
        print(
            'Проверка входных данных закончилась с ошибкой, '
            'дальнейшая калибровка невозможна!'
        )
    else:
        """ideal_matrix = np.append(
            ideal_matrix,
            [
                [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1],
                [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]
            ],
            axis=1
        )"""
        # print(ideal_matrix)
        flag = False
        raw_data = np.append(
            raw_data,
            [
                [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1],
                [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]
            ],
            axis=1
        )
        #print(raw_data)
        transposed_raw_matrix = np.transpose(raw_data)
        calibration_matrix = (
            np.linalg.inv(
                transposed_raw_matrix.dot(raw_data)).dot(transposed_raw_matrix)
        ).dot(ideal_matrix)
        calibrated_data = raw_data.dot(calibration_matrix)
        for idx, row in enumerate(ideal_matrix):
            if abs(calibrated_data[idx][0]) - abs(row[0]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {calibrated_data[idx]}, '
                    f'элемент {calibrated_data[idx][0]}'
                )
            if abs(calibrated_data[idx][1]) - abs(row[1]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {calibrated_data[idx]}, '
                    f'элемент {calibrated_data[idx][1]}'
                )
            if abs(calibrated_data[idx][2]) - abs(row[2]) > error_threshold:
                flag = True
                print(
                    'Погрешность калибровки больше допустимой!'
                    f'строка {calibrated_data[idx]}, '
                    f'элемент {calibrated_data[idx][2]}'
                )
        if not flag:
            print('Погрешность калибровки находится в пределах допустимой.')

        return calibration_matrix


def mag_input_validation(
        calibration_matrix,
        raw_dimensions,
        error_threshold,
        mag_declin
):
    """
    Данная функция проверяет все входные значения для магнитометра на предмет
    аномальных выбросов, которые могли бы повлиять на точность калибровки.
    Функция идёт по списку всех измерений и проверяет, попадает ли данное
    измерение в допуск после произведения на матрицу калибровки.
    :param calibration_matrix: Калибровочная матрица <numpy.ndarray>
        размерностью 24x3, полученная после математической обработки.
    :param raw_dimensions: Список всех измерений для каждого положения датчика.
        Структура: [[Значения для положения №1], [Значения для положения №2],
        ..., [Значения для положения №24]].
    :param error_threshold: Допустимая погрешность калибровки, вводимая
        пользователем. Тип данных - float.
    :return: Возвращает boolean переменную, которая описывает результат
        проверки.
    """
    ideal_matrix = form_ideal_matrix(mag_declin)
    flag = False
    for idx, dim in enumerate(raw_dimensions):
        # print(f'Dimension {idx}:\n {dim}')
        for row in dim:
            row_check = np.append(row, [1], axis=0)
            if (abs(row_check.dot(calibration_matrix)[0]) -
                    abs(ideal_matrix[idx][0]) > error_threshold or
                    abs(row_check.dot(calibration_matrix)[1]) -
                    abs(ideal_matrix[idx][1]) > error_threshold or
                    abs(row_check.dot(calibration_matrix)[2]) -
                    abs(ideal_matrix[idx][2]) > error_threshold):
                print(
                    'Значения во входных измерениях содержат '
                    'аномальные выбросы!'
                    f'Значения в строке {row} после калибровки '
                    f'сильно отличаются от {ideal_matrix[idx]}.'
                )
                flag = True
    if not flag:
        print('Измерения во входных данных не содержат аномальных выбросов!')

    return flag


