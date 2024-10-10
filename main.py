from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import openpyxl
import sys
import os

import bookmark

ID_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\ID.txt'
PASS_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\PASS.txt'

def read(path):
    with open(path, 'r') as file:
        return file.read()
def write(path, text):
    with open(path, 'w') as file:
        file.write(text)

def check_file(path):
    try:
        df = pd.read_excel(path, sheet_name=0, engine='openpyxl')
    except Exception as e:
        print(f'FILE ERROR::file import error - {e}')
        return 0
    
    if len(df.columns) != 4:
        print('FILE ERROR::data column size is not 4')
        return 0
    
    for index, row in df.iterrows():
        for col in range(4):
            if pd.isna(row.iloc[col]):
                print(f'FILE ERROR::Row {index + 2}, Column {col + 1} is empty.')
                return 0
    
    return df.size // 4

class Window(QWidget):
    def update_filePath(self, path):
        size = check_file(path)
        if size != 0:
            self.line_filepath.setText(path)
            self.lbl_count.setText(f'Count : {str(size).zfill(3)}')

    def __init__(self):
        super().__init__()
        self.UIinit()
    
    def UIinit(self):
        self.setFixedSize(500, 340) 
        self.setWindowTitle('Kakaomap Auto Bookmarking')
        grid = QGridLayout()

        self.gb_loginInfo = self.createGroup_loginInfo()
        self.gb_file = self.createGroup_file()
        self.gb_execution = self.createGroup_execution()

        grid.addWidget(self.gb_loginInfo, 0, 0)
        grid.addWidget(self.gb_file, 1, 0)
        grid.addWidget(self.gb_execution, 2, 0)

        self.setLayout(grid)

    def createGroup_loginInfo(self):
        groupbox = QGroupBox('Kakao Login Info')

        hbox_ID_PASS = QHBoxLayout()
        lbl_ID = QLabel('ID : ', self)
        lbl_PASS = QLabel('Password : ', self)
        self.line_ID = QLineEdit(read(ID_path), self)
        self.line_PASS = QLineEdit(read(PASS_path), self)
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
    def createGroup_file(self):
        groupbox = QGroupBox('File')

        lbl_format_guid = QLabel('<b>EXCEL FORMAT : [index|Name|Address|Count]</b>', self)

        self.line_filepath = QLineEdit(self)
        self.line_filepath.setReadOnly(True)

        self.lbl_count = QLabel('Count : ---', self)

        btn_selectFile = QPushButton('Import File (.excel)', self)
        btn_selectFile.clicked.connect(self.btn_selectFile_function)

        hbox = QHBoxLayout()
        hbox.addWidget(btn_selectFile)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_format_guid)
        vbox.addWidget(self.line_filepath)
        vbox.addWidget(self.lbl_count)
        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox
    def createGroup_execution(self):
        groupbox = QGroupBox('Execution')

        btn_start = QPushButton('Start', self)
        btn_start.clicked.connect(self.btn_start_function)

        lbl_color = QLabel('Color', self)

        self.cb_color = QComboBox(self)
        for color in bookmark.color_List:
            self.cb_color.addItem(str(color))
        self.cb_color.setCurrentText(bookmark.color_List[0])

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_color)
        hbox.addWidget(self.cb_color)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(btn_start)

        groupbox.setLayout(vbox)
        return groupbox

    def btn_edit_function(self):
        self.gb_file.setEnabled(False)
        self.gb_execution.setEnabled(False)
        self.btn_edit.setEnabled(False)
        self.btn_save.setEnabled(True)
        self.line_ID.setEnabled(True)
        self.line_PASS.setEnabled(True)
        self.line_PASS.setEchoMode(QLineEdit.Normal)
    def btn_save_function(self):
        self.gb_file.setEnabled(True)
        self.gb_execution.setEnabled(True)
        self.btn_edit.setEnabled(True)
        self.btn_save.setEnabled(False)
        self.line_ID.setEnabled(False)
        self.line_PASS.setEnabled(False)
        self.line_PASS.setEchoMode(QLineEdit.Password)
        write(ID_path, self.line_ID.text())
        write(PASS_path, self.line_PASS.text())
    def btn_selectFile_function(self):
        fname = QFileDialog.getOpenFileName(self, '파일선택', '', 'AllFiles(*.xlsx *.xls)')
        self.update_filePath(fname[0])
    def btn_start_function(self):
        bookmark.start(self.line_ID.text(), self.line_PASS.text(), color=self.cb_color.currentText(), filePath=self.line_filepath.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())