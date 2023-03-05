import struct


def crc_function(crc_type, buf):
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
    SFH_CRC_TYPE_NO_CRC = 0
    SFH_CRC_TYPE_SIZE_8BIT = 1
    SFH_CRC_TYPE_SIZE_16BIT = 2
    SFH_CRC_TYPE_FIX_16BIT = 3
    SFH_CRC_TYPE_SIZE_32BIT = 4


class IBCMParseMessageAPIE:
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
    Gyr = "Гироскоп"
    Acc = "Акселерометр"
    Mag = "Магнитометр"


class MagCalibParseMessageAPI:
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
        self.payload_size = 4

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        start_frame = "AAAA"

        sender_id_hex = struct.pack("B", sender_id).hex()
        recipient_id_hex = struct.pack("B", recipient_id).hex()
        pack_id_hex = struct.pack("I", pack_id).hex()
        crc_type_hex = struct.pack("I", crc_type).hex()
        # crc = crc_function(4, bytes.fromhex("00C201001027000006000000"))

        header = start_frame
        header += sender_id_hex
        header += recipient_id_hex
        header += pack_id_hex
        header += crc_type_hex
        header += struct.pack("I", self.payload_size).hex()
        pay_load = struct.pack("I", self.is_need_reconfig).hex()
        crc = crc_function(crc_type, bytes.fromhex(pay_load))
        crc = struct.pack("I", crc).hex()
        print(header + pay_load + crc)
        return header + pay_load + crc


class IBCMbConfPayloadS:
    def __init__(self, baud_rate, ul_dt_us, el_pack_id_for_default_request):
        self.baud_rate = baud_rate
        self.ul_dt_us = ul_dt_us
        self.el_pack_id_for_default_request = el_pack_id_for_default_request
        self.payload_size = 4 + 4 + 4

    def generate_hex(self, sender_id, recipient_id, pack_id, crc_type):
        start_frame = "AAAA"

        sender_id_hex = struct.pack("B", sender_id).hex()
        recipient_id_hex = struct.pack("B", recipient_id).hex()
        pack_id_hex = struct.pack("I", pack_id).hex()
        crc_type_hex = struct.pack("I", crc_type).hex()
        # crc = crc_function(4, bytes.fromhex("00C201001027000006000000"))

        header = start_frame
        header += sender_id_hex
        header += recipient_id_hex
        header += pack_id_hex
        header += crc_type_hex
        header += struct.pack("I", self.payload_size).hex()

        pay_load = struct.pack("I", self.baud_rate).hex()
        pay_load += struct.pack("I", self.ul_dt_us).hex()
        pay_load += struct.pack("I", self.el_pack_id_for_default_request).hex()

        crc = crc_function(crc_type, bytes.fromhex(pay_load))
        crc = struct.pack("I", crc).hex()

        return header + pay_load + crc
        # print(struct.pack("I", self.el_pack_id_for_default_request + self.ul_dt_us + self.baud_rate).hex())


class IBCMAllMeasPayloads:
    def __init__(self, bytes_data):
        self.header = bytes_data[0:16]
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
        self.controlSumm = bytes_data[72::]
