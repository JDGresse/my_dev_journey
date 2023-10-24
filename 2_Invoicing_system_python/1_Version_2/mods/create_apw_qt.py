import sys
import os
import hashlib
import pickle
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget

def set_apw():

    current_dir = os.getcwd()
    ui_dir = current_dir + '\\lib\\ui\\'
    dat_dir = current_dir + '\\lib\\dat\\'
          
    class AdminScreen(QDialog):
        def __init__(self):
            super().__init__()
            loadUi(f'{ui_dir}apw_dialog.ui',self)
            
            self.set_apw.clicked.connect(self.set_pw)
            
        def set_pw(self):
            # No pw
            if self.apw_1.text() == '' or self.apw_2.text() == '':
                some_text = 'Please add a valid password before proceeding!'
                self.err_message.setText(some_text)
            
            # No match
            elif self.apw_1.text() != self.apw_2.text():  
                some_text = 'Passwords do not match, please retpye carefully!'
                self.err_message.setText(some_text)
            
            # Match
            elif self.apw_1.text() == self.apw_2.text():
                some_text = 'Administrator password set!'
                self.err_message.setText(some_text)
                
                apw = hashlib.sha256(self.apw_1.text().encode()).hexdigest()
                
                save_apw = open(f'{dat_dir}apw.dat','wb')
                pickle.dump(apw, save_apw)
                save_apw.close()
                
                app.__exit__
                
    #if __name__ == "__main__":
        
    app = QApplication(sys.argv)
    
    stacked_widget = QStackedWidget()
    
    admin = AdminScreen()
    
    stacked_widget.addWidget(admin)
    
    stacked_widget.setCurrentIndex(0)
    
    stacked_widget.setFixedSize(375, 280)
    
    stacked_widget.show()
    
    try:
        sys.exit(app.exec_())
    except:
        app.exit()
            