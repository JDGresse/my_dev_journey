import os
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

def welcome_select(ui_dir):
    
    class Welcome(QWidget):
        def __init__(self):
            super(Welcome, self).__init__()
            loadUi(f'{ui_dir}welcome.ui', self)

            icon = QIcon(f'{ui_dir}0_icon.ico')
            self.setWindowIcon(icon) 
            
            self.pushButtonProceed.clicked.connect(self.result)
                         
    #if __name__ == '__main__':
                            
    app = QApplication(sys.argv)
    welcome_window = Welcome()
    welcome_window.show()
    app.exec_()