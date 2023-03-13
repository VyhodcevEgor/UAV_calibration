import time
import serial
import threading
from DataTypes import CaCrcType
from DataTypes import IBCMParseMessageAPIE
from DataTypes import CAServicesIDE
from DataTypes import IBCMReconfigCMDt
from DataTypes import IBCMbConfPayloadS
from DataTypes import IBCMAllMeasPayloads
from DataTypes import MagCalibParseMessageAPI
# from DataTypes import ICALIBGYRACCParseMessageAPI
from DataTypes import SensorIndicatorType
from DataTypes import MagnetometerCalibrationMatrix
from DataTypes import MagnetometerOffsetMatrix


class PortReader:
    def __init__(self):
        self.__serial_port = serial.Serial()
        self.__reading_thread = None
        self.__stop_thread = False
        self.__payloads = []
        self.__gyroscope = []
        self.__accelerometer = []
        self.__magnetometer = []
        self.__indicator_type = None

    def set_port(self, port, baud_rate):
        """
        :param port: Номер ком порта
        :param baud_rate: Скорость общения с ком портом
        :return: True если настрйока и подключение к порту были успешны, иначе False
        """
        try:
            self.__serial_port = serial.Serial(port=port, baudrate=baud_rate)
            self.__serial_port.close()
            return True
        except serial.serialutil.SerialException:
            return False

    def __read(self):

        self.__stop_thread = False
        self.__payloads = []

        self.__gyroscope = []
        self.__accelerometer = []
        self.__magnetometer = []

        x_conf_pack = IBCMbConfPayloadS(
            baud_rate=self.__serial_port.baudrate,
            ul_dt_us=10000,
            el_pack_id_for_default_request=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvSendAllData,
        )
        controller_setting_command = x_conf_pack.generate_hex(
            sender_id=CAServicesIDE.CA_ID_iBCM,
            recipient_id=CAServicesIDE.CA_ID_iBCM,
            pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
            crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT,
        )

        self.__serial_port.write(controller_setting_command.encode())
        time.sleep(0.2)

        x_conf_pack = IBCMReconfigCMDt(
            is_need_reconfig=1
        )

        controller_set_command = x_conf_pack.generate_hex(
            sender_id=CAServicesIDE.CA_ID_iBCM,
            recipient_id=CAServicesIDE.CA_ID_iBCM,
            pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
            crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT,
        )
        self.__serial_port.write(controller_set_command.encode())
        time.sleep(0.2)

        this_byte = ""
        byte_line = ""

        amount_of_bytes = 0

        while not self.__stop_thread:
            prev_byte = this_byte
            this_byte = self.__serial_port.read(size=1).hex()
            byte_line += this_byte
            amount_of_bytes += len(this_byte) // 2

            if prev_byte == "aa" and this_byte == "aa":
                byte_line = prev_byte + this_byte
                amount_of_bytes = 2

            if amount_of_bytes == 76:
                data = bytes.fromhex(byte_line)
                self.__payloads.append(IBCMAllMeasPayloads(data))

                self.__gyroscope.append(self.__payloads[-1].aGyr)
                self.__accelerometer.append(self.__payloads[-1].aAcc)
                self.__magnetometer.append(self.__payloads[-1].aMag)

        else:

            x_conf_pack = IBCMbConfPayloadS(
                baud_rate=self.__serial_port.baudrate,
                ul_dt_us=0,
                el_pack_id_for_default_request=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvSendAllData,
            )
            controller_setting_command = x_conf_pack.generate_hex(
                sender_id=CAServicesIDE.CA_ID_iBCM,
                recipient_id=CAServicesIDE.CA_ID_iBCM,
                pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
                crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT,
            )

            self.__serial_port.write(controller_setting_command.encode())
            time.sleep(0.2)

            x_conf_pack = IBCMReconfigCMDt(is_need_reconfig=1)

            controller_set_command = x_conf_pack.generate_hex(
                sender_id=CAServicesIDE.CA_ID_iBCM,
                recipient_id=CAServicesIDE.CA_ID_iBCM,
                pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
                crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT,
            )

            self.__serial_port.write(controller_set_command.encode())

            # self.__serial_port.close()
            time.sleep(0.2)

    def connect(self):
        """

        :return: Открывает порт для чтения и возвращает True, если порт откртыт, иначе False
        """
        # print("try to connect")
        try:
            self.__serial_port.open()
            return self.__serial_port.is_open
        except serial.serialutil.SerialException:
            return False

    def write_magnetometer_calibration_matrix(self, matrix):
        """

        :param matrix: калибровочная матриа магнитометра, float [3][3]
        :return: Статус выполнения записи матрицы
        """
        try:
            magnetometer = MagnetometerCalibrationMatrix(matrix)
            message = magnetometer.generate_hex(
                CAServicesIDE.CA_ID_MAG_CALIB,
                CAServicesIDE.CA_ID_MAG_CALIB,
                MagCalibParseMessageAPI.MAGCALIB_PARSE_MESSAGE_READ_MATRIX_CALIB,
                CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
            )
            self.__serial_port.write(message.encode())
            print(message)
            return True
        except serial.serialutil.SerialException:
            return False

    def write_magnetometer_offset_matrix(self, matrix):
        """

        :param matrix: матриа смещения, float [3][1]
        :return: Статус выполнения записи матрицы
        """
        try:
            magnetometer = MagnetometerOffsetMatrix(matrix)
            message = magnetometer.generate_hex(
                CAServicesIDE.CA_ID_MAG_CALIB,
                CAServicesIDE.CA_ID_MAG_CALIB,
                MagCalibParseMessageAPI.MAGCALIB_PARSE_MESSAGE_READ_MATRIX_CALIB,
                CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
            )
            print(message)
            self.__serial_port.write(message.encode())

            return True
        except serial.serialutil.SerialException:
            return False

    def start_read(self, read_type: SensorIndicatorType):
        """
        Пример вызова self.start_read(SensorIndicatorType.Mag) - считать показатели магнитометра
        Начинает чтение, если до этого порт был открыт
        :param read_type: Параметр, указывающий, какие данные считать
        :return: True, если чтение началось, инчае False
        """
        if self.__serial_port.isOpen():
            self.__indicator_type = read_type
            self.__reading_thread = threading.Thread(target=self.__read, daemon=True)
            self.__reading_thread.start()
            # print(self.__reading_thread)
            return True
        else:
            return False

    def stop_read(self):
        """
        Заканчивает чтение
        :return: Возвращает все считанные данные, в зависимости от read_type, заданного в start_read.
        Если тип был не задан, то возвращает None
        """
        # print(self.__reading_thread)
        self.__stop_thread = True
        self.__reading_thread.join()
        if self.__indicator_type == SensorIndicatorType.Gyr:
            return self.__gyroscope
        elif self.__indicator_type == SensorIndicatorType.Acc:
            return self.__accelerometer
        elif self.__indicator_type == SensorIndicatorType.Mag:
            return self.__magnetometer
        else:
            return None

    def close_port(self):
        """
        Функция закрывает откртый ранее порт
        :return: True - если порт был закрыт успешно, иначе False
        """

        if self.__serial_port.is_open:
            self.__serial_port.close()
        return not self.__serial_port.is_open


d = PortReader()
d.set_port("COM2", 1042003526)
d.connect()
d.start_read(SensorIndicatorType.Gyr)
d.write_magnetometer_offset_matrix([[0.152062505483627], [-0.0367708317935467], [0.0129895834252238]])
d.stop_read()
