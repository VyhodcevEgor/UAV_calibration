import time
import serial
import threading
from DataTypes import CaCrcType
from DataTypes import IBCMParseMessageAPIE
from DataTypes import CAServicesIDE
from DataTypes import IBCMReconfigCMDt
from DataTypes import IBCMbConfPayloadS
from DataTypes import IBCMAllMeasPayloads


class PortReader:
    def __init__(self):
        self.__serial_port = serial.Serial()
        self.__reading_thread = None
        self.__stop_thread = False
        self.__payloads = []

    def set_port(self, port, baud_rate):
        try:
            self.__serial_port = serial.Serial(
                port=port,
                baudrate=baud_rate
            )
            return True
        except serial.serialutil.SerialException:
            return False

    def __read(self):

        self.__stop_thread = False
        self.__payloads = []
        
        x_conf_pack = IBCMbConfPayloadS(
            baud_rate=self.__serial_port.baudrate,
            ul_dt_us=10000,
            el_pack_id_for_default_request=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvSendAllData
        )
        controller_setting_command = x_conf_pack.generate_hex(
            sender_id=CAServicesIDE.CA_ID_iBCM,
            recipient_id=CAServicesIDE.CA_ID_iBCM,
            pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
            crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
        )

        self.__serial_port.write(controller_setting_command)
        time.sleep(0.2)

        x_conf_pack = IBCMReconfigCMDt(
            is_need_reconfig=1
        )

        controller_set_command = x_conf_pack.generate_hex(
            sender_id=CAServicesIDE.CA_ID_iBCM,
            recipient_id=CAServicesIDE.CA_ID_iBCM,
            pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
            crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
        )

        self.__serial_port.write(controller_set_command)
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
                # УДАЛИТЬ НА ПРОДЕ
                temp_data = IBCMAllMeasPayloads(data)
                print(temp_data.aGyr)
                print(temp_data.aAcc)
                print(temp_data.gyrAccTemperature)
                print(temp_data.aMag)
                print(temp_data.gyrAccTemperature)
                print(temp_data.controlSumm)
                # ДАЛЬШЕ УДАЛЯТЬ НЕ НАДО

        else:

            x_conf_pack = IBCMbConfPayloadS(
                baud_rate=self.__serial_port.baudrate,
                ul_dt_us=0,
                el_pack_id_for_default_request=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvSendAllData
            )
            controller_setting_command = x_conf_pack.generate_hex(
                sender_id=CAServicesIDE.CA_ID_iBCM,
                recipient_id=CAServicesIDE.CA_ID_iBCM,
                pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
                crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
            )

            self.__serial_port.write(controller_setting_command)
            time.sleep(0.2)

            x_conf_pack = IBCMReconfigCMDt(
                is_need_reconfig=1
            )

            controller_set_command = x_conf_pack.generate_hex(
                sender_id=CAServicesIDE.CA_ID_iBCM,
                recipient_id=CAServicesIDE.CA_ID_iBCM,
                pack_id=IBCMParseMessageAPIE.iBCM_PARSE_MESSAGE_API_prvReadConfPack,
                crc_type=CaCrcType.SFH_CRC_TYPE_SIZE_32BIT
            )

            self.__serial_port.write(controller_set_command)

            self.__serial_port.close()
            time.sleep(0.2)

    def connect(self):
        try:
            self.__serial_port.open()
            return self.__serial_port.is_open()
        except serial.serialutil.SerialException:
            return False

    def start_read(self):
        if self.__serial_port.isOpen():
            self.__reading_thread = threading.Thread(target=self.__read, daemon=True)
            self.__reading_thread.start()
            print(self.__reading_thread)
            return True
        else:
            return False

    def stop_read(self):
        print(self.__reading_thread)
        self.__stop_thread = True
        self.__reading_thread.join()
        return self.__payloads


main_bus = PortReader()
payloads = []
while True:
    print("1. Настроить порт и скорость передачи")
    print("2. Начать чтение")
    print("3. Закончить чтение")
    print("4. Вывести считанные данные")
    print("5. Выход")
    choose = int(input("Ваш выбор: "))
    if choose == 1:
        com_port = input("Введите COM порт (например: COM12): ")
        speed = int(input("Введите скорость передачи (например: 115200): "))
        result = main_bus.set_port(com_port, speed)
        if result:
            print("Успешное подключение!")
        else:
            print("Не подключено")
    elif choose == 2:
        result = main_bus.start_read()
        if result:
            print("Чтение началось")
        else:
            print("Чтение не началось")
    elif choose == 3:
        payloads = main_bus.stop_read()
    elif choose == 4:
        for payload in payloads:
            print(payload.header)
            print(payload.timeStamp)
            print(payload.statusFlags)
            print(payload.ulDt_us)
            print(payload.aGyr)
            print(payload.aAcc)
            print(payload.gyrAccTemperature)
            print(payload.aMag)
            print(payload.gyrAccTemperature)
            print(payload.controlSumm)
            print("-" * 64)
    else:
        break
