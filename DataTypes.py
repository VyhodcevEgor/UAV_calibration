import struct

READ_TIMEOUT = 2


def crc_function(crc_type, buf):
    """
    Данная функция нужна для расчета контрольной суммы в зависимости от типа указанной контрольной суммы.
    :param crc_type: Тип контрольной суммы, с.м. Class CaCrcType
    :param buf: Строка (str) для которой мы рассчитываем контрольную сумму
    """
    if crc_type == 0:
        return 0
    elif crc_type == 1:
        return 0
    elif crc_type == 2:
        return 0
    elif crc_type == 3:
        return 0
    elif crc_type == 4:
        crc_table = [0] * 256
        for i in range(256):
            crc = i
            for j in range(8):
                crc = crc & 1 and (crc >> 1) ^ 0xEDB88320 or crc >> 1
            crc_table[i] = crc
        crc = 0xFFFFFFFF
        for b in buf:
            crc = crc_table[(crc ^ b) & 0xFF] ^ (crc >> 8)
        return crc ^ 0xFFFFFFFF
    else:
        raise ValueError("Invalid crc_type")


class CaCrcType:
    """
    Класс описывает возможные типы контрольной суммы
    """
    SFH_CRC_TYPE_NO_CRC = 0
    SFH_CRC_TYPE_SIZE_8BIT = 1
    SFH_CRC_TYPE_SIZE_16BIT = 2
    SFH_CRC_TYPE_FIX_16BIT = 3
    SFH_CRC_TYPE_SIZE_32BIT = 4


class IBCMParseMessageAPIE:
    """
    Класс описывает параметры IBCMParseMessageAPIE
    я сам не знаю для чего нужны некоторые из них
    """
    iBCM_PARSE_MESSAGE_API_prvSendConfPack = 0
    iBCM_PARSE_MESSAGE_API_prvReadConfPack = 1
    iBCM_PARSE_MESSAGE_API_prvSendReconfigCmd = 2
    iBCM_PARSE_MESSAGE_API_prvReadReconfigCmd = 3
    iBCM_PARSE_MESSAGE_API_prvRequestUID = 4
    iBCM_PARSE_MESSAGE_API_prvSendUID = 5
    iBCM_PARSE_MESSAGE_API_prvSendAllData = 6
    iBCM_PARSE_MESSAGE_API_prvReadAllData = 7
    iBCM_PARSE_MESSAGE_API_prvSendAllDataForSerialPlot = 8
    iBCM_PARSE_MESSAGE_API_prvSendGyrAccDataForSerialPlot = 9
    iBCM_PARSE_MESSAGE_API_prvSendGyrAccTemperatureDataForSerialPlot = 10
    iBCM_PARSE_MESSAGE_API_prvSendGyrAccTemperatureData = 11
    iBCM_PARSE_MESSAGE_API_prvReadGyrAccTemperatureData = 12
    iBCM_PARSE_MESSAGE_API_prvSendDataInSerialPlotForNavDebug = 13
    iBCM_PARSE_MESSAGE_API_MAX_NUMB = 14


class CAServicesIDE:
    """
    Класс описывает параметры CAServicesIDE
    я сам не знаю для чего нужны некоторые из них
    """
    CA_ID_BROADCAST = 0
    CA_ID_iMAG_SERVICE_MAIN = 1
    CA_ID_IMAG_COMMUNICATION_SERVICE_MAIN = 2
    CA_ID_iBCM = 3  # Use this value
    CA_ID_UNKNOW = 4
    CA_ID_IMAGCSext = 5
    CA_ID_iHILBINS = 6
    CA_ID_TO_DEBUG_PORT = 7
    CA_ID_TO_DEBUG_PORT_RAW = 8
    CA_ID_HEARTBEAT = 9
    CA_ID_IMAG_COMMUNICATION_SERVICE_RESERVE = 10
    CA_ID_CALIB_GYRACC = 11
    CA_ID_ACM_BINS = 12
    CA_ID_ACM_AUTOPILOT = 13
    CA_ID_ROTPLATCOM = 14
    CA_ID_ROTPLATCOM_SINERGET = 15
    CA_ID_MAG_CALIB = 16
    CA_SERVICE_MAX_NUMB = 17


class SensorIndicatorType:
    """
    Класс описывает параметры типы калибруемых сенсоров
    """
    Gyr = "Гироскоп"
    Acc = "Акселерометр"
    Mag = "Магнитометр"


