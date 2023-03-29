import time
from DataTypes import READ_TIMEOUT
from DataTypes import IBCMAllMeasPayloads
import serial
import struct

"""
Данный програмнный код не проверяет правильность отправки команда от основного контроллера, 
а просто при получении двух команд отправляет ответ на них
Этот код служит для тестирования программного продукта на этапе его разработки
Для тестирования требуется поменять ЛОКАЛЬНО следующие параметры:
COM_PORT - номер com порта на который у вас сделана пара через эмелятор
Пример: Создана пара из 21 и 20 ком портов, тогда главная программна подключается к 20 порту, а тестирующая к 21
BAUD_RATE - Скорость подкллючения, в большинстве случаев оставляем без изменений
TESTING_TYPE - датчик который мы тестируем
# 1 - Акселерометр
# 2 - Гироскоп
# 3 - Магнитометр
IDEAL_DATA - Матрица значений, которые будут отправлены на контроллер
"""


COM_PORT = "COM2"

BAUD_RATE = 115200

TESTING_TYPE = 1

IDEAL_DATA = [
    [[1.0, 0.0, 0.0]],
    [[-1.0, 0.0, 0.0]],
    [[0.0, 1.0, 0.0]],
    [[0.0, -1.0, 0.0]],
    [[0.0, 0.0, 1.0]],
    [[0.0, 0.0, -1.0]]
]


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

with serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, timeout=READ_TIMEOUT) as serial_port:
    while True:
        if serial_port.isOpen():
            current_byte = serial_port.read().hex().upper()
            print(current_byte)
            if last_byte == "AA" and current_byte == "AA":
                count_aa += 1
                if count_aa == 2:
                    for i in range(len(IDEAL_DATA[current_step])):
                        if TESTING_TYPE == 1:
                            data.aAcc = select_data_to_send(current_step, i, IDEAL_DATA)
                        if TESTING_TYPE == 2:
                            data.aGyr = select_data_to_send(current_step, i, IDEAL_DATA)
                        if TESTING_TYPE == 3:
                            data.aMag = select_data_to_send(current_step, i, IDEAL_DATA)
                        serial_port.write(data.generate_hex())
                    current_step += 1
                    if current_step == 6:
                        current_step = 0
            last_byte = current_byte


