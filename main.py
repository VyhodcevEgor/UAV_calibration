from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from DataTypes import SensorIndicatorType as indicT
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsScene
import serial
import serial.tools.list_ports as list_ports
import sys
import json
import error
import accelerometer as accel
import magnetometer as magnet
import SerialPortReader as ports
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('untitled.ui', self)

        # Здесь определяются свойства для хранения временных данных или констант
        self.open_com = True
        self.console_opened = True
        self.progress_value = 0
        self.progress_addition = {
            indicT.Acc: 16.7,
            indicT.Gyr: 16.7,
            indicT.Mag: 4.2
        }
        self.matrix = [[4, 1, 5, 6, 3, 6], [4, 1, 5, 6, 3, 6], [4, 1, 5, 6, 3, 6]]
        self.position_data = []
        self.magnetic_declination = 0 # магнетическое склонение
        self.accelerometer_allowance = 0 # допуск отклонений акселерометра
        self.gyroscope_allowance = 0 # допуск отклонений гироскопа
        self.magnetometer_allowance = 0 # допуск отклонений магнитометра
        self.max_allowance = 0 # допустимая погрешность калибровки
        self.port_reader = ports.PortReader()
        self.sleeping_time = 0.5
        self.current_step_num = 1
        self.reload_calib = False

        # Скрытие и отображение виджитов при инициализации
        if not self.console_opened:
            self.consoleButton.setText('Закрыть консоль')
            self.consoleText.hide()
        self.resultsWidjet.hide()
        self.calibrationWidjet.hide()

        # Присоединение методов к событиям
        self.consoleButton.clicked.connect(self.open_close_console)
        self.startButton.clicked.connect(self.start_calibration)
        self.continueButton.clicked.connect(self.continue_calibration)
        self.transferButton.clicked.connect(self.transfer_data)
        self.transferPZUButton.clicked.connect(self.save_in_equipment)
        self.openCloseCom.clicked.connect(self.open_close_com_port)
        self.actionSave.triggered.connect(self.save_matrix_in_file)
        self.actionLoad.triggered.connect(self.load_matrix_from_file)
        self.reloadButton.clicked.connect(self.serial_ports)
        self.backButton.clicked.connect(self.remove_last_step)

        views = [indicT.Acc, indicT.Gyr, indicT.Mag]
        self.serial_ports()
        speeds = ['115200']

        # Заполнение необходимых полей при инициализации
        self.eqvView.addItems(views)
        self.speedMean.addItems(speeds)
        self.comName.setText('')
        self.accelerometerAllowance.setValue(0.3)
        self.gyroscopeAllowance.setValue(0.3)
        self.magnetometerAllowance.setValue(0.3)
        self.maxAllowance.setValue(0.3)
        self.magneticDeclination.setValue(58)

        self.consoleText.setText('Программа запущена и готова к работе.')

    """Получение списка доступных портов"""
    def serial_ports(self):
        self.consoleText.setText('Список COM портов обновляется.')
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.comPort.clear()
        self.comPort.addItems(result)
        self.consoleText.setText('Список COM портов обновлен.')

    """Данный метод используется для открытия и закрытия консоли"""
    def open_close_console(self):
        self.console_opened = not self.console_opened

        if self.console_opened:
            self.consoleButton.setText('Закрыть консоль')
            self.consoleText.show()
            self.resize(1108, 554)
        else:
            self.consoleButton.setText('Открыть консоль')
            self.consoleText.hide()
            self.resize(800, 554)

    def get_image(self, pos_num):
        current_indic = self.eqvView.currentText()

        match current_indic:
            case indicT.Acc:
                image = f'./assets/accAndGyr/{pos_num}.jpeg'
            case indicT.Mag:
                print('Dumbass')
            case indicT.Gyr:
                image = f'./assets/accAndGyr/{pos_num}.jpeg'
        img = QPixmap(image)

        return img

    """Данный метод начинает выполнение калибровки при нажатии на соответствующую кнопку"""
    def start_calibration(self):
        if not self.reload_calib:
            self.consoleText.setText('Калибровка началась.')
            self.reload_calib = True
        else:
            self.consoleText.setText('Калибровка перезапущена.')

        self.progress_value = 0

        # Сохранение выбранных пользователем данных
        self.magnetic_declination = self.magneticDeclination.value()
        self.accelerometer_allowance = self.accelerometerAllowance.value()
        self.gyroscope_allowance = self.gyroscopeAllowance.value()
        self.magnetometer_allowance = self.magnetometerAllowance.value()
        self.max_allowance = self.maxAllowance.value()

        # Инициализация виджета прогресса калибровки
        self.progressBar.setValue(self.progress_value)
        self.resultsWidjet.hide()
        self.calibrationWidjet.show()

        self.indicPosition.setPixmap(self.get_image(self.current_step_num))
        self.current_step_num += 1

    """Данный метод выполняется каждый раз когда пользователь продолжает колибровку данных"""
    def continue_calibration(self):
        # Начало чтения порта
        raw_dim = self.port_reader.read_sensor_calibration_data(self.eqvView.currentText())
        if raw_dim is not None:
            self.position_data.append(accel.form_row(raw_dim))
        else:
            message = 'Данные не могут быть получены'
            error.show_error(message)
            self.consoleText.setText('Данные не могут быть получены.')
            return

        self.progress_value += self.progress_addition[self.eqvView.currentText()]
        self.progressBar.setValue(int(self.progress_value))

        if self.progress_value >= 100:
            self.consoleText.setText('Начался расчет матриц.')
            current_indic = self.eqvView.currentText()

            # Расчет матрицы калибровки для определенного типа датчика
            match current_indic:
                # Расчет для акселерометра
                case indicT.Acc:
                    raw_data = accel.form_raw_data(self.position_data)
                    self.matrix = accel.calibrate_accelerometer(raw_data, self.max_allowance,
                                                                self.accelerometer_allowance)
                # Расчет для магнитометра
                case indicT.Mag:
                    ideal_matrix = magnet.form_ideal_matrix(self.magnetometer_allowance)
                    raw_data = magnet.form_raw_data(self.position_data)
                    self.matrix = magnet.calibrate_magnetometer(raw_data, ideal_matrix, self.max_allowance,
                                                                self.magnetometer_allowance)
                # Расчет для гироскопа
                case indicT.Gyr:
                    print('Dumbass')

            self.reload_calib = False
            self.calibrationWidjet.hide()

            if self.matrix is not None:
                self.consoleText.setText('Расчет матриц завершен.')
                self.resultsWidjet.show()
                self.show_calculated_matrix()
            else:
                message = 'Расчет матриц не может быть произведен'
                error.show_error(message)
                self.consoleText.setText(message)


    """Этот метод отвечает за вывод готовой вычисленной матрицы для устройства, которую
    возможно перенести в оперативную или в постоянную память устройства"""
    def show_calculated_matrix(self):
        text = ''
        for mat_str in self.matrix:
            for elem in mat_str:
                text += str(elem) + '  '
            text += '\n\n'
        self.calculatedText.setText(text)

    """Этот метод отвечает за перенос вычисленных данных в оперативную память устройства
    для которого производилась калибровка"""
    def transfer_data(self):
        self.consoleText.setText('Перенос данных в оперативную память устройства.')
        text = ''
        for mat_str in self.matrix:
            for elem in mat_str:
                text += str(elem) + '  '
            text += '\n\n'
        self.equipmentText.setText(text)
        self.consoleText.setText('Данные перенесены в оперативную память устройства.')

    """Этот метод используется для записи вычесленых данный в постоянную память устройства"""
    def save_in_equipment(self):
        self.consoleText.setText('Сохранение данных в ПЗУ датчика.')
        text = ''
        for mat_str in self.matrix:
            for elem in mat_str:
                text += str(elem) + '  '
            text += '\n\n'
        self.equipmentText.setText(text)
        self.consoleText.setText('Данные сохранены в ПЗУ датчика')

    """Данный метод используется для открытия и закрытия общения с COM портом"""
    def open_close_com_port(self):
        if self.open_com:
            self.consoleText.setText('Открытие COM порта.')
            # Настройки порта
            port = self.comPort.currentText()
            baud_rate = self.speedMean.currentText()
            port_seted = self.port_reader.set_port(port, baud_rate)
            if not port_seted:
                message = 'Настройки порта не могут быть совершены'
                error.show_error(message)
                self.consoleText.setText('Настройки порта не могут быть совершены')
                return

            #Открытие порта для работы с ним
            port_opened = self.port_reader.connect()
            if not port_opened:
                message = 'Открыть порт для работы не возможно, проверьте его доступность'
                error.show_error(message)
                self.consoleText.setText('Открыть порт для работы не возможно, проверьте его доступность')
                return
            else:
                self.openCloseCom.setText('Закрыть порт')
                port_description = port
                self.comName.setText(port_description)
                self.consoleText.setText('COM порт открыт успешно.')
        else:
            self.consoleText.setText('Закрытие COM порта.')
            self.openCloseCom.setText('Открыть порт')
            self.comName.setText('')
            port_closed = self.port_reader.close_port()
            if not port_closed:
                message = 'Порт не может быть закрыт'
                error.show_error(message)
                self.consoleText.setText('Порт не может быть закрыт.')
            else:
                self.openCloseCom.setText('Открыть порт')
                self.comName.setText('')
                self.consoleText.setText('Порт успешно закрыт.')

        self.open_com = not self.open_com

    """Данный метод формирует структуру json и сохраняет её в файл. В структуре
    находятся вычисленные калибровочные матрицы"""
    def save_matrix_in_file(self):
        self.consoleText.setText('Сохранение матрицы в файл.')
        if len(self.matrix) == 0:
            message = 'Калибровочная матрица ещё не вычеслена или не загружена'
            error.show_error(message)
            return
        matrix_json = {'matrix': self.matrix}

        dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', 'untitled.json',
                                                       'Json (*.json)')
        url = dialog[0]
        if not url == '':
            with open(url, 'w') as outfile:
                json.dump(matrix_json, outfile)
        self.consoleText.setText(f'Матрица сохранена в файл: {url}.')

    """Этот метод читает файл типа json и сохраняет матрицу которая содержалась в нем"""
    def load_matrix_from_file(self):
        self.consoleText.setText('Чтение матрицы из файла.')
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', None,
                                                       'Json (*.json)')
        url = dialog[0]
        if not url == '':
            with open(url) as json_file:
                try:
                    data = json.load(json_file)
                except:
                    message = 'Структура файла не соответствует стандарту json'
                    error.show_error(message)
                    return

                try:
                    self.matrix = data['matrix']
                    self.consoleText.setText('Матрица успешно прочитана из файла.')
                except:
                    message = 'Файл не содержит подходящего поля. Убедитесь' \
                              ' что матрица присвоена свойству matrix'
                    error.show_error(message)
                    return

    def remove_last_step(self):
        try:
            last_mean = self.position_data.pop()
            self.consoleText.setText(f'Значение удалено: \n{last_mean}')
        except:
            message = 'Это первый шаг, повторите действия изображенные на рисунке и нажмите кнопку "Далее"'
            error.show_error(message)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