class MagCalibParseMessageAPI:
    """
    Класс описывает параметры MagCalibParseMessageAPI
    я сам не знаю для чего нужны некоторые из них
    """
    MAGCALIB_PARSE_MESSAGE_READ_MATRIX_CALIB = 0
    MAGCALIB_PARSE_MESSAGE_SEND_MATRIX_CALIB = 1
    MAGCALIB_PARSE_MESSAGE_READ_MATRIX_OFFSET = 2
    MAGCALIB_PARSE_MESSAGE_SEND_MATRIX_OFFSET = 3
    # Без полезной нагрузки
    MAGCALIB_PARSE_MESSAGE_WRITE_IN_EEPROM = 4

    # Без полезной нагрузки
    MAGCALIB_PARSE_MESSAGE_RESET_MATRIX_ALL = 5

    MAGCALIB_PARSE_MESSAGE_API_MAX_NUMB = 6


"""
# Полезная нагрузка сообщения MAGCALIB_PARSE_MESSAGE_SEND_MATRIX_CALIB
float a2MemAlloc[3][3];
# Полезная нагрузка сообщения MAGCALIB_PARSE_MESSAGE_SEND_MATRIX_OFFSET
float a2MemAlloc[3][1];
"""


def generate_header(sender_id, recipient_id, pack_id, crc_type, payload_size):
    """
    Данная функция генерирует header для сообщения, которое будет отправлено на контроллер
    :param sender_id: id Отправителя, как правило совпадает с recipient_id
    :param recipient_id - совпадает с sender_id
    :param pack_id: Тип команды, которую необходимо выполнить контроллеру
    :param crc_type: тип контрольной суммы
    :param payload_size: размер полезной нагрузки
    :return: сгенерированный заголовок для сообщения
    """
    start_frame = (43690).to_bytes(2, byteorder='little')
    sender_id_hex = struct.pack("B", sender_id)
    recipient_id_hex = struct.pack("B", recipient_id)
    pack_id_hex = struct.pack("I", pack_id)
    crc_type_hex = struct.pack("I", crc_type)
    header = start_frame
    header += sender_id_hex
    header += recipient_id_hex
    header += pack_id_hex
    header += crc_type_hex
    header += struct.pack("I", payload_size)
    return header


class MagnetometerOffsetMatrix:
    """
    Класс для описания матрицы смещений магнитометра
    """
    def __init__(self, matrix):
        """
        :param matrix: матрица смещений магнитометра
        """
        self.__payload_size = 12
        self.__matrix = matrix

    def rewrite_matrix(self, matrix):
        """
        Данная функция меняет значение внутри класса
        :param matrix: матрица смещений магнитометра
        """
        self.__matrix = matrix

    def __matrix_to_list(self):
        """
        Данная функция преобразует матрицу в список, для дальнейшего преобразования в bytes
        """
        temp = []
        for elem in self.__matrix:
            temp.extend(elem)
        return temp

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        """
        Данная функция генерирует сообщение для отправки на контроллер
        :param sender_id: отправитель
        :param recipient_id: получатель
        :param pack_id: тип нагрузки для компьютера
        :param crc_type: тип контрольной суммы
        :return: возвращает сообщения для отправки на контроллер
        """

        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        list_matrix = self.__matrix_to_list()
        pay_load = ""
        for element in list_matrix:
            pay_load += struct.pack("f", element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in list_matrix:
            pay_load += struct.pack("f", element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class ResetGyrPolyAll:
    @staticmethod
    def generate_hex(sender_id, recipient_id, pack_id, crc_type):
        """
        Функция и класс нужны для очистки значений гироскопа, находящихся на контроллере
        :param sender_id: отправитель
        :param recipient_id: получатель
        :param pack_id: тип нагрузки для компьютера
        :param crc_type: тип контрольной суммы
        :return: возвращает сообщения для отправки на контроллер
        """
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, 0)
        return header + struct.pack("i", 21845)


class ResetAccPolyAll:
    @staticmethod
    def generate_hex(sender_id, recipient_id, pack_id, crc_type):
        """
           Функция и класс нужны для очистки значений акселерометра, находящихся на контроллере
           :param sender_id: отправитель
           :param recipient_id: получатель
           :param pack_id: тип нагрузки для компьютера
           :param crc_type: тип контрольной суммы
           :return: возвращает сообщения для отправки на контроллер
           """
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, 0)
        return header + struct.pack("i", 21845)


