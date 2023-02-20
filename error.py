from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class Dialog(QDialog):
    def __init__(self, message):
        super(Dialog, self).__init__()
        uic.loadUi('error.ui', self)

        self.errorMessage.setText(message)
        self.okButton.clicked.connect(self.close)


def show_error(message):
    dialog = Dialog(message)

    dialog.exec()
