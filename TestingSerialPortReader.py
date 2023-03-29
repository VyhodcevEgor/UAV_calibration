import unittest
from SerialPortReader import PortReader
from DataTypes import SensorIndicatorType
from DataTypes import IBCMAllMeasPayloads
import time as t
import serial


class TestSerial(unittest.TestCase):
    def setUp(self):
        self.reader = PortReader()

    def test_set_port_1(self):
        d = self.reader.set_port("COM2", 115200)
        self.assertTrue(d)
        self.reader.close_port()

    def test_set_port_2(self):
        d = self.reader.set_port("SJAH", 115200)
        self.assertFalse(d)
        self.reader.close_port()

    def test_connect_1(self):
        self.reader.set_port("COM2", 115200)
        d = self.reader.connect()
        self.assertTrue(d)
        self.reader.close_port()

    def test_connect_2(self):
        self.reader.set_port("COM", 115200)
        d = self.reader.connect()
        self.assertFalse(d)
        self.reader.close_port()

    def test_connect_3(self):
        self.reader.set_port("COM2", 1)
        d = self.reader.connect()
        self.assertTrue(d)
        self.reader.close_port()

    def test_close_port(self):
        self.reader.set_port("COM2", 115200)
        self.reader.connect()
        t.sleep(0.1)
        self.assertTrue(self.reader.close_port())

    def test_start_read(self):
        self.reader.set_port("COM2", 115200)
        self.reader.connect()
        t.sleep(0.1)
        self.assertTrue(self.reader.start_read(SensorIndicatorType.Acc))
        t.sleep(0.1)
        self.assertTrue(self.reader.close_port())

    def test_reading_Acc(self):
        self.reader.set_port("COM2", 115200)
        self.reader.connect()
        t.sleep(0.1)
        self.assertTrue(self.reader.start_read(SensorIndicatorType.Acc))

        temp_hex = "AAAA0300070000000400000038000000410100000000000006000000513514BC363C51BB86CC" \
                   "BF3B0000A2BD000048BC00E07E3F50D10842728A0EBFBBB8ADBE8738C63E000000009710777D"

        com_port = "COM4"
        baud_rate = 115200

        data = IBCMAllMeasPayloads(bytes.fromhex(temp_hex))
        t.sleep(0.1)
        with serial.Serial(port=com_port, baudrate=baud_rate) as test_serial_port:
            data.reset_values([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
            if not test_serial_port.isOpen():
                test_serial_port.open()
            if test_serial_port.isOpen():
                test_serial_port.write(data.generate_hex())
            test_serial_port.close()
        t.sleep(5)
        self.assertEqual(self.reader.stop_read(), [[4.0, 5.0, 6.0]])
        self.assertTrue(self.reader.close_port())

    def test_reading_Gyr(self):
        self.reader.set_port("COM2", 115200)
        self.reader.connect()
        t.sleep(0.1)
        self.assertTrue(self.reader.start_read(SensorIndicatorType.Gyr))

        temp_hex = "AAAA0300070000000400000038000000410100000000000006000000513514BC363C51BB86CC" \
                   "BF3B0000A2BD000048BC00E07E3F50D10842728A0EBFBBB8ADBE8738C63E000000009710777D"

        com_port = "COM4"
        baud_rate = 115200

        data = IBCMAllMeasPayloads(bytes.fromhex(temp_hex))
        t.sleep(0.1)
        with serial.Serial(port=com_port, baudrate=baud_rate) as test_serial_port:
            data.reset_values([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
            if not test_serial_port.isOpen():
                test_serial_port.open()
            if test_serial_port.isOpen():
                test_serial_port.write(data.generate_hex())
            test_serial_port.close()
        t.sleep(5)
        self.assertEqual(self.reader.stop_read(), [[1.0, 2.0, 3.0]])
        self.assertTrue(self.reader.close_port())

    def test_reading_Mag(self):
        self.reader.set_port("COM2", 115200)
        self.reader.connect()
        t.sleep(0.1)
        self.assertTrue(self.reader.start_read(SensorIndicatorType.Mag))

        temp_hex = "AAAA0300070000000400000038000000410100000000000006000000513514BC363C51BB86CC" \
                   "BF3B0000A2BD000048BC00E07E3F50D10842728A0EBFBBB8ADBE8738C63E000000009710777D"

        com_port = "COM4"
        baud_rate = 115200

        data = IBCMAllMeasPayloads(bytes.fromhex(temp_hex))
        t.sleep(0.1)
        with serial.Serial(port=com_port, baudrate=baud_rate) as test_serial_port:
            data.reset_values([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0])
            if not test_serial_port.isOpen():
                test_serial_port.open()
            if test_serial_port.isOpen():
                test_serial_port.write(data.generate_hex())
            test_serial_port.close()
        t.sleep(5)
        self.assertEqual(self.reader.stop_read(), [[7.0, 8.0, 9.0]])
        self.assertTrue(self.reader.close_port())


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