class GyroscopeCalibrationPolynomial:
    def __init__(self, gyr_poly_calib_mat):
        self.__payload_size = 9 * 6 * 4
        self.__gyr_poly_calib_mat = gyr_poly_calib_mat

    def rewrite_matrix(self, gyr_poly_calib_mat):
        self.__gyr_poly_calib_mat = gyr_poly_calib_mat

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        pay_load = ""
        for element in self.__gyr_poly_calib_mat:
            pay_load += struct.pack('%f' % len(element), *element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in self.__gyr_poly_calib_mat:
            pay_load += struct.pack('%f' % len(element), *element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class GyroscopeOffsetPolynomial:
    def __init__(self, gyr_poly_off_mat):
        self.__payload_size = 3 * 6 * 4
        self.__gyr_poly_off_mat = gyr_poly_off_mat

    def rewrite_matrix(self, gyr_poly_off_mat):
        self.__gyr_poly_off_mat = gyr_poly_off_mat

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        pay_load = ""
        for element in self.__gyr_poly_off_mat:
            pay_load += struct.pack('%f' % len(element), *element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in self.__gyr_poly_off_mat:
            pay_load += struct.pack('%f' % len(element), *element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class AccelerometerCalibrationPolynomial:
    def __init__(self, acc_poly_calib_mat):
        self.__payload_size = 9 * 6 * 4
        self.__acc_poly_calib_mat = acc_poly_calib_mat

    def rewrite_matrix(self, acc_poly_calib_mat):
        self.__acc_poly_calib_mat = acc_poly_calib_mat

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        pay_load = ""
        for element in self.__acc_poly_calib_mat:
            pay_load += struct.pack('%f' % len(element), *element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in self.__acc_poly_calib_mat:
            pay_load += struct.pack('%f' % len(element), *element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class AccelerometerOffsetPolynomial:
    def __init__(self, acc_poly_off_mat):
        self.__payload_size = 3 * 6 * 4
        self.__acc_poly_off_mat = acc_poly_off_mat

    def rewrite_matrix(self, acc_poly_off_mat):
        self.__acc_poly_off_mat = acc_poly_off_mat

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        pay_load = ""
        for element in self.__acc_poly_off_mat:
            pay_load += struct.pack('%f' % len(element), *element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in self.__acc_poly_off_mat:
            pay_load += struct.pack('%f' % len(element), *element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class MagnetometerCalibrationMatrix:

    def __init__(self, matrix):
        self.__payload_size = 36
        self.__matrix = matrix

    def rewrite_matrix(self, matrix):
        self.__matrix = matrix

    def __matrix_to_list(self):
        temp = []
        for elem in self.__matrix:
            temp.extend(elem)
        return temp

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):

        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        list_matrix = self.__matrix_to_list()
        pay_load = ""
        for element in list_matrix:
            pay_load += struct.pack("f", element).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = b""
        for element in list_matrix:
            pay_load += struct.pack("f", element)

        crc = struct.pack("I", crc)
        return header + pay_load + crc


class ICALIBGYRACCParseMessageAPI:
    # Секция для взаимодействия с калибровочной матрицей полиномов гироскопа
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_SendRequestPolyCalibMat = 0
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_ReadPolyCalibMat = 1
    # Используем 2, 3
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_ReadPolyCalibMat = 2
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_SendPolyCalibMat = 3

    # Секция для взаимодействия с матрицей полиномов смещений гироскопа
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_SendRequestPolyOffsetMat = 4
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_ReadPolyOffsetMat = 5
    # Используем 6, 7
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_ReadPolyOffsetMat = 6
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_SendPolyOffsetMat = 7

    # Секция для взаимодействия с динамической матрицей полиномов гироскопа
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_SendRequestPolyDynamicMat = 8
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PC_ReadPolyDynamicMat = 9
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_ReadPolyDynamicMat = 10
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_MCU_SendPolyDynamicMat = 11

    # Секция для взаимодействия с калибровочной матрицей полиномов акселерометра
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_PC_SendRequestPolyCalibMat = 12
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_PC_ReadPolyCalibMat = 13
    # Используем 14, 15
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_ReadPolyCalibMat = 14
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_SendPolyCalibMat = 15

    # Секция для взаимодействия с матрицей полиномов смещений акселерометра
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_PC_SendRequestPolyOffsetMat = 16
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_PC_ReadPolyOffsetMat = 17
    # Используем 18-25
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_ReadPolyOffsetMat = 18
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_SendPolyOffsetMat = 19

    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGyr_MCU_RecalculatePolyAll = 20
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_RecalculatePolyAll = 21

    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGyr_MCU_WritePolyInEEPROM = 22
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_WritePolyInEEPROM = 23

    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGyr_MCU_ResetPolyAll = 24
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvAcc_MCU_ResetPolyAll = 25
    # Используем 28, 29, 31
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PcSendPolyInMCU = 26
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PcSendRequestWriteInEEPROMFromRAM = 27
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_McuCopyPolyInEEPROMFromRAM = 28
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_McuRecalculatePoly2Mat = 29
    ICALIB_GYRACC_PARSE_MESSAGE_API_prvGYR_PcSendRequestToRecalculatePoly2Mat = 30

    ICALIB_GYRACC_PARSE_MESSAGE_API_MAX_NUMB = 31


class IBCMReconfigCMDt:
    def __init__(self, is_need_reconfig):
        self.is_need_reconfig = is_need_reconfig
        self.__payload_size = 4

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        pay_load = struct.pack("I", self.is_need_reconfig).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))

        pay_load = struct.pack("I", self.is_need_reconfig)
        crc = struct.pack("I", crc)
        return header + pay_load + crc


class IBCMbConfPayloadS:
    def __init__(self, baud_rate, ul_dt_us, el_pack_id_for_default_request):
        self.baud_rate = baud_rate
        self.ul_dt_us = ul_dt_us
        self.el_pack_id_for_default_request = el_pack_id_for_default_request
        self.__payload_size = 4 + 4 + 4

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        header = generate_header(sender_id, recipient_id, pack_id, crc_type, self.__payload_size)

        temp_pay_load = struct.pack("I", self.baud_rate).hex()
        temp_pay_load += struct.pack("I", self.ul_dt_us).hex()
        temp_pay_load += struct.pack("I", self.el_pack_id_for_default_request).hex()
        crc = crc_function(crc_type, bytes.fromhex(temp_pay_load))
        crc = struct.pack("I", crc)

        pay_load = struct.pack("I", self.baud_rate)
        pay_load += struct.pack("I", self.ul_dt_us)
        pay_load += struct.pack("I", self.el_pack_id_for_default_request)
        return header + pay_load + crc


class IBCMAllMeasPayloads:
    def __init__(self, bytes_data):
        self.__bytes_data = bytes_data
        self.start_frame = bytes_data[0:16]
        self.timeStamp = struct.unpack("I", bytes_data[16:20])[0]
        self.statusFlags = struct.unpack("I", bytes_data[20:24])[0]
        self.ulDt_us = struct.unpack("I", bytes_data[24:28])[0]

        self.aGyr = [
            struct.unpack("f", bytes_data[28:32])[0],
            struct.unpack("f", bytes_data[32:36])[0],
            struct.unpack("f", bytes_data[36:40])[0],
        ]

        self.aAcc = [
            struct.unpack("f", bytes_data[40:44])[0],
            struct.unpack("f", bytes_data[44:48])[0],
            struct.unpack("f", bytes_data[48:52])[0],
        ]

        self.gyrAccTemperature = struct.unpack("f", bytes_data[52:56])[0]

        self.aMag = [
            struct.unpack("f", bytes_data[56:60])[0],
            struct.unpack("f", bytes_data[60:64])[0],
            struct.unpack("f", bytes_data[64:68])[0],
        ]

        self.gyrAccTemperature = struct.unpack("f", bytes_data[68:72])[0]

        self.control_sum = bytes_data[72::]

    def reset_values(self, a_gyr, a_acc, a_mag):
        self.aGyr = a_gyr
        self.aAcc = a_acc
        self.aMag = a_mag

    def generate_hex(self):
        result = self.__bytes_data[0:28]

        a_gyr = struct.pack("fff", self.aGyr[0], self.aGyr[1], self.aGyr[2])
        a_acc = struct.pack("fff", self.aAcc[0], self.aAcc[1], self.aAcc[2])
        a_mag = struct.pack("fff", self.aMag[0], self.aMag[1], self.aMag[2])
        result += a_gyr + a_acc
        result += self.__bytes_data[52:56]
        result += a_mag
        result += self.__bytes_data[68::]
        return result
