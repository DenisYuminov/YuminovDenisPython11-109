import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt6 import uic


class Main(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("calculate.ui", self)
        self.gui()
        self.logic()

    def get_btns(self):
        btns = [
            self.btn_1,
            self.btn_2,
            self.btn_3,
            self.btn_4,
            self.btn_5,
            self.btn_6,
            self.btn_7,
            self.btn_8,
            self.btn_9,
            self.btn_0,
            self.btn_plus,
            self.btn_mp,
            self.btn_div,
            self.btn_sub
        ]
        for btn in btns:
            btn.clicked.connect(lambda state, value=btn.text(): self.send_data(value))

    def logic(self):
        self.get_btns()
        self.btn_C.clicked.connect(self.clear)
        self.btn_eq.clicked.connect(self.answer)
        self.label.setText("")

    def gui(self):
        self.lineEdit: QTextEdit
        self.label: QLabel
        uic.loadUi('calculate.ui', self)
        self.show()

    def send_data(self, value):
        oper = ('+', '-', '/', '*')
        if value in oper and self.label.text()[-1] not in oper:
            self.label.setText(self.label.text() + value)
        elif value not in oper:
            self.label.setText(self.label.text() + value)

    def clear(self):
        self.label.setText("")

    def answer(self):
        res = str(eval(self.label.text()))
        self.label.setText(res)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())