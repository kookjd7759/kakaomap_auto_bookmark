from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pubsub import pub
import sys

class Window(QWidget):
### Window initalize
    def __init__(self):
        super().__init__()
        self.UIinit()
    
    def UIinit(self):
        self.setFixedSize(500, 500) 
        self.setWindowTitle('Kakaomap Auto Bookmarking')
        grid = QGridLayout()
        grid.addWidget(self.createGroup_LoginInfo(), 0, 0)

        self.setLayout(grid)

    def createGroup_LoginInfo(self):
        groupbox = QGroupBox('Kakao Login Info')

        hbox_ID_PASS = QHBoxLayout()
        lbl_ID = QLabel('ID : ', self)
        lbl_PASS = QLabel('Password : ', self)
        self.line_ID = QLineEdit('', self)
        self.line_PASS = QLineEdit('', self)
        self.line_PASS.setEchoMode(QLineEdit.Password)
        self.line_ID.setEnabled(False)
        self.line_PASS.setEnabled(False)
        hbox_ID_PASS.addWidget(lbl_ID)
        hbox_ID_PASS.addWidget(self.line_ID)
        hbox_ID_PASS.addWidget(lbl_PASS)
        hbox_ID_PASS.addWidget(self.line_PASS)
        
        hbox_edit_save = QHBoxLayout()
        self.btn_edit = QPushButton('Edit', self)
        self.btn_save = QPushButton('Save', self)
        self.btn_edit.setEnabled(True)
        self.btn_save.setEnabled(False)
        self.btn_edit.clicked.connect(self.btn_edit_function)
        self.btn_save.clicked.connect(self.btn_save_function)
        hbox_edit_save.addWidget(self.btn_edit)
        hbox_edit_save.addWidget(self.btn_save)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_ID_PASS)
        vbox.addLayout(hbox_edit_save)

        groupbox.setLayout(vbox)
        return groupbox

    def btn_edit_function(self):
        self.btn_edit.setEnabled(False)
        self.btn_save.setEnabled(True)
        self.line_ID.setEnabled(True)
        self.line_PASS.setEnabled(True)
        self.line_PASS.setEchoMode(QLineEdit.Normal)
    def btn_save_function(self):
        self.btn_edit.setEnabled(True)
        self.btn_save.setEnabled(False)
        self.line_ID.setEnabled(False)
        self.line_PASS.setEnabled(False)
        self.line_PASS.setEchoMode(QLineEdit.Password)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())