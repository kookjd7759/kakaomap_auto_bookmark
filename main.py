from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import openpyxl
import sys
import os

import bookmark
import db 

ID_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\ID.txt'
PASS_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\PASS.txt'
ico_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\ico.png'

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

class Warning(QDialog):
    def __init__(self, parent, key):
        super().__init__(parent)
        self.initUI(key)
    def initUI(self, key):
        self.setFixedSize(150, 100)
        self.setWindowTitle('Warning')
        label = QLabel(self.text(key), self)
        label.setAlignment(Qt.AlignCenter)

        btn = QPushButton('Ok', self)
        btn.clicked.connect(self.close)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(btn)
        self.setLayout(vbox)

    def text(self, key):
        if key == 'ID' or key == 'PASS':
            return f'Enter your {key}'
        else: # key == FILE
            return f'Import excel file'

class Window(QWidget):
    def update_filePath(self, path):
        size = check_file(path)
        if size != 0:
            self.line_filepath.setText(path)
            self.lbl_count.setText(f'Count : {str(size).zfill(3)}')
    def update_color(self):
        db.write_color(self.get_color())
    def update_group(self):
        db.write_group(self.cb_group.currentText())

    def __init__(self):
        super().__init__()
        self.UIinit()
    def UIinit(self):
        self.setFixedSize(500, 380) 
        self.setWindowTitle('Kakaomap Auto Bookmarking')
        self.setWindowIcon(QIcon(ico_path))
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
        self.line_ID = QLineEdit(db.read(ID_path), self)
        self.line_PASS = QLineEdit(db.read(PASS_path), self)
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

        btn_selectFile = QPushButton('Import File (excel)', self)
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

        lbl_color = QLabel('BookMark Color     ', self)
        
        hbox_color = QHBoxLayout()
        hbox_color.addWidget(lbl_color)
        self.radio_buttons = []
        for i in range(len(bookmark.color_List)):
            radio_button = QRadioButton()
            radio_button.setStyleSheet(f'''
                QRadioButton::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 10px;
                    background-color: {bookmark.color_List[i]};
                }}
                QRadioButton::indicator:checked {{
                    width: 12px;
                    height: 12px;
                    border-radius: 10px;
                    border: 4px solid {bookmark.color_List[i]};
                    background-color: transparent;
                }}
            ''')
            hbox_color.addWidget(radio_button)
            radio_button.clicked.connect(self.update_color)
            self.radio_buttons.append(radio_button)

            if i == db.read_color():
                radio_button.setChecked(True)

        lbl_group = QLabel('BookMark Group', self)
        self.cb_group = QComboBox(self)
        for group in [1,2,3,4,5,6,7,8,9,10]:
            self.cb_group.addItem(str(group))
        self.cb_group.setCurrentIndex(db.read_group() - 1)
        self.cb_group.currentIndexChanged.connect(self.update_group)
        hbox_group = QHBoxLayout()
        hbox_group.addWidget(lbl_group)
        hbox_group.addWidget(self.cb_group)

        lbl_warning_msg = QLabel('선택된 그룹에 이미 즐겨찾기가 존재하는 경우, 오류가 발생할 수 있습니다.', self)
        lbl_warning_msg.setStyleSheet( 'QLabel { font-size: 12px; color: red; }')
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_color)
        vbox.addLayout(hbox_group)
        vbox.addWidget(lbl_warning_msg)
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
        db.write(ID_path, self.line_ID.text())
        db.write(PASS_path, self.line_PASS.text())
    def btn_selectFile_function(self):
        fname = QFileDialog.getOpenFileName(self, '파일선택', '', 'AllFiles(*.xlsx *.xls)')
        self.update_filePath(fname[0])
    def btn_start_function(self):
        if self.start_check() == '':
            bookmark.start(self.line_ID.text(), self.line_PASS.text(), self.get_color(), self.line_filepath.text(), int(self.cb_group.currentText()))
        else:
            warning = Warning(self, self.start_check())
            warning.exec_()

    def start_check(self):
        if self.line_ID.text() == '':
            print(f'START ERROR::kakao ID is empty')
            return 'ID'
        elif self.line_PASS.text() == '':
            print(f'START ERROR::kakao Password is empty')
            return 'PASS'
        elif self.line_filepath.text() == '':
            print(f'START ERROR::there is no file')
            return 'FILE'
        return ''

    def get_color(self):
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                return i

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())