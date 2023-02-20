from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from serial.tools import list_ports
import sys
import json
import error


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('untitled.ui', self)

        # Здесь определяются свойства для хранения временных данных
        self.open_com = True
        self.console_opened = True
        self.progress_value = 0
        self.matrix = [[4, 1, 5, 6, 3, 6], [4, 1, 5, 6, 3, 6], [4, 1, 5, 6, 3, 6]]
        self.magnetic_declination = 0 # магнетическое склонение
        self.accelerometer_allowance = 0 # допуски отклонений
        self.gyroscope_allowance = 0
        self.magnetometer_allowance = 0

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

        types = ['Тип 1', 'Тип 2']
        views = ['Акселерометр', 'Гироскоп', 'Магнитометр']
        self.ports = list_ports.comports()
        port_names = [port.name for port in self.ports]
        speeds = ['115200']

        # Заполнение необходимых полей при инициализации
        self.eqvType.addItems(types)
        self.eqvView.addItems(views)
        self.comPort.addItems(port_names)
        self.speedMean.addItems(speeds)
        self.comName.setText('')

    """Данный метод используется для открытия и закрытия консоли"""
    def open_close_console(self):
        self.console_opened = not self.console_opened

        if self.console_opened:
            self.consoleButton.setText('Закрыть консоль')
            self.consoleText.show()
            self.setGeometry(50, 50, 800, 600)
        else:
            self.consoleButton.setText('Открыть консоль')
            self.consoleText.hide()
            self.setGeometry(50, 50, 800, 330)

        print(self.consoleButton)

    """Данный метод начинает выполнение колибровки при нажатии на соответствующую кнопку"""
    def start_calibration(self):
        # Сохранение выбранных пользователем данных
        self.magnetic_declination = self.magneticDeclination.value()
        self.accelerometer_allowance = self.accelerometerAllowance.value()
        self.gyroscope_allowance = self.gyroscopeAllowance.value()
        self.magnetometer_allowance = self.magnetometerAllowance.value()

        # Инициализация виджета прогресса калибровки
        self.progressBar.setValue(self.progress_value)
        self.resultsWidjet.hide()
        self.progress_value = 0
        self.calibrationWidjet.show()

    """Данный метод выполняется каждый раз когда пользователь продолжает колибровку данных"""
    def continue_calibration(self):
        self.progress_value += 25
        self.progressBar.setValue(self.progress_value)
        if self.progress_value == 100:
            self.calibrationWidjet.hide()
            self.resultsWidjet.show()
            self.show_calculated_matrix()

    """Этот метод отвечает за вывод готовой вычисленной матрицы для устройства, которую
    возможно перенести в оперативную или в постаянную память устройства"""
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
        text = ''
        for mat_str in self.matrix:
            for elem in mat_str:
                text += str(elem) + '  '
            text += '\n\n'
        self.equipmentText.setText(text)

    """Этот метод используется для записи вычесленых данный в постоянную память устройства"""
    def save_in_equipment(self):
        text = ''
        for mat_str in self.matrix:
            for elem in mat_str:
                text += str(elem) + '  '
            text += '\n\n'
        self.equipmentText.setText(text)

    """Данный метод используется для открытия и закрытия общения с COM портом"""
    def open_close_com_port(self):
        if self.open_com:
            self.openCloseCom.setText('Закрыть порт')

            port_description = self.ports[self.comPort.currentIndex()].description

            self.comName.setText(port_description)
        else:
            self.openCloseCom.setText('Открыть порт')
            self.comName.setText('')
        self.open_com = not self.open_com

    """Данный метод формирует структуру json и сохраняет её в файл. В структуре
    находятся вычисленные калибровочные матрицы"""
    def save_matrix_in_file(self):
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

    """Этот метод читает файл типа json и сохраняет матрицу которая содержалась в нем"""
    def load_matrix_from_file(self):
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
                except:
                    message = 'Файл не содержит подходящего поля. Убедитесь' \
                              ' что матрица присвоена свойству matrix'
                    error.show_error(message)
                    return


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
