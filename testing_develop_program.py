import time
from DataTypes import READ_TIMEOUT
from DataTypes import IBCMAllMeasPayloads
import serial
import struct
from numpy.random import uniform
from numpy import pi, sin, cos


"""
Данный программный код не проверяет правильность отправки команд от 
основного контроллера, а просто, при получении двух команд, отправляет ответ 
на них. Этот код служит для тестирования программного продукта на этапе его 
разработки. Для тестирования требуется поменять ЛОКАЛЬНО следующие параметры: 
* COM_PORT - номер com порта на который у вас сделана пара через эмулятор 
    Пример: Создана пара из 21 и 20 ком портов, тогда главная программна 
    подключается к 20 порту, а тестирующая к 21.
* BAUD_RATE - Скорость  подключения, в большинстве случаев, 
    оставляем без изменений.
* TESTING_TYPE - датчик, который мы тестируем:
    # 1 - Акселерометр 
    # 2 - Гироскоп 
    # 3 - Магнитометр 
* MAGNETIC_DECLINATION - магнитное отклонение местности, default=58.0.
* READING_TIMES - Количество "считанных" с датчика измерений. К примеру, при 
    значении 500 для каждого положения датчика будет 500 "считываний".
* RAW_DATA - Матрица значений, которые будут отправлены на контроллер
"""


COM_PORT = "COM2"

BAUD_RATE = 115200

TESTING_TYPE = 1

MAGNETIC_DECLINATION = 58.0

READING_TIMES = 500


def form_raw_data(sensor_type, mag_declination, read_times):
    raw_data = []
    if sensor_type == 1:
        for i in range(6):
            dimension = []
            if i + 1 == 1:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.98, 1.2),
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 2:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-1.2, -0.98),
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 3:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(0.98, 1.2),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 4:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-1.2, -0.98),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 5:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02),
                        uniform(0.98, 1.2)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 6:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02),
                        uniform(-1.2, -0.98)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)

    if sensor_type == 2:
        for i in range(6):
            dimension = []
            if i + 1 == 1:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.98, 1.2),
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 2:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-1.2, -0.98),
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 3:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(0.98, 1.2),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 4:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-1.2, -0.98),
                        uniform(-0.02, 0.02)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 5:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02),
                        uniform(0.98, 1.2)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 6:
                for _ in range(read_times):
                    rand_data = [
                        uniform(-0.02, 0.02),
                        uniform(-0.02, 0.02),
                        uniform(-1.2, -0.98)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)

    if sensor_type == 3:
        rad_angle = mag_declination * (pi / 180)
        for i in range(24):
            dimension = []
            if i + 1 == 1:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * sin(rad_angle),
                        uniform(0.9, 1.1) * cos(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 2:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * sin(rad_angle),
                        0.0,
                        -uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 3:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * sin(rad_angle),
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 4:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * sin(rad_angle),
                        0.0,
                        uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 5:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        uniform(0.9, 1.1) * cos(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 6:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        0.0,
                        uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 7:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 8:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        0.0,
                        -uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 9:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        uniform(0.9, 1.1) * sin(rad_angle),
                        uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 10:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        uniform(0.9, 1.1) * sin(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 11:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        uniform(0.9, 1.1) * sin(rad_angle),
                        -uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 12:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * cos(rad_angle),
                        uniform(0.9, 1.1) * sin(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 13:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 14:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * cos(rad_angle),
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 15:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        -uniform(0.9, 1.1) * cos(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 16:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        -uniform(0.9, 1.1) * sin(rad_angle),
                        0.0
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 17:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * cos(rad_angle),
                        0.0,
                        uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 18:
                for _ in range(read_times):
                    rand_data = [
                        0,
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 19:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        0.0,
                        uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 20:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        uniform(0.9, 1.1) * cos(rad_angle),
                        uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 21:
                for _ in range(read_times):
                    rand_data = [
                        uniform(0.9, 1.1) * cos(rad_angle),
                        0.0,
                        -uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 22:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        uniform(0.9, 1.1) * cos(rad_angle),
                        -uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 23:
                for _ in range(read_times):
                    rand_data = [
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        0.0,
                        -uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)
            if i + 1 == 24:
                for _ in range(read_times):
                    rand_data = [
                        0.0,
                        -uniform(0.9, 1.1) * cos(rad_angle),
                        -uniform(0.9, 1.1) * sin(rad_angle)
                    ]
                    dimension.append(rand_data)
                raw_data.append(dimension)

    return raw_data


def select_data_to_send(step, index, possible_data):
    return possible_data[step][index]


TEMP_HEX = "AAAA0300070000000400000038000000410100" \
           "000000000006000000513514BC363C51BB86CC" \
           "BF3B0000A2BD000048BC00E07E3F50D1084272" \
           "8A0EBFBBB8ADBE8738C63E000000009710777D"

data = IBCMAllMeasPayloads(bytes.fromhex(TEMP_HEX))

current_step = 0
count_aa = 0
last_byte = ""

RAW_DATA = form_raw_data(TESTING_TYPE, MAGNETIC_DECLINATION, READING_TIMES)
"""for row in RAW_DATA:
    print(row)"""

rec_data = ""

with serial.Serial(
        port=COM_PORT,
        baudrate=BAUD_RATE,
        timeout=READ_TIMEOUT
) as serial_port:
    while True:
        if serial_port.isOpen():
            current_byte = serial_port.read().hex().upper()
            rec_data += current_byte
            if last_byte == "AA" and current_byte == "AA":
                print(rec_data)
                rec_data = ""
                count_aa += 1
                if count_aa == 3:
                    for i in range(len(RAW_DATA[current_step])):
                        if TESTING_TYPE == 1:
                            data.aAcc = select_data_to_send(
                                current_step,
                                i,
                                RAW_DATA
                            )
                        if TESTING_TYPE == 2:
                            data.aGyr = select_data_to_send(
                                current_step,
                                i,
                                RAW_DATA
                            )
                        if TESTING_TYPE == 3:
                            data.aMag = select_data_to_send(
                                current_step,
                                i, 
                                RAW_DATA
                            )
                        serial_port.write(data.generate_hex())
                    current_step += 1
                    print(f"номер измерения: {current_step}")
                    print(data.aAcc)
                    if current_step == 6:
                        current_step = 0
                if(count_aa == 4 and current_step != 1) or (current_step == 1 and count_aa == 5):
                    count_aa = 0
            last_byte = current_byte


