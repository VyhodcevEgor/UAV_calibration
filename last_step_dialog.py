from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('lastStepDialog.ui', self)

        self.return_to_last = False

        self.noButton.clicked.connect(self.back_to_last_step)
        self.yesButton.clicked.connect(self.close)

    def back_to_last_step(self):
        self.return_to_last = True
        self.close()

def show_dialog():
    dialog = Dialog()

    result = dialog.exec()
    return dialog.return_to_last