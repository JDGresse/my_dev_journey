# Import libraries
import re
import pickle
import subprocess
import locale
import os
import io
import sys
from datetime import date
from multiprocessing import Value
from tokenize import group
import PySimpleGUI as sg
from PyPDF2 import PdfWriter, PdfReader, Transformation
from reportlab.pdfgen.canvas import Canvas
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
###

# Import modules
current_dir = os.getcwd()
mod_dir = current_dir + '\\\\mods\\'
ui_dir = current_dir + '\\lib\\ui\\'
dat_dir = current_dir + '\\lib\\dat\\'
dll_dir = current_dir + '\\lib\\dll\\'
media_dir = current_dir + '\\lib\\media\\'

path_list = [mod_dir, ui_dir, dat_dir, dll_dir]

for path in path_list:
    sys.path.append(path)

from mods.save_the_date import std

# Set locale to RSA english
locale.setlocale(locale.LC_ALL, 'en_ZA')
locale._override_localeconv = {'mon_thousands_sep':',','currency_symbol': 'R '}
###

# Global variables
bank_codes = {'ABSA Bank':'632 005', 'Bank of Athens':'410 506','Bidvest Bank':'462 005', 
              'Capitec Bank':'470 010','FNB':'250 655', 'Investec':'580 105', 'Nedbank':'198 765', 'Standard Bank':'051 001'}

banks = ['ABSA Bank', 'Bank of Athens','Bidvest Bank', 'Capitec Bank','FNB', 'Investec', 'Nedbank', 'Standard Bank']

# Variables
clients = []
code_codes = []
code_descriptions = []
selected_file = ''
inv_data = {}
payment_received = float(0)
inv_date = ''
inv_pro_codes = []
reg_details = {}
practitioner = ''
###

# Clients database - clients_db
try:
    load_file = open(f'{dll_dir}cdb.dll','rb')
    clients_db = pickle.load(load_file)

except:
    clients_db = {}
###
            
# Services - services_db
s_load_file = open(f'{dll_dir}sdb.dll','rb')
services_db = pickle.load(s_load_file)
###

# Procedure codes - pro_codes
p_load_file = open(f'{dll_dir}procdb.dll','rb')
pro_codes = pickle.load(p_load_file)
###

# Load Invoice History
try:
    ih_load_file = open(f'{dll_dir}invhisdb.dll','rb')
    invoice_history = pickle.load(ih_load_file)
    
except :
   invoice_history = {
       
       'client': [], 
       'inv num': [],
       'date': []

      }
###

#  Codes - code_ ...codes; ...descriptions
c_load_file = open(f'{dll_dir}codecdb.dll','rb')
code_codes = pickle.load(c_load_file)

d_load_file = open(f'{dll_dir}codeddb.dll','rb')
code_descriptions = pickle.load(d_load_file)
###

# Practice contact details - practice_db
try:
    load_file = open(f'{dll_dir}pdb.dll','rb')
    practice_db = pickle.load(load_file)

except:
    practice_db = []
###

# Banking details - banking_db
try:
    load_file = open(f'{dll_dir}bdb.dll','rb')
    banking_db = pickle.load(load_file)

except:
    banking_db = []
###

# PDF coordinates
col = 45
row = 508
###

# Theme setup
theme = 'LightGrey1' # Theme

# Icon
pps_icon = media_dir + '0_icon.ico'

# Font, and font size
main_font = 'Calibri'
hf_size = 25 # Heading
tf_size = 20 # text
btf_size = 20 # button
ebf_size = 15 # Exit and Back buttons
p_std = (10,10) # Std padding
p_ext = (15,15) # Exit Button padding

# Element size
i_size = 20 # Inputbox size
b_size = 20 # Button size
eb_size = 15 # Exit button size

# Invoice elements
inv_t = 10 # Text size
p_inv = 1 # padding
inv_s = 9 # Input element size
p_inv_cb = [(3,3),(6,6)] # Combo box padding
pc_size = 11 # Procedure codes Combo box size
cs_size = 22 # Client select Combo box size
###

class GenerateFromTemplate:
    def __init__(self,template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page= self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(self.packet,pagesize=(self.template_page.mediabox.width,self.template_page.mediabox.height))

    def setFont(self, font, size):
        self.c.setFont(font, size, 0)
        
    def addText(self,text,point):
        self.c.drawString(point[0],point[1],text)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        op = Transformation().rotate(0).translate(tx=0, ty=0)
        result.add_transformation(op)
        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)
    
    def generate(self,dest):
        outputStream = open(dest,"wb")
        self.output.write(outputStream)
        outputStream.close()

def welcome_menu():
    
    try:
        v_load = open(f'{dll_dir}v.dll', 'rb')
        v = pickle.load(v_load)

    except:
        v = 0
    
    if v == 0:
        
        # Capture date
        std()

        v =+ 1
        v_save = open(f'{dll_dir}v.dll', 'wb')
        pickle.dump(v, v_save)
        v_save.close()
             
        sg.theme(theme)

        layout = [
            
            [sg.Push(), sg.T('Welcome to Private Practice StartUp Invoicing System.', font=(main_font, hf_size)), sg.Push()],
            [sg.Push(), sg.T('To start, we will capture all of the essential information,', font=(main_font, hf_size)), sg.Push()],
            [sg.Push(), sg.T('    so please get the following information ready before proceeding:    ', font=(main_font, hf_size)), sg.Push()],
            [sg.T('', font=(main_font, hf_size))],
            [sg.T('     1. Practice Name', font=(main_font, hf_size))],
            [sg.T('     2. Practitioner Name and Surname', font=(main_font, hf_size))],
            [sg.T('     3. Highest Qualification and Tertiary Institution', font=(main_font, hf_size))],
            [sg.T('     4. BHF Practice Number', font=(main_font, hf_size))],
            [sg.T('     5. HPCSA registration number', font=(main_font, hf_size))],
            [sg.T('', font=(main_font, hf_size))],
            [sg.Push(), sg.T('Once you have all of this information ready, click "Proceed".', font=(main_font, hf_size)), sg.Push()],
            [sg.Push(), sg.B('Proceed', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std),sg.Push()]
        
        ]

        window = sg.Window(f'Welcome to PPStartUp Invoicing System', layout, icon=pps_icon)
        
        # Event Loop to process "events"
        while True:             
            event, values = window.read()

            # Exit
            if event == sg.WIN_CLOSED:
                               
                reset_v = 0
                new_v = open(f'{dll_dir}v.dll','wb')
                pickle.dump(reset_v, new_v)
                new_v.close()
                
                window.close()
                break
            
            # Proceed
            if event in 'Proceed':
                
                window.close()
                reg_deets()
        
    else:
        
        v += 1
        v_save = open(f'{dll_dir}v.dll', 'wb')
        pickle.dump(v, v_save)
        v_save.close()
        
        open_date = open(f'{dat_dir}std.dat','rb')
        sub_date = pickle.load(open_date)
                
        # Check date
        check_date = date.today()
        
        if check_date <= sub_date:
            
            main_menu()
        
        else:
            
            sg.popup_ok('Subscription has ended', 'Your subscription has expired. To continue using PPStartUp Invoicing system, please renew your subscription.\nFor more information visit www.ppstartup.co.za or email info@ppstartup.co.za.\n Thank you.',)
            
 
def reg_deets():
    
    reg_col1 = [
    
        [sg.T('1. Practice Name', font=(main_font, hf_size))],
        [sg.T('2. Practitioner Name and Surname', font=(main_font, hf_size))],
        [sg.T('3. Highest Qualification and Tertiary Institution', font=(main_font, hf_size))],
        [sg.T('4. BHF Practice Number', font=(main_font, hf_size))],
        [sg.T('5. HPCSA registration number', font=(main_font, hf_size))]
        
    ]

    reg_col2 = [
        
        [sg.I(k='PP', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k='PSY', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k='QUALI', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k='BHF', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k='HPCSA', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))]
        
    ]

    layout = [
        
        [sg.Column(reg_col1, element_justification='l' ), sg.Column(reg_col2, element_justification='l')],
        [sg.Push(), sg.B('Save Details', font=(main_font,tf_size), border_width='5px', s=b_size, p=p_std), sg.Push()],
        
        ]
        
    window = sg.Window(f'Registration Details:', layout, icon=pps_icon)

    # Event Loop to process "events"
    while True:    
                 
        event, values = window.read()
          
        # Save
        if event in 'Save Details':
            
            practice = str(values['PP'])
            practice = practice.split(' ',-1)
            
            practitioner = values['PSY'].split()
            practitioner = practitioner[0]
            
            gen = GenerateFromTemplate('contact_print_temp.pdf')
            
            gen.setFont('Courier-Bold',25)
            t_row = 730
            
            for i in range(0,len(practice)):
                
                gen.addText(practice[i],(col-3, t_row)) # Practice Name
                t_row += 20
            
            temp_row = 690
            
            gen.setFont('Courier-Bold',10)
            gen.addText(str(values['PSY']),(col-5, temp_row)) # Practitioner name
            gen.addText(str(values['QUALI']),(col-5, (temp_row - 14))) # Highest quali and Uni
            gen.addText(str(values['BHF']),(420, temp_row-1)) # BHF
            gen.addText(str(values['HPCSA']),(420, (temp_row - 13))) # HPCSA
            
            gen.merge()
            gen.generate('contact_print_temp.pdf')
            
            reg_details = [
                
                str(values['PP']),      # Practice name
                str(values['PSY']),     # Practitioner name
                str(values['QUALI']),   # Highest quali and Uni
                str(values['BHF']),     # BHF
                str(values['HPCSA'])    # HPCSA
                
            ]
            
            reg_save = open(f'{dll_dir}registry.dll','wb')
            pickle.dump(reg_details, reg_save)
            reg_save.close()
            
            window.close()
    
        practice_details()
              
def main_menu():
    
    p_load = open(f'{dll_dir}registry.dll','rb')
    loaded_p = pickle.load(p_load)
    practitioner = str(loaded_p[1])
    practitioner_name = list(practitioner.split(' ',-1))
    psychologist = practitioner_name[0]

    sg.theme(theme)   # Add a little color to your windows
        # All the stuff inside your window. This is the PSG magic code compactor...

    layout = [  
                
                [sg.T(f'Welcome {psychologist}, what would you like to do today?', font=(main_font, hf_size), 
                        s=(25,2), justification='centre'),
                    sg.Image('C:\\Users\\JD Gresse\\Pictures\\PPStartUp\\tiny logo.png')],
                [sg.B('Create an Invoice', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
                [sg.B('Add or Update a Client', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
                [sg.B('Add Code', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
                [sg.B('Update Practice Details', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
                [sg.B('Update Banking Details', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
                [sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]
    
    ]

    # Create the Window
    window = sg.Window(f'Welcome to PPStartUp Invoicing System {practitioner}', layout, element_justification='c',
                        icon=pps_icon)

    # Event Loop to process "events"
    while True:    
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            break
    
        # Open Invoice menu
        if event in 'Create an Invoice':
            window.close()
            invoice_menu()
        
        # Open Client menu
        if event in 'Add or Update a Client':
            window.close()
            client_menu()
        
        # Open  menu
        if event in 'Add Code':
            window.close()
            code_menu()
        
        # Open Practice details menu menu
        if event in 'Update Practice Details':            
            window.close()
            practice_details()
        
        # Open Banking details menu
        if event in 'Update Banking Details':
            window.close()
            banking_details()

    window.close()

def invoice_menu():
    
    sg.theme(theme)   
    
    # Initial folder directory
    parent_dir = os.getcwd()
    inv_dir = parent_dir + '\\Client Invoices\\'
    
    layout = [
        
        [sg.T('Do you want to create an Invoice for a New Client, or update the Invoice for an Existing Client?',
              font=(main_font, hf_size), s=(33,3), justification='centre', p=15)],
        [sg.B('Create a New Invoice', font=(main_font, btf_size), border_width='5px', s=(b_size+5), p=p_std)],
        [sg.FileBrowse('Update a Saved Invoice', file_types=(('Saved Invoice', '*.dat*'),), initial_folder=inv_dir,
                            change_submits=True, k='LOAD_FILE', font=(main_font, btf_size), s=(b_size+5), p=p_std)],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]
        
    ]

    # Create the Window
    window = sg.Window('Invoice menu', layout, icon=pps_icon,\
                       element_justification='c')
    
    # Event Loop to process "events"
    while True:      
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        # Back
        if event in 'Back':
            window.close()
            main_menu()
        
        # Go to Invoice temp
        if event in 'Create a New Invoice':
            window.close()
            new_invoice()
            
        # Load invoice
        if event in 'LOAD_FILE':
            # Open Invoice and Contact temp
            window.close()
            selected_file = str(values['LOAD_FILE'])
            load_invoice(selected_file)
            invoice_menu()
        
    window.close()

def client_menu():

    sg.theme(theme)   
    
    layout = [
        
        [sg.T('Do you want to add a New Client, or update an Existing Client?', font=(main_font, hf_size), 
              s=(33,2), justification='centre', p=15)],
        [sg.B('Add a New Client', font=(main_font, btf_size), border_width='5px', s=b_size, p=p_std)],
        [sg.B('Update an existing Client', font=(main_font, btf_size),border_width='5px', 
              s=b_size, p=p_std)],
        [sg.B('Print Contact List', font=(main_font, btf_size),border_width='5px', 
              s=b_size, p=p_std)],        
        [sg.B('Back', font=(main_font, ebf_size),border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]
   
    ]

    # Create the Window
    window = sg.Window('Client menu', layout, icon=pps_icon,\
                       element_justification='centre')
   
    while True:             
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        # Back
        elif event in 'Back':
            window.close()
            main_menu()
            
        # Add Client
        elif event in 'Add a New Client':
            window.close()
            add_client()
            
        # Update Client
        elif event in 'Update an existing Client':            
            window.close()
            edit_client()
            
        # Print Contact List
        elif event in 'Print Contact List':
            window.close()
            print_contacts()

    window.close()

def code_menu():
    
    c_load_file = open(f'{dll_dir}codecdb.dll','rb')
    code_codes = pickle.load(c_load_file)

    d_load_file = open(f'{dll_dir}codeddb.dll','rb')
    code_descriptions = pickle.load(d_load_file)
        
    sg.theme(theme)   
    
    selected = True
    
    col_1 = [
        
        [sg.T(' Code:', font=(main_font, tf_size), p=p_std)],
        [sg.I(k='SEARCH', do_not_clear=selected, font=(main_font, tf_size), s=i_size, p=p_std)],
        [sg.T(' Code:', font=(main_font, tf_size), p=((10,10),(27,10)))],
        [sg.I(k='NEW_CODE', do_not_clear=selected, font=(main_font, tf_size), s=10, p=p_std)],
        
    ]
    
    col_2 = [
        
        [sg.T('', text_color='white',font=(main_font, tf_size), p=(p_std))],
        [sg.B('Search for Code', font=(main_font, tf_size), border_width='5px', s=13)],
        [sg.T('Description:', font=(main_font, tf_size), p=(p_std))],
        [sg.I(k='NEW_DESCRIPTION', do_not_clear=selected, font=(main_font, tf_size), s=i_size, p=(p_std))],
                        
    ]
    
    layout = [
        
        [sg.T('Please enter the  code you would like to search for, or add:', font=(main_font, hf_size),
              s=(28,2), p=((30,15),(15,15)))],
        [sg.Column(col_1, element_justification='l' ), sg.Column(col_2, element_justification='l')],
        [sg.B('Add New Code', font=(main_font,tf_size), border_width='5px', s=b_size, p=p_std)],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext), \
         sg.Exit(font=(main_font, ebf_size), s=eb_size, p=p_ext)]
    
    ]
    
    window = sg.Window(' Codes menu:', layout, icon=pps_icon,\
                      element_justification='c')
    
    while True:        
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            
            window.close()
            break
        
        # Search
        if event in 'Search for Code':
            
            counter = 0
            
            search_code = values['SEARCH']
            
            for i in range(0,len(code_codes)):
                
                while search_code == code_codes[i]:
                    
                    sg.popup_ok('This  Code is already in the database.', title=' Code found:',
                                font=('Calibri',20), icon=pps_icon)
                    counter = 1
                    break
                    
            if counter == 0:
                    
                not_found = sg.popup_yes_no('This  Code is NOT in the database. \nWould you like to add it now?',\
                title='Add  Code?', font=('Calibri',20), icon=pps_icon)

                if not_found == 'Yes':

                    window['NEW_CODE'].Update(values['SEARCH'])

                elif not_found == 'No':

                    window.close()
                    main_menu()
                        
        # Add codes
        if event in 'Add New Code':
            
            if values['NEW_CODE'] != 0 and str(values['NEW_DESCRIPTION']).isalpha():
                
                code_codes.append(values['NEW_CODE'])        
                code_descriptions.append(values['NEW_DESCRIPTION'])

                selected = False

                # Code added notification
                more_codes =  sg.popup_yes_no(' Code added successfully! \nWould you like to add another code?',\
                    title=' Code Added', font=('Calibri',20), icon=pps_icon)

                if more_codes == 'No':

                    # Save codes and descriptions
                    c_save_file = open(f'{dll_dir}codecdb.dll', 'wb')
                    pickle.dump(code_codes, c_save_file)
                    c_save_file.close()

                    d_save_file = open(f'{dll_dir}codeddb.dll', 'wb')
                    pickle.dump(code_descriptions, d_save_file)
                    d_save_file.close()

                    window.close()
                    main_menu()
                    
            else:
                          
                sg.popup_ok('Please add a valid description - it may only contain letters and grammatical symbols.',
                            title='Invalid Description', font=('Calibri',20), 
                            icon=pps_icon)
                    
        # Back
        elif event in 'Back':
                        
            window.close()
            main_menu()

    window.close()

def practice_details():
    
    from email_validator import validate_email, EmailNotValidError
    
    sg.theme(theme)   
    
    col_1 = [
        
        [sg.T('Office Number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Email address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('', text_color='white',font=(main_font, tf_size), p=(p_std))],
        [sg.T('Suburb:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('City:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Postal Code:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Website:', font=(main_font, tf_size), p=(p_std))]
        
    ]
    
    col_2 = [
        
        [sg.I(k=1, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=2, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=3, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=4, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=5, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=6, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=7, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=8, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))]
        
    ]
    
    layout = [
        
        [sg.T('Please update the Practice Contact Details:', font=(main_font, hf_size), s=(35,2), p=10)],
        [sg.Column(col_1, element_justification='l' ), sg.Column(col_2, element_justification='l')],
        [sg.B('Update', font=(main_font, tf_size), border_width='5px', s=b_size, p=p_std)],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext), 
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]
    
    ]

    window = sg.Window('Practice Details menu:', layout, icon=pps_icon,
                       element_justification='c', finalize=True)
    
    try:
        
        pd_load = open(f'{dll_dir}pdb.dll','rb')
        practice_db = pickle.load(pd_load)
        
        for i in range(1,9):
            
            window[i].Update(practice_db[i-1])
        
    except:
        
        practice_db = []
                 
    # Event Loop 
    while True:
        
        event, values = window.read()
        
        v_load = open(f'{dll_dir}v.dll', 'rb')
        v = pickle.load(v_load)
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            
            # Save practice_db
            save_file = open(f'{dll_dir}pdb.dll','wb')
            pickle.dump(practice_db,save_file)
            save_file.close()
            
            window.close()
            break
        
        # Back
        if event in 'Back':
            
            # Save practice_db
            save_file = open(f'{dll_dir}pdb.dll','wb')
            pickle.dump(practice_db,save_file)
            save_file.close()
            
            window.close()
            main_menu()
            
        # Update
        if event in 'Update':  
            
            practice_details = []
            counter = 8
            
            practice_details = [i*' ' for i in range(0,8)]
                        
            while counter != 0:
                
                # Check Phone number
                if re.match(r'(\d{10})', values[1]) == None and re.match(r'\W\d{3}\W \d{3} \d{4}', values[1]) == None and re.match(r'\d{3} \d{3} \d{4}', values[1]) == None:
                    
                    sg.popup_ok('Please enter a valid Contact Number: \nAccepted formats: \n 000 000 0000, \n (000) 000 0000, \n 0000000000',
                                title='InvalidPhone Number', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    practice_details[0] = values[1]
                    counter -= 1
                    
                # Check email   
                try:

                    email = validate_email(values[2])
                    
                    practice_details[1] = values[2]
                    counter -= 1
                    
                except EmailNotValidError as e:

                    sg.popup_ok(str(e), title='Invalid Email', font=('Calibri',20),
                                icon=pps_icon)
                    break
                        
                # Address 1   
                if values[3] == '':
                    
                    sg.popup_ok('Please enter a valid Address:',
                                title='Invalid Address', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    practice_details[2] = (values[3])
                    practice_details[3] = (values[4])
                    practice_details[4] = (values[5])
                    practice_details[5] = (values[6])
                    counter = counter -4

                # Postal Code   
                if values[7] == '' or re.match(r'\d{4}', values[7]) == None:
                    
                    sg.popup_ok('Please enter a valid Postal Code:',
                                title='Invalid Postal Code', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    practice_details[6] = (values[7])
                    practice_details[7] = values[8]
                    counter = counter - 2
                
                # Updating pracice_db
                practice_db = practice_details
                
                # Saving practice_db
                save_file = open(f'{dll_dir}pdb.dll','wb')
                pickle.dump(practice_db,save_file)
                save_file.close()
                
                window.close()
                main_menu()             

def banking_details():
    
    selected = True
    
    sg.theme(theme)  
    
    code = 'Universal Branch Code'
    banks = []

    for bank in bank_codes.keys():
        banks.append(bank)                

    col_1 = [
        
        [sg.T('Account Name:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Bank:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Branch Code', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Account Number:', font=(main_font, tf_size), p=(p_std))],
        
    ]
    
    col_2 = [
        
        [sg.I(k=1, do_not_clear=selected, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.Combo(values=banks, enable_events=True, k='COMBO', font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.T('Universal branch code:', k='U_CODE', font=(main_font, tf_size), p=(p_std))],
        [sg.I(k=4, do_not_clear=selected, font=(main_font, tf_size), s=i_size, p=(p_std))],
                
    ]
    
    layout = [
        
        [sg.T('Please update any Banking Details that have changed:', font=(main_font, hf_size), s=35, p=10)],
        [sg.Column(col_1, element_justification='l' ), sg.Column(col_2, element_justification='l')],
        [sg.B('Update', font=(main_font, tf_size), border_width='5px', s=b_size, p=p_std)],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), s=eb_size, p=p_ext)]
    
    ]
 
    # Create the Window
    window = sg.Window('Banking Details Menu:', layout, icon=pps_icon, 
                       element_justification='c', finalize=True)
    
    # Updating Universal Branch code
    if len(banking_db) != 0:
            
            window[1].Update(banking_db[0])
            window['COMBO'].Update(banking_db[1])
            window['U_CODE'].Update(banking_db[2])
            window[4].Update(banking_db[3])
            
            u_code = banking_db[2]
    
    # Event Loop to process "events"
    while True:
        
        event, values = window.read()
        
        v_load = open(f'{dll_dir}v.dll','rb')
        v = pickle.load(v_load)
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            
            # Clear inputs
            selected = False
            
            # Save banking_db
            save_file = open(f'{dll_dir}bdb.dll','wb')
            pickle.dump(banking_db,save_file)
            save_file.close()
            
            window.close()
        
            break

        # Update universal bank codes based on bank selection
        elif event in 'COMBO':
            window['U_CODE'].Update(bank_codes[values['COMBO']])
            u_code = bank_codes[values['COMBO']]
        
        # Update
        elif event in 'Update':
            
            # First time
            if len(banking_db) == 0:
                
                if values[1] == '':
                    
                    sg.popup_ok('Please enter a valid Account Name:',
                        title='Invalid Account Name', font=('Calibri',20),
                        icon=pps_icon)
                
                else:
                        
                    banking_db.append(values[1])
                    banking_db.append(values['COMBO'])
                    banking_db.append(bank_codes[values['COMBO']])
                    
                    if re.match(r'^(\d{7,11})$', values[4]) == None or values[4] == '':
                        
                        sg.popup_ok('Please enter a valid Account Number:',
                        title='InvalidAccount Number', font=('Calibri',20),
                        icon=pps_icon)
                    
                    else:
                        
                        banking_db.append(values[4])  

            # Not first time
            else:
                
                if values[1] == '':
                    
                    sg.popup_ok('Please enter a valid Account Name:',
                        title='Invalid Account Name', font=('Calibri',20),
                        icon=pps_icon)
                
                else:
                    
                    banking_db[0] = values[1]
                    banking_db[1] = values['COMBO']
                    banking_db[2] = u_code
                    
                    if re.match(r'^(\d{7,11})$', values[4]) == None or values[4] == '':
                        
                        sg.popup_ok('Please enter a valid Account Number:',
                        title='Invalid Account Number', font=('Calibri',20),
                        icon=pps_icon)
                    
                    else:
                        
                        banking_db[3] = values[4]

            # Clear inputs
            selected = False

            # Save banking_db
            save_file = open(f'{dll_dir}bdb.dll','wb')
            pickle.dump(banking_db,save_file)
            save_file.close()
            
            if v == 1:
            
                window.close()
                add_client()

            else:
            
                window.close()
                main_menu()
            
        # Back to Main Menu
        if event in 'Back':
            
            # Save banking_db
            save_file = open(f'{dll_dir}bdb.dll','wb')
            pickle.dump(banking_db,save_file)
            save_file.close()
            
            window.close()
            main_menu()
    
    window.close()

## Add Client Menu
def add_client():
    
    from email_validator import validate_email, EmailNotValidError
    
    # List to capture Client details
    new_client_db = {}

    sg.theme(theme) 
    
    # Client details text boxes
    col_1 = [

        [sg.T('Client Name:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Identity number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Mobile number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Email address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Suburb:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('City/ Town:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Postal Code:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Emergeny Contact:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Name:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Contact number:', font=(main_font, tf_size), p=(p_std))]

    ]

    # Client details input boxes
    col_2 = [

        [sg.I(k=1, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=2, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=3, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=4, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=5, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=6, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=7, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=8, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=9, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.I(k=10, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=11, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],

    ]

    # Medical Aid text boxes
    col_3 = [

        [sg.T('Medical Aid:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Medical Aid number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Is the Client also the Principal Member?', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Principal Member:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Identity number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Suburb:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   City/ Town:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Postal code:', text_color='white',font=(main_font, tf_size), p=(p_std))],

    ]

    # Medical Aid input boxes
    col_4 = [

        [sg.I(k=12, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=13, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.Combo(values=('Yes','No'), enable_events=True, k='PRINCE', font=(main_font, tf_size), s=5, p=(p_std))],
        [sg.I(k=14, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=15, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=16, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=17, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=18, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=19, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=20, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))]

    ]

    layout = [

        [sg.T('Please enter New Client details below:', font=(main_font, hf_size), s=35, p=10)],
        [sg.Column(col_1, element_justification='l' ), sg.Column(col_2, element_justification='l'),
         sg.Column(col_3, element_justification='l' ), sg.Column(col_4, element_justification='l')],
        [sg.B('Add New Client', font=(main_font, tf_size), border_width='5px', s=13, p=(p_std))],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]

    ]

    # Create the Window
    window = sg.Window('Client menu', layout, icon=pps_icon, 
                       element_justification='c')
    
    # Event Loop to process "events"
    while True:    
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            
            # Saving client_db
            save_file = open(f'{dll_dir}cdb.dll','wb')
            pickle.dump(clients_db,save_file)
            save_file.close()
            
            window.close()
            break
                
        # Principal Member = New Client
        if event in 'PRINCE':
            
            if values['PRINCE'] == 'Yes':
                
                window[14].Update(values[1])
                window[15].Update(values[2])
                window[16].Update(values[5])
                window[17].Update(values[6])
                window[18].Update(values[7])
                window[19].Update(values[8])
                window[20].Update(values[9])
                                
        # Back
        if event in 'Back':
            
            # Saving client_db
            save_file = open(f'{dll_dir}cdb.dll','wb')
            pickle.dump(clients_db,save_file)
            save_file.close()
            
            window.close()
            client_menu()
            
               # Add New Client
        if event in 'Add New Client':
            
            clients = [i*1 for i in range(0,20)]
            counter = 20
            
            while counter != 0:
                
                # Name 
                if values[1] == '' or re.search(r'(\d)', values[1]) != None:
                    
                    sg.popup_ok('Please enter a valid Client Name (letters only please):', 
                                title='Invalid Client Name', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[0] = (values[1]) 
                    counter -= 1
                    
                # ID Num
                if re.match(r'(\d{13})', values[2]) == None and re.match(r'\d{6} \d{4} \d{3}', values[2]) == None:
                    
                    sg.popup_ok('Please enter a valid ID number \n Valid formats: \n\t XXXXXX XXXX XXX, \n\t XXXXXXXXXXXXX:',
                                title='Invalid ID Number', font=('Calibri',20),
                                icon=pps_icon) 
                    break
                
                else:
                    
                    clients[1] = (values[2])
                    counter -= 1
                                
                # Contact Number
                if re.match(r'(\d{10})', values[3]) == None and re.match(r'\W\d{3}\W \d{3} \d{4}', values[3]) == None and re.match(r'\d{3} \d{3} \d{4}', values[3]) == None:
                    
                    sg.popup_ok('Please enter a valid Contact Number: \nAccepted formats: \n\t 000 000 0000, \n\t (000) 000 0000, \n\t0000000000',
                                title='Invalid Contact Number', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[2] = (values[3])
                    counter -= 1
                
                # Email:
                try:

                    validate_email(values[4])
                    clients[3] = (values[4])
                    counter -= 1
                    
                except EmailNotValidError as e:

                    sg.popup_ok(str(e),title='Invalid Email', font=('Calibri',20),
                                icon=pps_icon)
                    break
                    
                # Address 1   
                if values[5] == '':
                    
                    sg.popup_ok('Please enter a valid Address:',
                                title='Invalid Address', font=('Calibri',20),
                                icon=pps_icon)
                    break
                    
                else:
                    
                    clients[4] = (values[5])
                    clients[5] = (values[6])
                    clients[6] = (values[7])
                    clients[7] = (values[8])
                    counter = counter - 4
                    
                
                # Postal Code   
                if values[9] == '' or re.match(r'\d{4}', values[9]) == None:
                    
                    sg.popup_ok('Please enter a valid Postal Code:',
                                title='Invalid Postal Code', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[8] = (values[9])
                    counter -= 1
                
                # Emergency Contact
                if values[10] == '' or re.search(r'(\d)', values[10]) != None:
                    
                    sg.popup_ok('Please enter a valid Emergency Contact Name (letters only please):',
                                title='Invalid Emergency Contact Name', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[9] = (values[10])
                    counter -= 1
                            
                # Emergency Contact Number
                if re.match(r'(\d{10})', values[11]) == None and re.match(r'\W\d{3}\W \d{3} \d{4}', values[11]) == None and re.match(r'\d{3} \d{3} \d{4}', values[11]) == None:
                    
                    sg.popup_ok('Please enter a valid Contact Number: \nAccepted formats: \n\t 000 000 0000, \n\t (000) 000 0000, \n\t 0000000000',
                                title='Invalid Phone Number', font=('Calibri',20),
                                icon=pps_icon)   
                    break
                
                else:
                    
                    clients[10] = (values[11])
                    counter -= 1
        
                for i in range(12,21):
                    clients[i-1] = values[i]
                    counter -= 1
                        
                # create acc name
                c_name = clients[0].split(' ',-1)
                acc_name = c_name[0][0] + c_name[1][0]+str(len(clients_db))
                clients.append(acc_name)
                
                # Update clients_db
                new_client_db[clients[0]] = clients[1:]
                clients_db.update(new_client_db)
                
                # Saving client_db
                save_file = open(f'{dll_dir}cdb.dll','wb')
                pickle.dump(clients_db,save_file)
                save_file.close()
                
                # Client added notification
                more_clients =  sg.popup_yes_no('Client added successfully! \nWould you like to add another Client?',\
                title='Client Added ', font=('Calibri',20), icon=pps_icon)
        
                if more_clients == 'No':
                    window.close()
                    main_menu()
            
    window.close() 

## Edit Client Menu
def edit_client():
    
    from email_validator import validate_email, EmailNotValidError
    
    # List to capture Client details
    new_client_db = {}
    client_list = []

    for key in clients_db.keys():
        client_list.append(key)

    sg.theme(theme)   

    # Client details text boxes
    col_1 = [

        [sg.T('Client Name:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Identity number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Mobile number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Email address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Suburb:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('City/ Town:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Postal Code:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Emergeny Contact:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Name:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Contact number:', font=(main_font, tf_size), p=(p_std))]

    ]

    # Client details input boxes
    col_2 = [

        [sg.Combo(values=client_list, enable_events=True, k='CLIENTS', font=(main_font, tf_size),\
                  s=19, p=(p_std))],
        [sg.I(k=2, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=3, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=4, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=5, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=6, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=7, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=8, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=9, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.I(k=10, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=11, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],

    ]

    # Medical Aid text boxes
    col_3 = [

        [sg.T('Medical Aid:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Medical Aid number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('Principal Memeber Details', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Principal Member:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Identity number:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Address:', font=(main_font, tf_size), p=(p_std))],
        [sg.T('', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Suburb:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   City/ Town:', font=(main_font, tf_size), p=(p_std))],
        [sg.T(' ->   Postal code:', text_color='white',font=(main_font, tf_size), p=(p_std))],

    ]

    # Medical Aid input boxes
    col_4 = [

        [sg.I(k=12, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=13, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.Combo(values=('Yes','No'), enable_events=True, k='PRINCE', font=(main_font, tf_size), s=5, p=(p_std))],
        [sg.I(k=14, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=15, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=16, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=17, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=18, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=19, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=20, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))]

    ]

    layout = [

        [sg.T('Please select and update Client details:', font=(main_font, hf_size), s=35, p=10)],
        [sg.Column(col_1, element_justification='l' ), sg.Column(col_2, element_justification='l'),\
         sg.Column(col_3, element_justification='l' ), sg.Column(col_4, element_justification='l')],
        [sg.B('Update Client', font=(main_font, tf_size), border_width='5px', s=b_size, p=(p_std))],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]

    ]

    # Create the Window
    window = sg.Window('Client menu', layout, icon=pps_icon,
                      element_justification='c')
    
    # Event Loop to process "events"
    while True:
        
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            
            # Saving client_db
            save_file = open(f'{dll_dir}cdb.dll','wb')
            pickle.dump(clients_db,save_file)
            save_file.close()
            
            break
            
        # Update client details based on selected client
        if event in 'CLIENTS':
            for i in range(2,21):
                window[i].Update(clients_db[values['CLIENTS']][i-2])
            
        # Back
        if event in 'Back':
            
            # Saving client_db
            save_file = open(f'{dll_dir}cdb.dll','wb')
            pickle.dump(clients_db,save_file)
            save_file.close()
            
            window.close()
            client_menu()
            
        # Principal Member = New Client
        if event in 'PRINCE':
            
            if values['PRINCE'] == 'Yes':
                
                window[14].Update(values['CLIENTS'])
                window[15].Update(values[2])
                window[16].Update(values[5])
                window[17].Update(values[6])
                window[18].Update(values[7])
                window[19].Update(values[8])
                window[20].Update(values[9])
            
        # Update Client
        if event in 'Update Client':
            
            clients = [i*1 for i in range(0,20)]
            counter = 20
            
            while counter != 0:
                
                # Name 
                if values['CLIENTS'] == '' or re.search(r'(\d)', values['CLIENTS']) != None:
                    
                    sg.popup_ok('Please enter a valid Client Name (letters only please):', 
                                title='Invalid Client Name', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[0] = (values['CLIENTS']) 
                    counter -= 1
                    
                # ID Num
                if re.match(r'(\d{13})', values[2]) == None and re.match(r'\d{6} \d{4} \d{3}', values[2]) == None:
                    
                    sg.popup_ok('Please enter a valid ID number \n Valid formats: \n\t XXXXXX XXXX XXX, \n\t XXXXXXXXXXXXX:',
                                title='Invalid ID Number', font=('Calibri',20),
                                icon=pps_icon) 
                    break
                
                else:
                    
                    clients[1] = (values[2])
                    counter -= 1
                                
                # Contact Number
                if re.match(r'(\d{10})', values[3]) == None and re.match(r'\W\d{3}\W \d{3} \d{4}', values[3]) == None and re.match(r'\d{3} \d{3} \d{4}', values[3]) == None:
                    
                    sg.popup_ok('Please enter a valid Contact Number: \nAccepted formats: \n\t 000 000 0000, \n\t (000) 000 0000, \n\t0000000000',
                                title='Invalid Contact Number', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[2] = (values[3])
                    counter -= 1
                
                # Email:
                try:

                    validate_email(values[4])
                    clients[3] = (values[4])
                    counter -= 1
                    
                except EmailNotValidError as e:

                    sg.popup_ok(str(e),title='Invalid Email', font=('Calibri',20),
                                icon=pps_icon)
                    break
                    
                # Address 1   
                if values[5] == '':
                    
                    sg.popup_ok('Please enter a valid Address:',
                                title='Invalid Address', font=('Calibri',20),
                                icon=pps_icon)
                    break
                    
                else:
                    
                    clients[4] = (values[5])
                    clients[5] = (values[6])
                    clients[6] = (values[7])
                    clients[7] = (values[8])
                    counter = counter - 4
                    
                
                # Postal Code   
                if values[9] == '' or re.match(r'\d{4}', values[9]) == None:
                    
                    sg.popup_ok('Please enter a valid Postal Code:',
                                title='Invalid Postal Code', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[8] = (values[9])
                    counter -= 1
                
                # Emergency Contact
                if values[10] == '' or re.search(r'(\d)', values[10]) != None:
                    
                    sg.popup_ok('Please enter a valid Emergency Contact Name (letters only please):',
                                title='Invalid Emergency Contact Name', font=('Calibri',20),
                                icon=pps_icon)
                    break
                
                else:
                    
                    clients[9] = (values[10])
                    counter -= 1
                            
                # Emergency Contact Number
                if re.match(r'(\d{10})', values[11]) == None and re.match(r'\W\d{3}\W \d{3} \d{4}', values[11]) == None and re.match(r'\d{3} \d{3} \d{4}', values[11]) == None:
                    
                    sg.popup_ok('Please enter a valid Contact Number: \nAccepted formats: \n\t(000) 000 0000, \n\t000 000 0000, \n\t 0000000000',
                                title='Invalid Phone Number', font=('Calibri',20),
                                icon=pps_icon)   
                    break
                
                else:
                    
                    clients[10] = (values[11])
                    counter -= 1
        
                for i in range(12,21):
                    clients[i-1] = values[i]
                    counter -= 1
                        
                # create acc name
                c_name = clients[0].split(' ',-1)
                acc_name = c_name[0][0] + c_name[1][0]+str(len(clients_db))
                clients.append(acc_name)
                
                # Update clients_db
                new_client_db[clients[0]] = clients[1:]
                clients_db.update(new_client_db)
                
                # Saving client_db
                save_file = open(f'{dll_dir}cdb.dll','wb')
                pickle.dump(clients_db,save_file)
                save_file.close()
                
                # Client added notification
                more_clients =  sg.popup_yes_no('Client updated successfully! \nWould you like to update another Client?',\
                title='Client Added ', font=('Calibri',20), icon=pps_icon)
        
                if more_clients == 'No':
                    window.close()
                    main_menu()
            
    window.close()

# Print Client menu
def print_contacts():
        
    # Create print Client list
    load_file = open(f'{dll_dir}cdb.dll','rb')
    clients_db = pickle.load(load_file)

    name_list = []
    number_list = []
    email_list = []
    print_list = {}
    
    selected_name_list = []
    selected_number_list = []
    selected_email_list = []

    # Create Print List
    for k in clients_db.keys():

        name_list.append(k)

    name_list = list(name_list)

    for n in name_list:

        number_list.append(clients_db[n][1])
        email_list.append(clients_db[n][2]) 

    print_list['Client'] = name_list
    print_list['Contact Number'] = number_list
    print_list['Email'] = email_list
    
    # Function to create the Frame
    def cb_frame(sequence, key):
        select_clients = [[sg.Checkbox(text=item, font=(main_font, tf_size), p=(p_std),
                                       enable_events=False, auto_size_text=True)] for item in sequence[key]]
        column = [[sg.Column(layout=select_clients, element_justification='l')]]
        return sg.Frame(title=key, layout=column)

    sg.theme(theme)

    layout = [ 

        [[cb_frame(print_list, key) for key in ['Client']]],
        [sg.B('Print Selected', font=(main_font, tf_size), enable_events=True, border_width='5px', s=b_size, p=(p_std)), 
         sg.B('Print All', font=(main_font, tf_size), enable_events=True, border_width='5px', s=b_size, p=(p_std))],
        [sg.B('Back', font=(main_font, ebf_size), border_width='4px', s=eb_size, p=p_ext),
         sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)]

    ]

    window = sg.Window('Please select Contacts to print:', layout, icon=pps_icon, element_justification='c')

    while True:

        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            break
            
        if event in 'Back':
            
            window.close()
            client_menu()
        
        # Print Selected
        if event in 'Print Selected':
            
            select_check = 0
            
            while select_check == 0:
            
                for x in range(0, len(name_list)):
                    
                    if values[x] == True:
                        
                        select_check += 1
                        break
                    
                if select_check == 0:
                    
                    sg.popup_ok('Please select at least 1 contact to print.', 
                                        title='Invalid Selection', font=('Calibri',20),
                                        icon=pps_icon)
                    break
                
            else:    
                
                for x in range(0, len(name_list)):
                
                    if values[x] == True:   
                                
                        selected_name_list.append(name_list[x])
                        selected_number_list.append(number_list[x])
                        selected_email_list.append(email_list[x])
                        
                        gen = GenerateFromTemplate('contact_print_temp.pdf')
            
                        entries = len(selected_name_list)

                        col_1 = 40
                        row_1 = 630
                        for i in range(0, entries):
                            gen.addText(selected_name_list[i],(col_1, row_1))
                            row_1 -= 15

                        col_2 = col_1 + 220
                        row_2 = 630
                        for i in range(0,entries):
                            gen.addText(selected_number_list[i],(col_2, row_2))
                            row_2 -= 15

                        col_3 = col_2 + 130
                        row_3 = 630
                        for i in range(0,entries):
                            gen.addText(selected_email_list[i],(col_3, row_3))
                            row_3 -= 15
                        
                        from datetime import date
                        file_name = date.today()

                        gen.merge()
                        gen.generate(f'{file_name}.pdf')

                print_file = f'{file_name}.pdf'

                def command_print(event = None):
                    command = "{} {}".format('PDFtoPrinter.exe', print_file)
                    subprocess.call(command,shell=True)

                command_print()
                
                window.close()
                main_menu()    
                
        # Print All
        if event in 'Print All':
            
            gen = GenerateFromTemplate('contact_print_temp.pdf')
            
            entries = len(name_list)

            col_1 = 40
            row_1 = 630
            for i in range(0, entries):
                gen.addText(name_list[i],(col_1, row_1))
                row_1 -= 16

            col_2 = col_1 + 220
            row_2 = 630
            for i in range(0,entries):
                gen.addText(number_list[i],(col_2, row_2))
                row_2 -= 16

            col_3 = col_2 + 130
            row_3 = 630
            for i in range(0,entries):
                gen.addText(email_list[i],(col_3, row_3))
                row_3 -= 16
            
            from datetime import date
            file_name = date.today()

            gen.merge()
            gen.generate(f'{file_name}.pdf')

            print_file = f'{file_name}.pdf'

            def command_print(event = None):
                command = "{} {}".format('PDFtoPrinter.exe', print_file)
                subprocess.call(command,shell=True)

            command_print()
        
            window.close()
            main_menu()    

# Create new Invocie
def new_invoice():
    
    # discount
    discount = [''*i for i in range(0,8)]
    
    # Load Invoice number
    try:
        i_load_file = open(f'{dll_dir}inumdb.dll','rb')
        invoice_number = pickle.load(i_load_file)

    except :
        invoice_number = {
        'start': 1000, 
        'current': 1000
        }

    inv_num = invoice_number['current']
    
    ## Required variables
    open_reg = open(f'{dll_dir}registry.dll','rb')
    details = pickle.load(open_reg)
    open_reg.close()
    
    ##### Create Combo lists
    # code
    code_list = []

    for i in range(0,len(code_codes)):
        
        code_list.append(str(code_codes[i]) + ' - ' + code_descriptions[i])
    
    ## Clients
    inv_client_list = []

    for key in clients_db.keys():
        inv_client_list.append(key)
    
    sg.theme(theme)
    
    # Frame 1 = Practice name
    frame_1 = [
        [sg.T('', font=(main_font, 20), p=(p_inv))],
        [sg.T(f'{details[0]}', font=(main_font, 20), p=(p_inv))],
        [sg.T('', font=(main_font, 20), p=(p_inv))]
    ]

    # Frame 2 = Practce Address 
    f2_col_1 = [
        [sg.T('Address:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Suburb:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('City:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Postal Code:', font=(main_font, inv_t), p=(p_inv))]
    ]

    f2_col_2 = [
        [sg.T(f'{practice_db[2]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[3]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[4]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[5]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[6]}', font=(main_font, inv_t), p=(p_inv))]
    ]

    frame_2 = [

        [sg.Column(f2_col_1, element_justification='l' ), sg.Column(f2_col_2, element_justification='l')]

    ]

    # Frame 3 = Practice Contact details
    f3_col_1 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Contact Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Email:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Website:', font=(main_font, inv_t), p=(p_inv))]

    ]

    f3_col_2 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[0]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[7]}', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_3 = [

        [sg.Column(f3_col_1, element_justification='l' ), sg.Column(f3_col_2, element_justification='l')]

    ]

    # Frame 4 = Psychologist details
    frame_4 = [

        [sg.T(f'{details[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{details[2]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    # Frame 5 = BHF and HPCSA reg details
    f5_col_1 = [

        [sg.T(f'BHF Practice Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('HPCSA Registration Number:', font=(main_font, inv_t), p=(p_inv))],

    ]

    f5_col_2 = [

        [sg.T(f'{details[3]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{details[4]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_5 = [

        [sg.Column(f5_col_1, element_justification='l' ), sg.Column(f5_col_2, element_justification='l')]

    ]

    # Frame 6 - 9 = Inv num and Inv Date
    frame_6 = [

        [sg.T('Invoice Number:', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_7 = [

        [sg.T(f'{inv_num}', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_8 = [

        [sg.CalendarButton('Invoice Date', k='I_DATE', format=('%d %b %y'), target=('IN_DATE'), begin_at_sunday_plus=1)]

    ]

    frame_9 = [

        [sg.I(enable_events=True, k='IN_DATE', font=(main_font, inv_t), s=inv_s, p=(p_inv))]  

    ]

    # Frame 10 - 13 = Account Details
    frame_10 = [

        [sg.T('Account Name:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Client ID Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Address:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Suburb:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('City:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Postal Code:', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_11 = [

        [sg.Combo(list(clients_db.keys()), k='CS1', enable_events=True, font=(main_font, inv_t), s=cs_size, p=(p_inv))],
        [sg.T(k='CS0', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS3', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS4', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS5', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS6', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS7', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_12 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Medical Aid:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Medical Aid Number', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Principal Member:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Principal Member ID:', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_13 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T(k='CS10', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS11', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS12', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(k='CS13', font=(main_font, inv_t), p=(p_inv))]

    ]

    ### Frames 14 - 25 = Invoice Details
    # Session Dates
    frame_14 = [
        
        [sg.I(enable_events=True, k='SD1', font=(main_font, inv_t), s=inv_s, p=(p_inv)),
         sg.CalendarButton('Date', k='CAL1', format=('%d %b %y'), target=('SD1'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD2', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL2', format=('%d %b %y'), target=('SD2'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD3', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL3', format=('%d %b %y'), target=('SD3'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD4', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL4', format=('%d %b %y'), target=('SD4'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD5', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL5', format=('%d %b %y'), target=('SD5'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD6', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL6', format=('%d %b %y'), target=('SD6'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD7', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL7', format=('%d %b %y'), target=('SD7'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD8', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL8', format=('%d %b %y'), target=('SD8'), begin_at_sunday_plus=1)]
        
    ]
    
    # Services
    frame_15 = [
        
        [sg.Combo(services_db, k='SER1', enable_events=True, font=(main_font, inv_t), p=((3,3),(10,6)))],
        [sg.Combo(services_db, k='SER2', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER3', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER4', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER5', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER6', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER7', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, k='SER8', enable_events=True, font=(main_font, inv_t), p=((3,3),(5,6)))]

    ]
    
    # Procedure Codes
    frame_16 = [

        [sg.Combo([], k='PC1', font=(main_font, inv_t), s=pc_size, p=((3,3),(10,6)))],
        [sg.Combo([], k='PC2', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC3', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC4', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC5', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC6', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC7', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], k='PC8', font=(main_font, inv_t), s=pc_size, p=((3,3),(5,6)))]

    ]
    
    #  Codes
    frame_17 = [

        [sg.Combo(code_list, k='code1', enable_events=True, font=(main_font, inv_t), p=((3,3),(10,6)))],
        [sg.Combo(code_list, k='code2', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code3', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code4', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code5', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code6', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code7', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(code_list, k='code8', enable_events=True, font=(main_font, inv_t), p=((3,3),(5,6)))]

    ]
    
    # Fees
    frame_18 = [

        [sg.I(font=(main_font, inv_t), k="R1", enable_events=True, p=((3,3),(10,6)))],
        [sg.I(font=(main_font, inv_t), k="R2", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R3", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R4", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R5", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R6", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R7", enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k="R8", enable_events=True, p=((3,3),(5,6)))]
        
    ]
    
    # Discount
    frame_19 = [

        [sg.I(font=(main_font, inv_t), k='D1', enable_events=True, p=((3,3),(10,6)))],
        [sg.I(font=(main_font, inv_t), k='D2', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D3', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D4', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D5', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D6', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D7', enable_events=True, p=(p_inv_cb))],
        [sg.I(font=(main_font, inv_t), k='D8', enable_events=True, p=((3,3),(5,6)))]

    ]
    
    # Total
    frame_20 = [

        [sg.T(k='AO1', font=(main_font, inv_t), p=((3,3),(10,6)))],
        [sg.T(k='AO2', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO3', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO4', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO5', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO6', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO7', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(k='AO8', font=(main_font, inv_t), p=((3,3),(5,6)))]

    ]

    # Frame 30 = T and C
    # T's and C's
    try:
        load_file = open(f'{dll_dir}tnc.dll','rb')
        tnc = pickle.load(load_file)

    except:
        tnc = ['','','','']
        
    frame_30 = [

        [sg.I(tnc[0], k='T1', font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(tnc[1], k='T2',font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(tnc[2], k='T3',font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(tnc[3], k='T4',font=(main_font, inv_t), s=115, p=(p_inv))]

    ]

    # Frame 31 - 33 = Banking Details
    frame_31 = [

        [sg.T('Practice Banking Details:', font=(main_font, inv_t, 'underline'), p=(p_inv))],
        [sg.T('Account Name:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Bank:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Branch Code:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Account Number:', font=(main_font, inv_t), p=(p_inv))],

    ]
    
    frame_32 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[0]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[2]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[3]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_33 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T('Please email proof of payment to:', font=(main_font, inv_t, 'italic'), p=(p_inv))],
        [sg.T(f'{practice_db[1]}', font=(main_font, inv_t, 'bold'), p=(p_inv))],
        [sg.T('Please use "Account Name" as reference.', text_color='red',font=(main_font, inv_t, 'italic'), p=(p_inv))],
        [sg.T('', font=(main_font,inv_t), p=(p_inv))]

    ]

    # Final layout
    final_frame = [

        # Practice Name, Address and Contact details
        [sg.Frame('', layout=frame_1, s=(250,120), element_justification='c'), 
         sg.Frame('', layout=frame_2, s=(250,120)), 
         sg.Frame('', layout=frame_3, s=(300,120))],

        # Psychologist, Highest Qualification, BHF Registration, HPCSA registration
        [sg.Frame('', layout=frame_4, s=(355,50)), 
         sg.Frame('', layout=frame_5, s=(455,50))],

        # Invoice Number and Date
        [sg.Frame('', layout=frame_6, s=(195,30), element_justification='c'), 
         sg.Frame('', layout=frame_7, s=(200,30), element_justification='c'),
         sg.Frame('', layout=frame_8, s=(195,30), element_justification='c'), 
         sg.Frame('', layout=frame_9, s=(200,30), element_justification='c')],

        # Client and Medical aid details
        [sg.Frame('', layout=frame_10, s=(195,155)), 
         sg.Frame('', layout=frame_11, s=(200,155)),
         sg.Frame('', layout=frame_12, s=(195,155)), 
         sg.Frame('', layout=frame_13, s=(200,155))],   

        # Invoie Data
        [sg.Frame('Session Date:', layout=frame_14, s=(120,275)),
         sg.Frame('Service', layout=frame_15, s=(145,275)), 
         sg.Frame('Procedure Code', layout=frame_16, s=(110,275)),
         sg.Frame(' Code', layout=frame_17, s=(85,275),expand_x=True), 
         sg.Frame('Fee', layout=frame_18, s=(100,275)),
         sg.Frame('Discount', layout=frame_19, s=(100,275)), 
         sg.Frame('Amount', layout=frame_20, s=(100,275))],

        # Terms and Conditions
        [sg.Frame('Terms and Conditions:', layout=frame_30, s=(820,110))],

        # Banking details
        [sg.Frame('', layout=frame_31, s=(250,115)), 
         sg.Frame('', layout=frame_32, s=(300,115)), 
         sg.Frame('', layout=frame_33, s=(250,115))],

        # Buttons
        [sg.B(button_text='Save & Print Invoice', font=(main_font,btf_size), border_width='5px', p=10),
         sg.B(button_text='Save Invoice', font=(main_font,btf_size), border_width='5px', p=10),
         sg.B(button_text='Back', font=(main_font,eb_size), border_width='4px', p=10),
         sg.Exit(font=(main_font,eb_size), size=15, p=(10,10))]

    ]
    
    #Creating FinalFrame
    layout = [
        
        [sg.Frame('', layout=final_frame, element_justification='c', )]
        
    ]
    
    # Create GUI
    window = sg.Window(f'{details[0]}'+' - INV # ' + f'{inv_num}', layout,
                       icon=pps_icon, element_justification='c',
                       relative_location=(0,-50))

    while True:
        
        event, values = window.read() 

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event in 'Back':
            window.close()
            invoice_menu()

        # Selecting Session Date
        if event in 'SD1':           
            window['SD1'].Update(values['SD1'])
                        
        if event in 'SD2':
            window['SD2'].Update(values['SD2'])
            
        if event in 'SD3':
            window['SD3'].Update(values['SD3'])
            
        if event in 'SD4':
            window['SD4'].Update(values['SD4'])
            
        if event in 'SD5':
            window['SD5'].Update(values['SD5'])
            
        if event in 'SD6':
            window['SD6'].Update(values['SD6'])
            
        if event in 'SD7':
            window['SD7'].Update(values['SD7'])
            
        if event in 'SD8':
            window['SD8'].Update(values['SD8'])
            
        # Selecting Invoice date
        if event in 'IN_DATE':
            window['IN_DATE'].Update(values['IN_DATE'])
            
        # Selecting  Codes
        if event in 'code1':
            code_result = values['code1'].split(' - ', 1)
            window['code1'].Update(code_result[0])
            
        if event in 'code2':
            code_result = values['code2'].split(' - ', 1)
            window['code2'].Update(code_result[0])
            
        if event in 'code3':
            code_result = values['code3'].split(' - ', 1)
            window['code3'].Update(code_result[0])
            
        if event in 'code4':
            code_result = values['code4'].split(' - ', 1)
            window['code4'].Update(code_result[0])
            
        if event in 'code5':
            code_result = values['code5'].split(' - ', 1)
            window['code5'].Update(code_result[0])
            
        if event in 'code6':
            code_result = values['code6'].split(' - ', 1)
            window['code6'].Update(code_result[0])
            
        if event in 'code7':
            code_result = values['code7'].split(' - ', 1)
            window['code7'].Update(code_result[0])
            
        if event in 'code8':
            code_result = values['code8'].split(' - ', 1)
            window['code8'].Update(code_result[0])
            
        # Selecting Service and setting -> Procedure codes
        if event in 'SER1':

            try:
                pass
                codes_list = pro_codes[values['SER1']]
                window['PC1'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER2':

            try:
                codes_list = pro_codes[values['SER2']]
                window['PC2'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER3':

            try:
                codes_list = pro_codes[values['SER3']]
                window['PC3'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER4':

            try:
                codes_list = pro_codes[values['SER4']]
                window['PC4'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER5':

            try:
                codes_list = pro_codes[values['SER5']]
                window['PC5'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER6':

            try:
                codes_list = pro_codes[values['SER6']]
                window['PC6'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER7':

            try:
                codes_list = pro_codes[values['SER7']]
                window['PC7'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER8':

            try:
                codes_list = pro_codes[values['SER8']]
                window['PC8'].update(values=codes_list)
               
            except:
                pass

        # Update Amount owed -> Fees
        if event in 'R1':
            
            if values['SER1'] == 'Payment Received':

                try:
                    window['PC1'].update(values['PC1'])
                    total = locale.currency((float(values['R1'])), grouping=True)
                    window['AO1'].update(f'({total})')

                except:
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(float(values['R1']), grouping=True))
                
                except:
               
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(0, grouping=True))
        # 2
        if event in 'R2':

            if values['SER2'] == 'Payment Received':

                try:
                    window['PC2'].update(values['PC2'])
                    total = locale.currency((float(values['R2'])), grouping=True)
                    window['AO2'].update(f'({total})')

                except:
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(float(values['R2']), grouping=True))
                
                except:
               
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(0, grouping=True))
                    
        # 3       
        if event in 'R3':

            if values['SER3'] == 'Payment Received':

                try:
                    window['PC3'].update(values['PC3'])
                    total = locale.currency((float(values['R3'])), grouping=True)
                    window['AO3'].update(f'({total})')

                except:
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(float(values['R3']), grouping=True))
                
                except:
               
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(0, grouping=True))
                
        # 4        
        if event in 'R4':

            if values['SER4'] == 'Payment Received':

                try:
                    window['PC4'].update(values['PC4'])
                    total = locale.currency((float(values['R4'])), grouping=True)
                    window['AO4'].update(f'({total})')

                except:
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(float(values['R4']), grouping=True))
                
                except:
               
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(0, grouping=True))
                
        # 5        
        if event in 'R5':

            if values['SER5'] == 'Payment Received':

                try:
                    window['PC5'].update(values['PC5'])
                    total = locale.currency((float(values['R5'])), grouping=True)
                    window['AO5'].update(f'({total})')

                except:
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(float(values['R5']), grouping=True))
                
                except:
               
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(0, grouping=True))
                
        # 6        
        if event in 'R6':

            if values['SER6'] == 'Payment Received':

                try:
                    window['PC6'].update(values['PC6'])
                    total = locale.currency((float(values['R6'])), grouping=True)
                    window['AO6'].update(f'({total})')

                except:
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(float(values['R6']), grouping=True))
                
                except:
               
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(0, grouping=True))
                
        # 7        
        if event in 'R7':

            if values['SER7'] == 'Payment Received':

                try:
                    window['PC7'].update(values['PC7'])
                    total = locale.currency((float(values['R7'])), grouping=True)
                    window['AO7'].update(f'({total})')

                except:
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(float(values['R7']), grouping=True))
                
                except:
               
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(0, grouping=True))
                
        # 8        
        if event in 'R8':

            if values['SER28'] == 'Payment Received':

                try:
                    window['PC8'].update(values['PC8'])
                    total = locale.currency((float(values['R8'])), grouping=True)
                    window['AO8'].update(f'({total})')

                except:
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(float(values['R8']), grouping=True))
                
                except:
               
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(0, grouping=True))
        
        # Update Amount owed --> Discount
        if event in 'D1':

            try:
                discount[0] = float(values['D1'])
                fees_1 = float(values['R1'])
                
                window['PC1'].update(values['PC1'])                
                window['AO1'].update(locale.currency((fees_1 - discount[0]), grouping=True)) 

            except:
                discount[0] = 0
                fees_1 = float(values['R1'])
                
                window['PC1'].update(values['PC1'])
                window['AO1'].update(locale.currency((fees_1 - discount[0]), grouping=True))

        # 2
        if event in 'D2':

            try:
                discount[1] = float(values['D2'])
                fees_2 = float(values['R2'])
                
                window['PC2'].update(values['PC2'])                
                window['AO2'].update(locale.currency((fees_2 - discount[1]), grouping=True)) 

            except:
                discount[1] = 0
                fees_2 = float(values['R2'])
                
                window['PC2'].update(values['PC2'])
                window['AO2'].update(locale.currency((fees_2 - discount[1]), grouping=True))

        # 3
        if event in 'D3':

            try:
                discount[2] = float(values['D3'])
                fees_3 = float(values['R3'])
                
                window['PC3'].update(values['PC3'])
                window['AO3'].update(locale.currency((fees_3 - discount[2]), grouping=True)) 

            except:
                discount[2] = 0
                fees_3 = float(values['R3'])
                
                window['PC3'].update(values['PC3'])
                window['AO3'].update(locale.currency((fees_3 - discount[2]), grouping=True))

        # 4
        if event in 'D4':

            try:
                discount[3] = float(values['D4'])
                fees_4 = float(values['R4'])
                
                window['PC4'].update(values['PC4'])
                window['AO4'].update(locale.currency((fees_4 - discount[3]), grouping=True)) 

            except:
                discount[3] = 0
                fees_4 = float(values['R4'])
                
                window['PC4'].update(values['PC4'])
                window['AO4'].update(locale.currency((fees_4 - discount[3]), grouping=True))

        # 5
        if event in 'D5':

            try:
                discount[4] = float(values['D5'])
                fees_5 = float(values['R5'])
                
                window['PC5'].update(values['PC5'])
                window['AO5'].update(locale.currency((fees_5 - discount[4]), grouping=True)) 

            except:
                discount[4] = 0
                fees_5 = float(values['R5'])
                
                window['PC5'].update(values['PC5'])
                window['AO5'].update(locale.currency((fees_5 - discount[4]), grouping=True))

        # 6
        if event in 'D6':

            try:
                discount[5] = float(values['D6'])
                fees_6 = float(values['R6'])
                
                window['PC6'].update(values['PC6'])
                window['AO6'].update(locale.currency((fees_6 - discount[5]), grouping=True)) 

            except:
                discount[5] = 0
                fees_6 = float(values['R6'])
                
                window['PC6'].update(values['PC6'])
                window['AO6'].update(locale.currency((fees_6 - discount[5]), grouping=True))

        # 7
        if event in 'D7':

            try:
                discount[6] = float(values['D7'])
                fees_7 = float(values['R7'])
                
                window['PC7'].update(values['PC7'])
                window['AO7'].update(locale.currency((fees_7 - discount[6]), grouping=True)) 

            except:
                discount[6] = 0
                fees_7 = float(values['R7'])
                
                window['PC7'].update(values['PC7'])
                window['AO7'].update(locale.currency((fees_7 - discount[6]), grouping=True))

        # 8
        if event in 'D8':

            try:
                discount[7] = float(values['D8'])
                fees_8 = float(values['R8'])
                
                window['PC8'].update(values['PC8'])
                window['AO8'].update(locale.currency((fees_8 - discount[7]), grouping=True)) 

            except:
                discount[7] = 0
                fees_8 = float(values['R8'])
                
                window['PC8'].update(values['PC8'])
                window['AO8'].update(locale.currency((fees_8 - discount[7]), grouping=True))

        # Client Select
        if event in 'CS1':

            cs = values['CS1']

            for i in [0,3,4,5,6,7,10,11,12,13]:
                window[f'CS{i}'].update(clients_db[cs][i])

        # Save Invoice
        if event in 'Save Invoice':
            
            #Check Inv Date
            while values['IN_DATE'] == '':
                
                sg.popup_ok('Please select Invoice Date:', title='Invalid Invoice Date',
                            font=('Calibri',20), icon=pps_icon)
                break

            else:
                
                inv_date = values['IN_DATE']
                
                # Check Session Date
                while values['SD1'] == '':
                    
                    sg.popup_ok('Please select at least 1 Session Date:', title='Please select a Session Date',
                                font=('Calibri',20), icon=pps_icon)
                    break
                    
                else:
                    
                    open_reg = open(f'{dll_dir}registry.dll','rb')
                    registry = pickle.load(open_reg)
                    
                    sub_total = 0
                    disc = 0
                    payment_received = 0
                    total_due = 0
                    
                    file_acc_name = values['CS1']
                    file_date = values['IN_DATE']

                    # Creating / Opening save folder
                    parent_dir = os.getcwd()
                    inv_dir = parent_dir + '\\Client Invoices\\'
                    client_dir = inv_dir + file_acc_name
                    
                    try:
                        # Create Client Invoices Folderd
                        os.mkdir(inv_dir)
                        
                        try:
                            # Create Client Folder
                            os.mkdir(client_dir)
                            
                        except FileExistsError:
                            pass
                            # Client Folder already exists

                    except FileExistsError:              
                        # Client Invoices Folder already exists, try creating Client Folder
                        try:                  
                            # Create Client Folder
                            os.mkdir(client_dir)
                        
                        except FileExistsError:
                            pass
                            # Client Folder already exists     
                            
                    # Capturing Invoice data
                    inv_data = {
                        'dates': [''*i for i in range(0,8)],
                        'services': [''*i for i in range(0,8)],
                        'pro_codes': [''*i for i in range(0,8)],
                        'code': [''*i for i in range(0,8)],
                        'fees': [''*i for i in range(0,8)],
                        'discount': [''*i for i in range(0,8)],
                        'payment_received': [''*i for i in range(0,8)],
                        'total': [''*i for i in range(0,8)]
                        }
                    
                    for i in range(0,8):    
                        
                        if values[f'SD{i+1}'] == '':
                        
                            inv_data['dates'][i] = ''
                            inv_data['services'][i] = ''
                            inv_data['pro_codes'][i] = ''
                            inv_data['code'][i] = ''
                            inv_data['fees'][i] = ''
                            inv_data['discount'][i] = ''
                            inv_data['payment_received'][i] = ''
                            inv_data['total'][i] = ''
                        
                        else:
                            
                            inv_data['dates'][i] = (values[f'SD{i+1}'])
                            inv_data['services'][i] = (values[f'SER{i+1}'])
                            inv_data['pro_codes'][i] = (values[f'PC{i+1}'])
                            inv_data['code'][i] = (values[f'code{i+1}'])
                            
                            if values[f'SER{i+1}'] == 'Payment Received':
                                
                                inv_data['payment_received'][i] = (values[f'R{i+1}'])
                                inv_data['fees'][i] = '' 
                                
                                payment_received = payment_received + float(values[f'R{i+1}'])

                            else: 
                                
                                inv_data['fees'][i] = (values[f'R{i+1}'])
                                inv_data['payment_received'][i] = ''
                                
                            # check for discount to calculate inv_data['total']
                            if discount[i] == '':
                                
                                inv_data['discount'][i] = str(discount[i])
                                inv_data['total'][i] = (values[f'R{i+1}'])
                                
                                sub_total = sub_total + float(inv_data['fees'][i])
                                
                            else: 
                                
                                inv_data['discount'][i] = str(discount[i])
                                disc = disc + float(inv_data['discount'][i])
                                
                                inv_data['total'][i] = (float(inv_data['fees'][i]) - float(inv_data['discount'][i]))
                                
                                sub_total = sub_total + float(inv_data['fees'][i])

                    total_due = sub_total - disc - payment_received                
                    
                    for i in range(0,4):
                        tnc[i] = values[f'T{i+1}']
                        
                    tnc_save = open(f'{dll_dir}tnc.dll','wb')
                    pickle.dump(tnc, tnc_save)
                    tnc_save.close()               
                    
                    class Invoice(QWidget):
                        def __init__(self):
                            super(Invoice, self).__init__()
                            loadUi(f'{ui_dir}invoice_temp.ui', self)
                        
                            # Practice Name
                            self.practice_name.setText(registry[0])
                            
                            # Practice Address
                            self.l1.setText(practice_db[2])
                            self.l2.setText(practice_db[3])
                            self.l3.setText(practice_db[4])
                            self.l4.setText(practice_db[5])
                            self.l5.setText(practice_db[6])
                            
                            # Practice contacts
                            self.l6.setText(practice_db[0])
                            self.l7.setText(practice_db[1])
                            self.l8.setText(practice_db[7])

                            # registration details:
                            self.psyc.setText(registry[1])
                            self.quali.setText(registry[2])
                            self.bhf_num.setText(registry[3])
                            self.hpcsa_num.setText(registry[4])
                            
                            # Inv num and date
                            self.inv_num_3.setText(str(inv_num))
                            self.inv_date_3.setText(inv_date)
                            
                            # Client detailsvalues['CS1']
                            self.l9_6.setText(clients_db[values['CS1']][-1]) # acc name
                            self.l9_6.setText(clients_db[values['CS1']][0]) # id
                            self.l9_6.setText(clients_db[values['CS1']][3]) # ad 1
                            self.l9_6.setText(clients_db[values['CS1']][4]) # ad 2
                            self.l9_6.setText(clients_db[values['CS1']][5]) # sub
                            self.l9_6.setText(clients_db[values['CS1']][6]) # city
                            self.l9_6.setText(clients_db[values['CS1']][7]) # postal
                            self.l9_6.setText(clients_db[values['CS1']][10]) # med aid
                            self.l9_6.setText(clients_db[values['CS1']][11]) # med aid num
                            self.l9_6.setText(clients_db[values['CS1']][12]) # prince
                            self.l9_6.setText(clients_db[values['CS1']][13]) # prince id
                            
                            # Inv data
                            # SD
                            self.sd_1.setText(inv_data['dates'][0])
                            self.sd_2.setText(inv_data['dates'][1])
                            self.sd_3.setText(inv_data['dates'][2])
                            self.sd_4.setText(inv_data['dates'][3])
                            self.sd_5.setText(inv_data['dates'][4])
                            self.sd_6.setText(inv_data['dates'][5])
                            self.sd_7.setText(inv_data['dates'][6])
                            self.sd_8.setText(inv_data['dates'][7])
                            self.sd_9.setText('')
                            self.sd_10.setText('')
                            self.sd_11.setText('')
                            self.sd_12.setText('')
                            
                            # Service
                            self.services_1.setText(inv_data['services'][0])
                            self.services_2.setText(inv_data['services'][1])
                            self.services_3.setText(inv_data['services'][2])
                            self.services_4.setText(inv_data['services'][3])
                            self.services_5.setText(inv_data['services'][4])
                            self.services_6.setText(inv_data['services'][5])
                            self.services_7.setText(inv_data['services'][6])
                            self.services_8.setText(inv_data['services'][7])
                            self.services_9.setText('')
                            self.services_10.setText('')
                            self.services_11.setText('')
                            self.services_12.setText('')
                            
                            # PC
                            self.pc_1.setText(inv_data['pro_codes'][0])
                            self.pc_2.setText(inv_data['pro_codes'][1])
                            self.pc_3.setText(inv_data['pro_codes'][2])
                            self.pc_4.setText(inv_data['pro_codes'][3])
                            self.pc_5.setText(inv_data['pro_codes'][4])
                            self.pc_6.setText(inv_data['pro_codes'][5])
                            self.pc_7.setText(inv_data['pro_codes'][6])
                            self.pc_8.setText(inv_data['pro_codes'][7])
                            self.pc_9.setText('')
                            self.pc_10.setText('')
                            self.pc_11.setText('')
                            self.pc_12.setText('')
                            
                            # code
                            self.code_1.setText(inv_data['code'][0])
                            self.code_2.setText(inv_data['code'][1])
                            self.code_3.setText(inv_data['code'][2])
                            self.code_4.setText(inv_data['code'][3])
                            self.code_5.setText(inv_data['code'][4])
                            self.code_6.setText(inv_data['code'][5])
                            self.code_7.setText(inv_data['code'][6])
                            self.code_8.setText(inv_data['code'][7])
                            self.code_9.setText('')
                            self.code_10.setText('')
                            self.code_11.setText('')
                            self.code_12.setText('')
                            
                            # Fees
                            self.fees_1.setText(inv_data['fees'][0])
                            self.fees_2.setText(inv_data['fees'][1])
                            self.fees_3.setText(inv_data['fees'][2])
                            self.fees_4.setText(inv_data['fees'][3])
                            self.fees_5.setText(inv_data['fees'][4])
                            self.fees_6.setText(inv_data['fees'][5])
                            self.fees_7.setText(inv_data['fees'][6])
                            self.fees_8.setText(inv_data['fees'][7])
                            self.fees_9.setText('')
                            self.fees_10.setText('')
                            self.fees_11.setText('')
                            self.fees_12.setText('')
                            
                            # Disc
                            self.disc_1.setText(inv_data['discount'][0])
                            self.disc_2.setText(inv_data['discount'][1])
                            self.disc_3.setText(inv_data['discount'][2])
                            self.disc_4.setText(inv_data['discount'][3])
                            self.disc_5.setText(inv_data['discount'][4])
                            self.disc_6.setText(inv_data['discount'][5])
                            self.disc_7.setText(inv_data['discount'][6])
                            self.disc_8.setText(inv_data['discount'][7])
                            self.disc_9.setText('')
                            self.disc_10.setText('')
                            self.disc_11.setText('')
                            self.disc_12.setText('')
                            
                            # AO
                            self.ao_1.setText(str(inv_data['total'][0]))
                            self.ao_2.setText(str(inv_data['total'][1]))
                            self.ao_3.setText(str(inv_data['total'][2]))
                            self.ao_4.setText(str(inv_data['total'][3]))
                            self.ao_5.setText(str(inv_data['total'][4]))
                            self.ao_6.setText(str(inv_data['total'][5]))
                            self.ao_7.setText(str(inv_data['total'][6]))
                            self.ao_8.setText(str(inv_data['total'][7]))
                            self.ao_9.setText('')
                            self.ao_10.setText('')
                            self.ao_11.setText('')
                            self.ao_12.setText('')
                            
                            # Terms and conditions
                            self.tnc_1.setText(tnc[0])
                            self.tnc_2.setText(tnc[1])
                            self.tnc_3.setText(tnc[2])
                            self.tnc_4.setText(tnc[3])
                            
                            # Banking deets
                            self.bd_5.setText(banking_db[0])
                            self.bd_6.setText(banking_db[1])
                            self.bd_7.setText(banking_db[2])
                            self.bd_8.setText(banking_db[3])
                            
                            # Totals
                            self.sub_total.setText(str(sub_total))
                            self.discount.setText(str(disc))
                            self.payment_received.setText(str(payment_received))
                            self.amount_owed.setText(str(total_due))
                            
                            # Save
                            printer = QPrinter()                          
                            printer.OutputFormat(1)
                            printer.setOutputFileName(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf')
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end() 
                            
                            close_print = sg.popup_ok(f'Invoice {inv_num} - saved succefully as: \n {clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf',
                                    title='Invoice Saved', icon=pps_icon)
                            
                            if close_print == 'OK':
                                self.close()      
                            
                    if __name__ == '__main__':
                        
                        app = QApplication(sys.argv)
                        print_window = Invoice()
                        
            save_inv_data = open(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}.dat', 'wb')
            pickle.dump(inv_data, save_inv_data)
            save_inv_data.close()
            
            invoice_number['current'] = (inv_num +1)
            
            save_inv_num = open(f'{dll_dir}inumdb.dll','wb')  
            pickle.dump(invoice_number, save_inv_num)
            save_inv_num.close()
            
            invoice_history['client'].append(clients_db[values['CS1']][-1])
            invoice_history['inv num'].append(inv_num)
            invoice_history['date'].append(inv_date)
            
            save_inv_hist = open(f'{dll_dir}invhis.dll','wb')
            pickle.dump(invoice_history,save_inv_hist)
            save_inv_hist.close()
            
            window.close()
            new_invoice()

        # Save and Print Invoice
        if event in 'Save & Print Invoice':
            
            #Check Inv Date
            while values['IN_DATE'] == '':
                
                sg.popup_ok('Please select Invoice Date:', title='Invalid Invoice Date',
                            font=('Calibri',20), icon=pps_icon)
                break

            else:
                
                inv_date = values['IN_DATE']
                
                # Check Session Date
                while values['SD1'] == '':
                    
                    sg.popup_ok('Please select at least 1 Session Date:', title='Please select a Session Date',
                                font=('Calibri',20), icon=pps_icon)
                    break
                    
                else:
                    
                    open_reg = open(f'{dll_dir}registry.dll','rb')
                    registry = pickle.load(open_reg)
                    
                    sub_total = 0
                    disc = 0
                    payment_received = 0
                    total_due = 0
                    
                    file_acc_name = values['CS1']
                    file_date = values['IN_DATE']

                    # Creating / Opening save folder
                    parent_dir = os.getcwd()
                    inv_dir = parent_dir + '\\Client Invoices\\'
                    client_dir = inv_dir + file_acc_name
                    
                    try:
                        # Create Client Invoices Folderd
                        os.mkdir(inv_dir)
                        
                        try:
                            # Create Client Folder
                            os.mkdir(client_dir)
                            
                        except FileExistsError:
                            pass
                            # Client Folder already exists

                    except FileExistsError:              
                        # Client Invoices Folder already exists, try creating Client Folder
                        try:                  
                            # Create Client Folder
                            os.mkdir(client_dir)
                        
                        except FileExistsError:
                            pass
                            # Client Folder already exists     
                            
                    # Capturing Invoice data
                    inv_data = {
                        'dates': [''*i for i in range(0,8)],
                        'services': [''*i for i in range(0,8)],
                        'pro_codes': [''*i for i in range(0,8)],
                        'code': [''*i for i in range(0,8)],
                        'fees': [''*i for i in range(0,8)],
                        'discount': [''*i for i in range(0,8)],
                        'payment_received': [''*i for i in range(0,8)],
                        'total': [''*i for i in range(0,8)]
                        }
                    
                    for i in range(0,8):    
                        
                        if values[f'SD{i+1}'] == '':
                        
                            inv_data['dates'][i] = ''
                            inv_data['services'][i] = ''
                            inv_data['pro_codes'][i] = ''
                            inv_data['code'][i] = ''
                            inv_data['fees'][i] = ''
                            inv_data['discount'][i] = ''
                            inv_data['payment_received'][i] = ''
                            inv_data['total'][i] = ''
                        
                        else:
                            
                            inv_data['dates'][i] = (values[f'SD{i+1}'])
                            inv_data['services'][i] = (values[f'SER{i+1}'])
                            inv_data['pro_codes'][i] = (values[f'PC{i+1}'])
                            inv_data['code'][i] = (values[f'code{i+1}'])
                            
                            if values[f'SER{i+1}'] == 'Payment Received':
                                
                                inv_data['payment_received'][i] = (values[f'R{i+1}'])
                                inv_data['fees'][i] = '' 
                                
                                payment_received = payment_received + float(values[f'R{i+1}'])

                            else: 
                                
                                inv_data['fees'][i] = (values[f'R{i+1}'])
                                inv_data['payment_received'][i] = ''
                                
                            # check for discount to calculate inv_data['total']
                            if values[f'D{i+1}'] == '':
                                
                                inv_data['discount'][i] = str(discount[i])
                                inv_data['total'][i] = (values[f'R{i+1}'])
                                
                                sub_total = sub_total + float(inv_data['fees'][i])
                                
                            else: 
                                
                                inv_data['discount'][i] = str(discount[i])
                                disc = disc + float(inv_data['discount'][i])
                                
                                inv_data['total'][i] = (float(inv_data['fees'][i]) - float(inv_data['discount'][i]))
                                
                                sub_total = sub_total + float(inv_data['fees'][i])

                    total_due = sub_total - disc - payment_received                
                                        
                    for i in range(0,4):
                        tnc[i] = values[f'T{i+1}']
                        
                    tnc_save = open(f'{dll_dir}tnc.dll','wb')
                    pickle.dump(tnc, tnc_save)
                    tnc_save.close()               
                    
                    class Invoice(QWidget):
                        def __init__(self):
                            super(Invoice, self).__init__()
                            loadUi(f'{ui_dir}invoice_temp.ui', self)
                        
                            # Practice Name
                            self.practice_name.setText(registry[0])
                            
                            # Practice Address
                            self.l1.setText(practice_db[2])
                            self.l2.setText(practice_db[3])
                            self.l3.setText(practice_db[4])
                            self.l4.setText(practice_db[5])
                            self.l5.setText(practice_db[6])
                            
                            # Practice contacts
                            self.l6.setText(practice_db[0])
                            self.l7.setText(practice_db[1])
                            self.l8.setText(practice_db[7])

                            # registration details:
                            self.psyc.setText(registry[1])
                            self.quali.setText(registry[2])
                            self.bhf_num.setText(registry[3])
                            self.hpcsa_num.setText(registry[4])
                            
                            # Inv num and date
                            self.inv_num_3.setText(str(inv_num))
                            self.inv_date_3.setText(inv_date)
                            
                            # Client detailsvalues['CS1']
                            self.l9_6.setText(clients_db[values['CS1']][-1]) # acc name
                            self.l9_6.setText(clients_db[values['CS1']][0]) # id
                            self.l9_6.setText(clients_db[values['CS1']][3]) # ad 1
                            self.l9_6.setText(clients_db[values['CS1']][4]) # ad 2
                            self.l9_6.setText(clients_db[values['CS1']][5]) # sub
                            self.l9_6.setText(clients_db[values['CS1']][6]) # city
                            self.l9_6.setText(clients_db[values['CS1']][7]) # postal
                            self.l9_6.setText(clients_db[values['CS1']][10]) # med aid
                            self.l9_6.setText(clients_db[values['CS1']][11]) # med aid num
                            self.l9_6.setText(clients_db[values['CS1']][12]) # prince
                            self.l9_6.setText(clients_db[values['CS1']][13]) # prince id
                            
                            # Inv data
                            # SD
                            self.sd_1.setText(inv_data['dates'][0])
                            self.sd_2.setText(inv_data['dates'][1])
                            self.sd_3.setText(inv_data['dates'][2])
                            self.sd_4.setText(inv_data['dates'][3])
                            self.sd_5.setText(inv_data['dates'][4])
                            self.sd_6.setText(inv_data['dates'][5])
                            self.sd_7.setText(inv_data['dates'][6])
                            self.sd_8.setText(inv_data['dates'][7])
                            self.sd_9.setText('')
                            self.sd_10.setText('')
                            self.sd_11.setText('')
                            self.sd_12.setText('')
                            
                            # Service
                            self.services_1.setText(inv_data['services'][0])
                            self.services_2.setText(inv_data['services'][1])
                            self.services_3.setText(inv_data['services'][2])
                            self.services_4.setText(inv_data['services'][3])
                            self.services_5.setText(inv_data['services'][4])
                            self.services_6.setText(inv_data['services'][5])
                            self.services_7.setText(inv_data['services'][6])
                            self.services_8.setText(inv_data['services'][7])
                            self.services_9.setText('')
                            self.services_10.setText('')
                            self.services_11.setText('')
                            self.services_12.setText('')
                            
                            # PC
                            self.pc_1.setText(inv_data['pro_codes'][0])
                            self.pc_2.setText(inv_data['pro_codes'][1])
                            self.pc_3.setText(inv_data['pro_codes'][2])
                            self.pc_4.setText(inv_data['pro_codes'][3])
                            self.pc_5.setText(inv_data['pro_codes'][4])
                            self.pc_6.setText(inv_data['pro_codes'][5])
                            self.pc_7.setText(inv_data['pro_codes'][6])
                            self.pc_8.setText(inv_data['pro_codes'][7])
                            self.pc_9.setText('')
                            self.pc_10.setText('')
                            self.pc_11.setText('')
                            self.pc_12.setText('')
                            
                            # code
                            self.code_1.setText(inv_data['code'][0])
                            self.code_2.setText(inv_data['code'][1])
                            self.code_3.setText(inv_data['code'][2])
                            self.code_4.setText(inv_data['code'][3])
                            self.code_5.setText(inv_data['code'][4])
                            self.code_6.setText(inv_data['code'][5])
                            self.code_7.setText(inv_data['code'][6])
                            self.code_8.setText(inv_data['code'][7])
                            self.code_9.setText('')
                            self.code_10.setText('')
                            self.code_11.setText('')
                            self.code_12.setText('')
                            
                            # Fees
                            self.fees_1.setText(inv_data['fees'][0])
                            self.fees_2.setText(inv_data['fees'][1])
                            self.fees_3.setText(inv_data['fees'][2])
                            self.fees_4.setText(inv_data['fees'][3])
                            self.fees_5.setText(inv_data['fees'][4])
                            self.fees_6.setText(inv_data['fees'][5])
                            self.fees_7.setText(inv_data['fees'][6])
                            self.fees_8.setText(inv_data['fees'][7])
                            self.fees_9.setText('')
                            self.fees_10.setText('')
                            self.fees_11.setText('')
                            self.fees_12.setText('')
                            
                            # Disc
                            self.disc_1.setText(inv_data['discount'][0])
                            self.disc_2.setText(inv_data['discount'][1])
                            self.disc_3.setText(inv_data['discount'][2])
                            self.disc_4.setText(inv_data['discount'][3])
                            self.disc_5.setText(inv_data['discount'][4])
                            self.disc_6.setText(inv_data['discount'][5])
                            self.disc_7.setText(inv_data['discount'][6])
                            self.disc_8.setText(inv_data['discount'][7])
                            self.disc_9.setText('')
                            self.disc_10.setText('')
                            self.disc_11.setText('')
                            self.disc_12.setText('')
                            
                            # AO
                            self.ao_1.setText(str(inv_data['total'][0]))
                            self.ao_2.setText(str(inv_data['total'][1]))
                            self.ao_3.setText(str(inv_data['total'][2]))
                            self.ao_4.setText(str(inv_data['total'][3]))
                            self.ao_5.setText(str(inv_data['total'][4]))
                            self.ao_6.setText(str(inv_data['total'][5]))
                            self.ao_7.setText(str(inv_data['total'][6]))
                            self.ao_8.setText(str(inv_data['total'][7]))
                            self.ao_9.setText('')
                            self.ao_10.setText('')
                            self.ao_11.setText('')
                            self.ao_12.setText('')
                            
                            # Terms and conditions
                            self.tnc_1.setText(tnc[0])
                            self.tnc_2.setText(tnc[1])
                            self.tnc_3.setText(tnc[2])
                            self.tnc_4.setText(tnc[3])
                            
                            # Banking deets
                            self.bd_5.setText(banking_db[0])
                            self.bd_6.setText(banking_db[1])
                            self.bd_7.setText(banking_db[2])
                            self.bd_8.setText(banking_db[3])
                            
                            # Totals
                            self.sub_total.setText(str(sub_total))
                            self.discount.setText(str(disc))
                            self.payment_received.setText(str(payment_received))
                            self.amount_owed.setText(str(total_due))
                            
                            # Save and print
                            printer = QPrinter()
                            printer.OutputFormat(1)            
                            printer.setOutputFileName(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf')
                            
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end()
                            
                            printer.OutputFormat(0)
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end() 
                            
                            close_print = sg.popup_ok(f'Invoice {inv_num} - saved succefully as: \n {clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf',
                                    title='Invoice Saved', icon=pps_icon)
                            
                            if close_print == 'OK':
                                self.close()      
                            
                    if __name__ == '__main__':
                        
                        app = QApplication(sys.argv)
                        print_window = Invoice()
                        app.exec_()

            save_inv_data = open(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}.dat', 'wb')
            pickle.dump(inv_data, save_inv_data)
            save_inv_data.close()
            
            invoice_number['current'] = (inv_num +1)
            
            save_inv_num = open(f'{dll_dir}inumdb.dll','wb')  
            pickle.dump(invoice_number, save_inv_num)
            save_inv_num.close()
            
            invoice_history['client'].append(clients_db[values['CS1']][-1])
            invoice_history['inv num'].append(inv_num)
            invoice_history['date'].append(inv_date)
            
            save_inv_hist = open(f'{dll_dir}invhis.dll','wb')
            pickle.dump(invoice_history,save_inv_hist)
            save_inv_hist.close()
            
            window.close()
            new_invoice()

## Load Invoice
def load_invoice(selected_file):
    
    # discount
    discount = [''*i for i in range(0,8)]
    
    try:
        i_load_file = open(f'{dll_dir}inumdb.dll','rb')
        invoice_number = pickle.load(i_load_file)

    except :
        invoice_number = {
        
        'start': 1000, 
        'current': 1000

        }

    inv_num = invoice_number['current']
    ###
    
    ## Required variable
    open_reg = open(f'{dll_dir}registry.dll','rb')
    details = pickle.load(open_reg)
    open_reg.close()
    
    # Load Client Invoice
    split_selected_file = selected_file.split('/')
    selected_acc = (len(split_selected_file)-2)
    selected_client = split_selected_file[selected_acc]
    
    inv_data_load = open(selected_file,'rb')
    inv_data = pickle.load(inv_data_load)

    ##### Create Combo lists
    # 
    code_list = []

    for i in range(0,len(code_codes)):
        code_list.append(code_codes[i] + ' - ' + code_descriptions[i])
    ###
    
    ## Clients
    inv_client_list = []

    for key in clients_db.keys():
        inv_client_list.append(key)
    ###
      
    sg.theme(theme)

    # Frame 1 = Practice name
    frame_1 = [

        [sg.T('', font=(main_font, 20), p=(p_inv))],
        [sg.T(f'{details[0]}', font=(main_font, 20), p=(p_inv))],
        [sg.T('', font=(main_font, 20), p=(p_inv))]

    ]

    # Frame 2 = Practce Address 
    f2_col_1 = [

        [sg.T('Address:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Suburb:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('City:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Postal Code:', font=(main_font, inv_t), p=(p_inv))]

    ]

    f2_col_2 = [

        [sg.T(f'{practice_db[2]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[3]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[4]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[5]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[6]}', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_2 = [

        [sg.Column(f2_col_1, element_justification='l' ), sg.Column(f2_col_2, element_justification='l')]

    ]

    # Frame 3 = Practice Contact details
    f3_col_1 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Contact Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Email:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Website:', font=(main_font, inv_t), p=(p_inv))]

    ]

    f3_col_2 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[0]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{practice_db[7]}', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_3 = [

        [sg.Column(f3_col_1, element_justification='l' ), sg.Column(f3_col_2, element_justification='l')]

    ]

    # Frame 4 = Psychologist details
    frame_4 = [

        [sg.T(f'{details[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{details[2]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    # Frame 5 = BHF and HPCSA reg details
    f5_col_1 = [

        [sg.T('BHF Practice Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('HPCSA Registration Number:', font=(main_font, inv_t), p=(p_inv))],

    ]

    f5_col_2 = [

        [sg.T(f'{details[3]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{details[4]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_5 = [

        [sg.Column(f5_col_1, element_justification='l' ), sg.Column(f5_col_2, element_justification='l')]

    ]

    # Frame 6 - 9 = Inv num and Inv Date
    frame_6 = [

        [sg.T('Invoice Number:', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_7 = [

        [sg.T(inv_num, font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_8 = [

        [sg.CalendarButton('Invoice Date', k='I_DATE', format=('%d %b %y'), target=('IN_DATE'), begin_at_sunday_plus=1)]

    ]

    frame_9 = [

        [sg.I(enable_events=True, k='IN_DATE', font=(main_font, inv_t), s=inv_s, p=(p_inv))]  

    ]

    # Frame 10 - 13 = Account Details
    frame_10 = [

        [sg.T('Account Name:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Client ID Number:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Address:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Suburb:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('City:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Postal Code:', font=(main_font, inv_t), p=(p_inv))]
        
    ]
    
    frame_11 = [

        [sg.T(selected_client, k='CS1', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][0], k='CS0', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][3], k='CS3', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][4], k='CS4', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][5], k='CS5', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][6], k='CS6', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][7], k='CS7', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_12 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Medical Aid:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Medical Aid Number', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Principal Member:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Principal Member ID:', font=(main_font, inv_t), p=(p_inv))]

    ]

    frame_13 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][10], k='CS10', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][11], k='CS11', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][12], k='CS12', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(clients_db[f'{selected_client}'][13], k='CS13', font=(main_font, inv_t), p=(p_inv))]

    ]

    ## Frames 14 - 25 = Invoice Details
    # Session Dates
    frame_14 = [
        
        [sg.I(enable_events=True, k='SD1', font=(main_font, inv_t), s=inv_s, p=(p_inv)),
         sg.CalendarButton('Date', k='CAL1', format=('%d %b %y'), target=('SD1'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD2', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL2', format=('%d %b %y'), target=('SD2'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD3', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL3', format=('%d %b %y'), target=('SD3'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD4', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL4', format=('%d %b %y'), target=('SD4'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD5', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL5', format=('%d %b %y'), target=('SD5'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD6', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL6', format=('%d %b %y'), target=('SD6'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD7', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL7', format=('%d %b %y'), target=('SD7'), begin_at_sunday_plus=1)],
        [sg.I(enable_events=True, k='SD8', font=(main_font, inv_t), s=inv_s, p=(p_inv)), 
         sg.CalendarButton('Date', k='CAL8', format=('%d %b %y'), target=('SD8'), begin_at_sunday_plus=1)]
        
    ]
    
    # Services
    frame_15 = [
        
        [sg.Combo(services_db, inv_data['services'][0], k='SER1', enable_events=True, font=(main_font, inv_t), p=((3,3),(10,6)))],
        [sg.Combo(services_db, inv_data['services'][1], k='SER2', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][2], k='SER3', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][3], k='SER4', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][4], k='SER5', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][5], k='SER6', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][6], k='SER7', enable_events=True, font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.Combo(services_db, inv_data['services'][7], k='SER8', enable_events=True, font=(main_font, inv_t), p=((3,3),(5,6)))]
                  
    ]
    
    # Procedure Codes
    frame_16 = [

        [sg.Combo([], inv_data['pro_codes'][0], k='PC1', font=(main_font, inv_t), s=pc_size, p=((3,3),(10,6)))],
        [sg.Combo([], inv_data['pro_codes'][1], k='PC2', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][2], k='PC3', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][3], k='PC4', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][4], k='PC5', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][5], k='PC6', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][6], k='PC7', font=(main_font, inv_t), s=pc_size, p=(p_inv_cb))],
        [sg.Combo([], inv_data['pro_codes'][7], font=(main_font, inv_t), s=pc_size, p=((3,3),(5,6)))]

    ]
    
    #  Codes
    frame_17 = [

        [sg.Combo(code_list, default_value=inv_data['code'][0], k='code1', enable_events=True, font=(main_font, inv_t),
                  p=((3,3),(10,6)))],
        [sg.Combo(code_list, default_value=inv_data['code'][1], k='code2', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][2], k='code3', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][3], k='code4', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][4], k='code5', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][5], k='code6', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][6], k='code7', enable_events=True, font=(main_font, inv_t),
                  p=(p_inv_cb))],
        [sg.Combo(code_list, default_value=inv_data['code'][7], k='code8', enable_events=True, font=(main_font, inv_t),
                  p=((3,3),(5,6)))]

    ]
    
    # Fees
    frame_18 = [

        [sg.I(inv_data['fees'][0], font=(main_font, inv_t), k="R1", enable_events=True, p=((3,3),(10,6)))],
        [sg.I(inv_data['fees'][1], font=(main_font, inv_t), k="R2", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][2], font=(main_font, inv_t), k="R3", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][3], font=(main_font, inv_t), k="R4", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][4], font=(main_font, inv_t), k="R5", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][5], font=(main_font, inv_t), k="R6", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][6], font=(main_font, inv_t), k="R7", enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['fees'][7], font=(main_font, inv_t), k="R8", enable_events=True, p=((3,3),(5,6)))]
        
    ]
    
    # Discount
    frame_19 = [

        [sg.I(inv_data['discount'][0], font=(main_font, inv_t), k='D1', enable_events=True, p=((3,3),(10,6)))],
        [sg.I(inv_data['discount'][1], font=(main_font, inv_t), k='D2', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][2], font=(main_font, inv_t), k='D3', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][3], font=(main_font, inv_t), k='D4', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][4], font=(main_font, inv_t), k='D5', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][5], font=(main_font, inv_t), k='D6', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][6], font=(main_font, inv_t), k='D7', enable_events=True, p=(p_inv_cb))],
        [sg.I(inv_data['discount'][7], font=(main_font, inv_t), k='D8', enable_events=True, p=((3,3),(5,6)))]

    ]
    
    # Total
    frame_20 = [

        [sg.T(inv_data['total'][0], k='AO1', font=(main_font, inv_t), p=((3,3),(10,6)))],
        [sg.T(inv_data['total'][1], k='AO2', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][2], k='AO3', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][3], k='AO4', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][4], k='AO5', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][5], k='AO6', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][6], k='AO7', font=(main_font, inv_t), p=(p_inv_cb))],
        [sg.T(inv_data['total'][7], k='AO8', font=(main_font, inv_t), p=((3,3),(5,6)))]

    ]

    # Frame 30 = T and C
    # T's and C's
    try:
        load_file = open('tnc.dll','rb')
        tnc = pickle.load(load_file)

    except:
        tnc = ['','','','']
        
    frame_30 = [

        [sg.I(f'{tnc[0]}', k='T1', font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(f'{tnc[1]}', k='T2', font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(f'{tnc[2]}', k='T3', font=(main_font, inv_t), s=115, p=(p_inv))],
        [sg.I(f'{tnc[3]}', k='T4', font=(main_font, inv_t), s=115, p=(p_inv))]

    ]

    # Frame 31 - 33 = Banking Details
    frame_31 = [

        [sg.T('Practice Banking Details:', font=(main_font, inv_t, 'underline'), p=(p_inv))],
        [sg.T('Account Name:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Bank:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Branch Code:', font=(main_font, inv_t), p=(p_inv))],
        [sg.T('Account Number:', font=(main_font, inv_t), p=(p_inv))],

    ]
    
    frame_32 = [

        [sg.T('', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[0]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[1]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[2]}', font=(main_font, inv_t), p=(p_inv))],
        [sg.T(f'{banking_db[3]}', font=(main_font, inv_t), p=(p_inv))],

    ]

    frame_33 = [

        [sg.T('', font=(main_font,inv_t), p=(p_inv))],
        [sg.T('Please email proof of payment to:', font=(main_font, inv_t, 'italic'), p=(p_inv))],
        [sg.T(f'{practice_db[1]}', font=(main_font, inv_t, 'bold'), p=(p_inv))],
        [sg.T('Please use "Account Name" as reference.', text_color='red',font=(main_font, inv_t, 'italic'), p=(p_inv))],
        [sg.T('', font=(main_font,inv_t), p=(p_inv))]

    ]

    # Combined layout
    final_frame = [

        # Practice Name, Address and Contact details
        [sg.Frame('', layout=frame_1, s=(250,120), element_justification='c'), 
         sg.Frame('', layout=frame_2, s=(250,120)), 
         sg.Frame('', layout=frame_3, s=(300,120))],

        # Psychologist, Highest Qualification, BHF Registration, HPCSA registration
        [sg.Frame('', layout=frame_4, s=(355,50)), 
         sg.Frame('', layout=frame_5, s=(455,50))],

        # Invoice Number and Date
        [sg.Frame('', layout=frame_6, s=(195,30), element_justification='c'), 
         sg.Frame('', layout=frame_7, s=(200,30), element_justification='c'),
         sg.Frame('', layout=frame_8, s=(195,30), element_justification='c'), 
         sg.Frame('', layout=frame_9, s=(200,30), element_justification='c')],

        # Client and Medical aid details
        [sg.Frame('', layout=frame_10, s=(195,155)), 
         sg.Frame('', layout=frame_11, s=(200,155)),
         sg.Frame('', layout=frame_12, s=(195,155)), 
         sg.Frame('', layout=frame_13, s=(200,155))],   

        # Invoie Data
        [sg.Frame('Session Date:', layout=frame_14, s=(120,275)),
         sg.Frame('Service', layout=frame_15, s=(145,275)), 
         sg.Frame('Procedure Code', layout=frame_16, s=(110,275)),
         sg.Frame(' Code', layout=frame_17, s=(85,275)), 
         sg.Frame('Fee', layout=frame_18, s=(100,275)),
         sg.Frame('Discount', layout=frame_19, s=(100,275)), 
         sg.Frame('Amount', layout=frame_20, s=(100,275))],

        # Terms and Conditions
        [sg.Frame('Terms and Conditions:', layout=frame_30, s=(820,110))],

        # Banking details
        [sg.Frame('', layout=frame_31, s=(250,115)), 
         sg.Frame('', layout=frame_32, s=(300,115)), 
         sg.Frame('', layout=frame_33, s=(250,115))],

        # Buttons
        [sg.B(button_text='Save & Print Invoice', font=(main_font,btf_size), border_width='5px', p=10),
         sg.B(button_text='Save Invoice', font=(main_font,btf_size), border_width='5px', p=10),
         sg.B(button_text='Back', font=(main_font,eb_size), border_width='4px', p=10),
         sg.Exit(font=(main_font,eb_size), size=15, p=(10,10))]

    ]
    
    # Creating Final Frame
    layout = [
        
        [sg.Frame('', layout=final_frame)]
        
    ]

    # Creating GUI
    window = sg.Window(f'{details[0]}'+' - INV # ' + f'{inv_num}', layout,
                       icon=pps_icon, element_justification='c',
                       relative_location=(0,-50))
    
    while True:
        
        event, values = window.read() 

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event in 'Back':
            window.close()
            invoice_menu()

        # Selecting Session Date
        if event in 'SD1':           
            window['SD1'].Update(values['SD1'])
                        
        if event in 'SD2':
            window['SD2'].Update(values['SD2'])
            
        if event in 'SD3':
            window['SD3'].Update(values['SD3'])
            
        if event in 'SD4':
            window['SD4'].Update(values['SD4'])
            
        if event in 'SD5':
            window['SD5'].Update(values['SD5'])
            
        if event in 'SD6':
            window['SD6'].Update(values['SD6'])
            
        if event in 'SD7':
            window['SD7'].Update(values['SD7'])
            
        if event in 'SD8':
            window['SD8'].Update(values['SD8'])
            
        # Selecting Invoice date
        if event in 'IN_DATE':
            window['IN_DATE'].Update(values['IN_DATE'])
            
        # Selecting  Codes
        if event in 'code1':
            code_result = values['code1'].split(' - ', 1)
            window['code1'].Update(code_result[0])
            
        if event in 'code2':
            code_result = values['code2'].split(' - ', 1)
            window['code2'].Update(code_result[0])
            
        if event in 'code3':
            code_result = values['code3'].split(' - ', 1)
            window['code3'].Update(code_result[0])
            
        if event in 'code4':
            code_result = values['code4'].split(' - ', 1)
            window['code4'].Update(code_result[0])
            
        if event in 'code5':
            code_result = values['code5'].split(' - ', 1)
            window['code5'].Update(code_result[0])
            
        if event in 'code6':
            code_result = values['code6'].split(' - ', 1)
            window['code6'].Update(code_result[0])
            
        if event in 'code7':
            code_result = values['code7'].split(' - ', 1)
            window['code7'].Update(code_result[0])
            
        if event in 'code8':
            code_result = values['code8'].split(' - ', 1)
            window['code8'].Update(code_result[0])
            
        # Selecting Service and setting -> Procedure codes
        if event in 'SER1':

            try:
                codes_list = pro_codes[values['SER1']]
                window['PC1'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER2':

            try:
                codes_list = pro_codes[values['SER2']]
                window['PC2'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER3':

            try:
                codes_list = pro_codes[values['SER3']]
                window['PC3'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER4':

            try:
                codes_list = pro_codes[values['SER4']]
                window['PC4'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER5':

            try:
                codes_list = pro_codes[values['SER5']]
                window['PC5'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER6':

            try:
                codes_list = pro_codes[values['SER6']]
                window['PC6'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER7':

            try:
                codes_list = pro_codes[values['SER7']]
                window['PC7'].update(values=codes_list)
                
            except:
                pass

        if event in 'SER8':

            try:
                codes_list = pro_codes[values['SER8']]
                window['PC8'].update(values=codes_list)
               
            except:
                pass

        # Update Amount owed -> Fees
        if event in 'R1':
            
            if values['SER1'] == 'Payment Received':

                try:
                    window['PC1'].update(values['PC1'])
                    total = locale.currency((float(values['R1'])), grouping=True)
                    window['AO1'].update(f'({total})')

                except:
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(float(values['R1']), grouping=True))
                
                except:
               
                    window['PC1'].update(values['PC1'])
                    window['AO1'].update(locale.currency(0, grouping=True))
                    
        # 2
        if event in 'R2':

            if values['SER2'] == 'Payment Received':

                try:
                    window['PC2'].update(values['PC2'])
                    total = locale.currency((float(values['R2'])), grouping=True)
                    window['AO2'].update(f'({total})')

                except:
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(float(values['R2']), grouping=True))
                
                except:
               
                    window['PC2'].update(values['PC2'])
                    window['AO2'].update(locale.currency(0, grouping=True))
                    
        # 3       
        if event in 'R3':

            if values['SER3'] == 'Payment Received':

                try:
                    window['PC3'].update(values['PC3'])
                    total = locale.currency((float(values['R3'])), grouping=True)
                    window['AO3'].update(f'({total})')

                except:
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(float(values['R3']), grouping=True))
                
                except:
               
                    window['PC3'].update(values['PC3'])
                    window['AO3'].update(locale.currency(0, grouping=True))
                
        # 4        
        if event in 'R4':

            if values['SER4'] == 'Payment Received':

                try:
                    window['PC4'].update(values['PC4'])
                    total = locale.currency((float(values['R4'])), grouping=True)
                    window['AO4'].update(f'({total})')

                except:
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(float(values['R4']), grouping=True))
                
                except:
               
                    window['PC4'].update(values['PC4'])
                    window['AO4'].update(locale.currency(0, grouping=True))
                
        # 5        
        if event in 'R5':

            if values['SER5'] == 'Payment Received':

                try:
                    window['PC5'].update(values['PC5'])
                    total = locale.currency((float(values['R5'])), grouping=True)
                    window['AO5'].update(f'({total})')

                except:
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(float(values['R5']), grouping=True))
                
                except:
               
                    window['PC5'].update(values['PC5'])
                    window['AO5'].update(locale.currency(0, grouping=True))
                
        # 6        
        if event in 'R6':

            if values['SER6'] == 'Payment Received':

                try:
                    window['PC6'].update(values['PC6'])
                    total = locale.currency((float(values['R6'])), grouping=True)
                    window['AO6'].update(f'({total})')

                except:
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(float(values['R6']), grouping=True))
                
                except:
               
                    window['PC6'].update(values['PC6'])
                    window['AO6'].update(locale.currency(0, grouping=True))
                
        # 7        
        if event in 'R7':

            if values['SER7'] == 'Payment Received':

                try:
                    window['PC7'].update(values['PC7'])
                    total = locale.currency((float(values['R7'])), grouping=True)
                    window['AO7'].update(f'({total})')

                except:
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(float(values['R7']), grouping=True))
                
                except:
               
                    window['PC7'].update(values['PC7'])
                    window['AO7'].update(locale.currency(0, grouping=True))
                
        # 8        
        if event in 'R8':

            if values['SER28'] == 'Payment Received':

                try:
                    window['PC8'].update(values['PC8'])
                    total = locale.currency((float(values['R8'])), grouping=True)
                    window['AO8'].update(f'({total})')

                except:
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(0, grouping=True))
            
            else:
                
                try:
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(float(values['R8']), grouping=True))
                
                except:
               
                    window['PC8'].update(values['PC8'])
                    window['AO8'].update(locale.currency(0, grouping=True))
        
        # Update Amount owed --> Discount
        if event in 'D1':

            try:
                discount[0] = float(values['D1'])
                fees_1 = float(values['R1'])
                
                window['PC1'].update(values['PC1'])                
                window['AO1'].update(locale.currency((fees_1 - discount[0]), grouping=True)) 

            except:
                discount[0] = 0
                fees_1 = float(values['R1'])
                
                window['PC1'].update(values['PC1'])
                window['AO1'].update(locale.currency((fees_1 - discount[0]), grouping=True))

        # 2
        if event in 'D2':

            try:
                discount[1] = float(values['D2'])
                fees_2 = float(values['R2'])
                
                window['PC2'].update(values['PC2'])                
                window['AO2'].update(locale.currency((fees_2 - discount[1]), grouping=True)) 

            except:
                discount[1] = 0
                fees_2 = float(values['R2'])
                
                window['PC2'].update(values['PC2'])
                window['AO2'].update(locale.currency((fees_2 - discount[1]), grouping=True))

        # 3
        if event in 'D3':

            try:
                discount[2] = float(values['D3'])
                fees_3 = float(values['R3'])
                
                window['PC3'].update(values['PC3'])
                window['AO3'].update(locale.currency((fees_3 - discount[2]), grouping=True)) 

            except:
                discount[2] = 0
                fees_3 = float(values['R3'])
                
                window['PC3'].update(values['PC3'])
                window['AO3'].update(locale.currency((fees_3 - discount[2]), grouping=True))

        # 4
        if event in 'D4':

            try:
                discount[3] = float(values['D4'])
                fees_4 = float(values['R4'])
                
                window['PC4'].update(values['PC4'])
                window['AO4'].update(locale.currency((fees_4 - discount[3]), grouping=True)) 

            except:
                discount[3] = 0
                fees_4 = float(values['R4'])
                
                window['PC4'].update(values['PC4'])
                window['AO4'].update(locale.currency((fees_4 - discount[3]), grouping=True))

        # 5
        if event in 'D5':

            try:
                discount[4] = float(values['D5'])
                fees_5 = float(values['R5'])
                
                window['PC5'].update(values['PC5'])
                window['AO5'].update(locale.currency((fees_5 - discount[4]), grouping=True)) 

            except:
                discount[4] = 0
                fees_5 = float(values['R5'])
                
                window['PC5'].update(values['PC5'])
                window['AO5'].update(locale.currency((fees_5 - discount[4]), grouping=True))

        # 6
        if event in 'D6':

            try:
                discount[5] = float(values['D6'])
                fees_6 = float(values['R6'])
                
                window['PC6'].update(values['PC6'])
                window['AO6'].update(locale.currency((fees_6 - discount[5]), grouping=True)) 

            except:
                discount[5] = 0
                fees_6 = float(values['R6'])
                
                window['PC6'].update(values['PC6'])
                window['AO6'].update(locale.currency((fees_6 - discount[5]), grouping=True))

        # 7
        if event in 'D7':

            try:
                discount[6] = float(values['D7'])
                fees_7 = float(values['R7'])
                
                window['PC7'].update(values['PC7'])
                window['AO7'].update(locale.currency((fees_7 - discount[6]), grouping=True)) 

            except:
                discount[6] = 0
                fees_7 = float(values['R7'])
                
                window['PC7'].update(values['PC7'])
                window['AO7'].update(locale.currency((fees_7 - discount[6]), grouping=True))

        # 8
        if event in 'D8':

            try:
                discount[7] = float(values['D8'])
                fees_8 = float(values['R8'])
                
                window['PC8'].update(values['PC8'])
                window['AO8'].update(locale.currency((fees_8 - discount[7]), grouping=True)) 

            except:
                discount[7] = 0
                fees_8 = float(values['R8'])
                
                window['PC8'].update(values['PC8'])
                window['AO8'].update(locale.currency((fees_8 - discount[7]), grouping=True))

        # Save Invoice
        if event in 'Save Invoice':
            
            #Check Inv Date
            while values['IN_DATE'] == '':
                
                sg.popup_ok('Please select Invoice Date:', title='Invalid Invoice Date',
                            font=('Calibri',20), icon=pps_icon)
                break

            else:
                
                inv_date = values['IN_DATE']
                
                # Check Session Date
                while values['SD1'] == '':
                    
                    sg.popup_ok('Please select at least 1 Session Date:', title='Please select a Session Date',
                                font=('Calibri',20), icon=pps_icon)
                    break
                    
                else:
                    
                    open_reg = open(f'{dll_dir}registry.dll','rb')
                    registry = pickle.load(open_reg)
                    
                    sub_total = 0
                    disc = 0
                    payment_received = 0
                    total_due = 0
                    
                    file_acc_name = selected_client
                    file_date = values['IN_DATE']

                    # Creating / Opening save folder
                    parent_dir = os.getcwd()
                    inv_dir = parent_dir + '\\Client Invoices\\'
                    client_dir = inv_dir + file_acc_name
                    
                    try:
                        # Create Client Invoices Folderd
                        os.mkdir(inv_dir)
                        
                        try:
                            # Create Client Folder
                            os.mkdir(client_dir)
                            
                        except FileExistsError:
                            pass
                            # Client Folder already exists

                    except FileExistsError:              
                        # Client Invoices Folder already exists, try creating Client Folder
                        try:                  
                            # Create Client Folder
                            os.mkdir(client_dir)
                        
                        except FileExistsError:
                            pass
                            # Client Folder already exists     
                            
                    # Capturing Invoice data
                    inv_data = {
                        'dates': [''*i for i in range(0,8)],
                        'services': [''*i for i in range(0,8)],
                        'pro_codes': [''*i for i in range(0,8)],
                        'code': [''*i for i in range(0,8)],
                        'fees': [''*i for i in range(0,8)],
                        'discount': [''*i for i in range(0,8)],
                        'payment_received': [''*i for i in range(0,8)],
                        'total': [''*i for i in range(0,8)]
                        }
                    
                    for i in range(0,8):    
                        
                        if values[f'SD{i+1}'] == '':
                        
                            inv_data['dates'][i] = ''
                            inv_data['services'][i] = ''
                            inv_data['pro_codes'][i] = ''
                            inv_data['code'][i] = ''
                            inv_data['fees'][i] = ''
                            inv_data['discount'][i] = ''
                            inv_data['payment_received'][i] = ''
                            inv_data['total'][i] = ''
                        
                        else:
                            
                            inv_data['dates'][i] = (values[f'SD{i+1}'])
                            inv_data['services'][i] = (values[f'SER{i+1}'])
                            inv_data['pro_codes'][i] = (values[f'PC{i+1}'])
                            inv_data['code'][i] = (values[f'code{i+1}'])
                            
                            if values[f'SER{i+1}'] == 'Payment Received':
                                
                                inv_data['payment_received'][i] = (values[f'R{i+1}'])
                                inv_data['fees'][i] = '' 
                                
                                payment_received = payment_received + float(values[f'R{i+1}'])

                            else: 
                                
                                inv_data['fees'][i] = (values[f'R{i+1}'])
                                inv_data['payment_received'][i] = ''
                                
                            # check for discount to calculate inv_data['total']
                            if values[f'D{i+1}'] == '':
                                
                                inv_data['discount'][i] = ''
                                inv_data['total'][i] = (values[f'R{i+1}'])
                                
                                sub_total = sub_total + float(inv_data['fees'][i])
                                
                            else: 
                                
                                inv_data['discount'][i] = str(discount[i])
                                disc = disc + float(inv_data['discount'][i])
                                
                                inv_data['total'][i] = (float(inv_data['fees'][i]) - float(inv_data['discount'][i]))
                                
                                sub_total = sub_total + float(inv_data['fees'][i])

                    total_due = sub_total - disc - payment_received                
                                        
                    for i in range(0,4):
                        tnc[i] = values[f'T{i+1}']
                        
                    tnc_save = open(f'{dll_dir}tnc.dll','wb')
                    pickle.dump(tnc, tnc_save)
                    tnc_save.close()               
                    
                    class Invoice(QWidget):
                        def __init__(self):
                            super(Invoice, self).__init__()
                            loadUi(f'{ui_dir}invoice_temp.ui', self)
                        
                            # Practice Name
                            self.practice_name.setText(registry[0])
                            
                            # Practice Address
                            self.l1.setText(practice_db[2])
                            self.l2.setText(practice_db[3])
                            self.l3.setText(practice_db[4])
                            self.l4.setText(practice_db[5])
                            self.l5.setText(practice_db[6])
                            
                            # Practice contacts
                            self.l6.setText(practice_db[0])
                            self.l7.setText(practice_db[1])
                            self.l8.setText(practice_db[7])

                            # registration details:
                            self.psyc.setText(registry[1])
                            self.quali.setText(registry[2])
                            self.bhf_num.setText(registry[3])
                            self.hpcsa_num.setText(registry[4])
                            
                            # Inv num and date
                            self.inv_num_3.setText(str(inv_num))
                            self.inv_date_3.setText(inv_date)
                            
                            # Client details values['CS1']
                            ## can replace values['CS1'] with selected_client
                            self.l9_6.setText(clients_db[values['CS1']][-1]) # acc name
                            self.l9_6.setText(clients_db[values['CS1']][0]) # id
                            self.l9_6.setText(clients_db[values['CS1']][3]) # ad 1
                            self.l9_6.setText(clients_db[values['CS1']][4]) # ad 2
                            self.l9_6.setText(clients_db[values['CS1']][5]) # sub
                            self.l9_6.setText(clients_db[values['CS1']][6]) # city
                            self.l9_6.setText(clients_db[values['CS1']][7]) # postal
                            self.l9_6.setText(clients_db[values['CS1']][10]) # med aid
                            self.l9_6.setText(clients_db[values['CS1']][11]) # med aid num
                            self.l9_6.setText(clients_db[values['CS1']][12]) # prince
                            self.l9_6.setText(clients_db[values['CS1']][13]) # prince id
                            
                            # Inv data
                            # SD
                            self.sd_1.setText(inv_data['dates'][0])
                            self.sd_2.setText(inv_data['dates'][1])
                            self.sd_3.setText(inv_data['dates'][2])
                            self.sd_4.setText(inv_data['dates'][3])
                            self.sd_5.setText(inv_data['dates'][4])
                            self.sd_6.setText(inv_data['dates'][5])
                            self.sd_7.setText(inv_data['dates'][6])
                            self.sd_8.setText(inv_data['dates'][7])
                            self.sd_9.setText('')
                            self.sd_10.setText('')
                            self.sd_11.setText('')
                            self.sd_12.setText('')
                            
                            # Service
                            self.services_1.setText(inv_data['services'][0])
                            self.services_2.setText(inv_data['services'][1])
                            self.services_3.setText(inv_data['services'][2])
                            self.services_4.setText(inv_data['services'][3])
                            self.services_5.setText(inv_data['services'][4])
                            self.services_6.setText(inv_data['services'][5])
                            self.services_7.setText(inv_data['services'][6])
                            self.services_8.setText(inv_data['services'][7])
                            self.services_9.setText('')
                            self.services_10.setText('')
                            self.services_11.setText('')
                            self.services_12.setText('')
                            
                            # PC
                            self.pc_1.setText(inv_data['pro_codes'][0])
                            self.pc_2.setText(inv_data['pro_codes'][1])
                            self.pc_3.setText(inv_data['pro_codes'][2])
                            self.pc_4.setText(inv_data['pro_codes'][3])
                            self.pc_5.setText(inv_data['pro_codes'][4])
                            self.pc_6.setText(inv_data['pro_codes'][5])
                            self.pc_7.setText(inv_data['pro_codes'][6])
                            self.pc_8.setText(inv_data['pro_codes'][7])
                            self.pc_9.setText('')
                            self.pc_10.setText('')
                            self.pc_11.setText('')
                            self.pc_12.setText('')
                            
                            # code
                            self.code_1.setText(inv_data['code'][0])
                            self.code_2.setText(inv_data['code'][1])
                            self.code_3.setText(inv_data['code'][2])
                            self.code_4.setText(inv_data['code'][3])
                            self.code_5.setText(inv_data['code'][4])
                            self.code_6.setText(inv_data['code'][5])
                            self.code_7.setText(inv_data['code'][6])
                            self.code_8.setText(inv_data['code'][7])
                            self.code_9.setText('')
                            self.code_10.setText('')
                            self.code_11.setText('')
                            self.code_12.setText('')
                            
                            # Fees
                            self.fees_1.setText(inv_data['fees'][0])
                            self.fees_2.setText(inv_data['fees'][1])
                            self.fees_3.setText(inv_data['fees'][2])
                            self.fees_4.setText(inv_data['fees'][3])
                            self.fees_5.setText(inv_data['fees'][4])
                            self.fees_6.setText(inv_data['fees'][5])
                            self.fees_7.setText(inv_data['fees'][6])
                            self.fees_8.setText(inv_data['fees'][7])
                            self.fees_9.setText('')
                            self.fees_10.setText('')
                            self.fees_11.setText('')
                            self.fees_12.setText('')
                            
                            # Disc
                            self.disc_1.setText(inv_data['discount'][0])
                            self.disc_2.setText(inv_data['discount'][1])
                            self.disc_3.setText(inv_data['discount'][2])
                            self.disc_4.setText(inv_data['discount'][3])
                            self.disc_5.setText(inv_data['discount'][4])
                            self.disc_6.setText(inv_data['discount'][5])
                            self.disc_7.setText(inv_data['discount'][6])
                            self.disc_8.setText(inv_data['discount'][7])
                            self.disc_9.setText('')
                            self.disc_10.setText('')
                            self.disc_11.setText('')
                            self.disc_12.setText('')
                            
                            # AO
                            self.ao_1.setText(str(inv_data['total'][0]))
                            self.ao_2.setText(str(inv_data['total'][1]))
                            self.ao_3.setText(str(inv_data['total'][2]))
                            self.ao_4.setText(str(inv_data['total'][3]))
                            self.ao_5.setText(str(inv_data['total'][4]))
                            self.ao_6.setText(str(inv_data['total'][5]))
                            self.ao_7.setText(str(inv_data['total'][6]))
                            self.ao_8.setText(str(inv_data['total'][7]))
                            self.ao_9.setText('')
                            self.ao_10.setText('')
                            self.ao_11.setText('')
                            self.ao_12.setText('')
                            
                            # Terms and conditions
                            self.tnc_1.setText(tnc[0])
                            self.tnc_2.setText(tnc[1])
                            self.tnc_3.setText(tnc[2])
                            self.tnc_4.setText(tnc[3])
                            
                            # Banking deets
                            self.bd_5.setText(banking_db[0])
                            self.bd_6.setText(banking_db[1])
                            self.bd_7.setText(banking_db[2])
                            self.bd_8.setText(banking_db[3])
                            
                            # Totals
                            self.sub_total.setText(str(sub_total))
                            self.discount.setText(str(disc))
                            self.payment_received.setText(str(payment_received))
                            self.amount_owed.setText(str(total_due))
                            
                            # Save
                            printer = QPrinter()                          
                            printer.OutputFormat(1)
                            printer.setOutputFileName(client_dir + '\\' + f'{clients_db[selected_client][-1]}_INV-{inv_num}_{file_date}.pdf')
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end() 
                            
                            close_print = sg.popup_ok(f'Invoice {inv_num} - saved succefully as: \n {clients_db[selected_client][-1]}_INV-{inv_num}_{file_date}.pdf',
                                    title='Invoice Saved', icon=pps_icon)
                            
                            if close_print == 'OK':
                                self.close()      
                            
                    if __name__ == '__main__':
                        
                        app = QApplication(sys.argv)
                        print_window = Invoice()
                        
            save_inv_data = open(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}.dat', 'wb')
            pickle.dump(inv_data, save_inv_data)
            save_inv_data.close()
            
            invoice_number['current'] = (inv_num +1)
            
            save_inv_num = open(f'{dll_dir}inumdb.dll','wb')  
            pickle.dump(invoice_number, save_inv_num)
            save_inv_num.close()
            
            invoice_history['client'].append(clients_db[values['CS1']][-1])
            invoice_history['inv num'].append(inv_num)
            invoice_history['date'].append(inv_date)
            
            save_inv_hist = open(f'{dll_dir}invhis.dll','wb')
            pickle.dump(invoice_history,save_inv_hist)
            save_inv_hist.close()
            
            window.close()
            new_invoice()

        # Save and Print Invoice
        if event in 'Save & Print Invoice':
            
            #Check Inv Date
            while values['IN_DATE'] == '':
                
                sg.popup_ok('Please select Invoice Date:', title='Invalid Invoice Date',
                            font=('Calibri',20), icon=pps_icon)
                break

            else:
                
                inv_date = values['IN_DATE']
                
                # Check Session Date
                while values['SD1'] == '':
                    
                    sg.popup_ok('Please select at least 1 Session Date:', title='Please select a Session Date',
                                font=('Calibri',20), icon=pps_icon)
                    break
                    
                else:
                    
                    open_reg = open(f'{dll_dir}registry.dll','rb')
                    registry = pickle.load(open_reg)
                    
                    sub_total = 0
                    disc = 0
                    payment_received = 0
                    total_due = 0
                    
                    file_acc_name = values['CS1']
                    file_date = values['IN_DATE']

                    # Creating / Opening save folder
                    parent_dir = os.getcwd()
                    inv_dir = parent_dir + '\\Client Invoices\\'
                    client_dir = inv_dir + file_acc_name
                    
                    try:
                        # Create Client Invoices Folderd
                        os.mkdir(inv_dir)
                        
                        try:
                            # Create Client Folder
                            os.mkdir(client_dir)
                            
                        except FileExistsError:
                            pass
                            # Client Folder already exists

                    except FileExistsError:              
                        # Client Invoices Folder already exists, try creating Client Folder
                        try:                  
                            # Create Client Folder
                            os.mkdir(client_dir)
                        
                        except FileExistsError:
                            pass
                            # Client Folder already exists     
                            
                    # Capturing Invoice data
                    inv_data = {
                        'dates': [''*i for i in range(0,8)],
                        'services': [''*i for i in range(0,8)],
                        'pro_codes': [''*i for i in range(0,8)],
                        'code': [''*i for i in range(0,8)],
                        'fees': [''*i for i in range(0,8)],
                        'discount': [''*i for i in range(0,8)],
                        'payment_received': [''*i for i in range(0,8)],
                        'total': [''*i for i in range(0,8)]
                        }
                    
                    for i in range(0,8):    
                        
                        if values[f'SD{i+1}'] == '':
                        
                            inv_data['dates'][i] = ''
                            inv_data['services'][i] = ''
                            inv_data['pro_codes'][i] = ''
                            inv_data['code'][i] = ''
                            inv_data['fees'][i] = ''
                            inv_data['discount'][i] = ''
                            inv_data['payment_received'][i] = ''
                            inv_data['total'][i] = ''
                        
                        else:
                            
                            inv_data['dates'][i] = (values[f'SD{i+1}'])
                            inv_data['services'][i] = (values[f'SER{i+1}'])
                            inv_data['pro_codes'][i] = (values[f'PC{i+1}'])
                            inv_data['code'][i] = (values[f'code{i+1}'])
                            
                            if values[f'SER{i+1}'] == 'Payment Received':
                                
                                inv_data['payment_received'][i] = (values[f'R{i+1}'])
                                inv_data['fees'][i] = '' 
                                
                                payment_received = payment_received + float(values[f'R{i+1}'])

                            else: 
                                
                                inv_data['fees'][i] = (values[f'R{i+1}'])
                                inv_data['payment_received'][i] = ''
                                
                            # check for discount to calculate inv_data['total']
                            if values[f'D{i+1}'] == '':
                                
                                inv_data['discount'][i] = ''
                                inv_data['total'][i] = (values[f'R{i+1}'])
                                
                                sub_total = sub_total + float(inv_data['fees'][i])
                                
                            else: 
                                
                                inv_data['discount'][i] = str(discount[i])
                                disc = disc + float(inv_data['discount'][i])
                                
                                inv_data['total'][i] = (float(inv_data['fees'][i]) - float(inv_data['discount'][i]))
                                
                                sub_total = sub_total + float(inv_data['fees'][i])

                    total_due = sub_total - disc - payment_received                
                                        
                    for i in range(0,4):
                        tnc[i] = values[f'T{i+1}']
                        
                    tnc_save = open(f'{dll_dir}tnc.dll','wb')
                    pickle.dump(tnc, tnc_save)
                    tnc_save.close()               
                    
                    class Invoice(QWidget):
                        def __init__(self):
                            super(Invoice, self).__init__()
                            loadUi(f'{ui_dir}invoice_temp.ui', self)
                        
                            # Practice Name
                            self.practice_name.setText(registry[0])
                            
                            # Practice Address
                            self.l1.setText(practice_db[2])
                            self.l2.setText(practice_db[3])
                            self.l3.setText(practice_db[4])
                            self.l4.setText(practice_db[5])
                            self.l5.setText(practice_db[6])
                            
                            # Practice contacts
                            self.l6.setText(practice_db[0])
                            self.l7.setText(practice_db[1])
                            self.l8.setText(practice_db[7])

                            # registration details:
                            self.psyc.setText(registry[1])
                            self.quali.setText(registry[2])
                            self.bhf_num.setText(registry[3])
                            self.hpcsa_num.setText(registry[4])
                            
                            # Inv num and date
                            self.inv_num_3.setText(str(inv_num))
                            self.inv_date_3.setText(inv_date)
                            
                            # Client detailsvalues['CS1']
                            self.l9_6.setText(clients_db[values['CS1']][-1]) # acc name
                            self.l9_6.setText(clients_db[values['CS1']][0]) # id
                            self.l9_6.setText(clients_db[values['CS1']][3]) # ad 1
                            self.l9_6.setText(clients_db[values['CS1']][4]) # ad 2
                            self.l9_6.setText(clients_db[values['CS1']][5]) # sub
                            self.l9_6.setText(clients_db[values['CS1']][6]) # city
                            self.l9_6.setText(clients_db[values['CS1']][7]) # postal
                            self.l9_6.setText(clients_db[values['CS1']][10]) # med aid
                            self.l9_6.setText(clients_db[values['CS1']][11]) # med aid num
                            self.l9_6.setText(clients_db[values['CS1']][12]) # prince
                            self.l9_6.setText(clients_db[values['CS1']][13]) # prince id
                            
                            # Inv data
                            # SD
                            self.sd_1.setText(inv_data['dates'][0])
                            self.sd_2.setText(inv_data['dates'][1])
                            self.sd_3.setText(inv_data['dates'][2])
                            self.sd_4.setText(inv_data['dates'][3])
                            self.sd_5.setText(inv_data['dates'][4])
                            self.sd_6.setText(inv_data['dates'][5])
                            self.sd_7.setText(inv_data['dates'][6])
                            self.sd_8.setText(inv_data['dates'][7])
                            self.sd_9.setText('')
                            self.sd_10.setText('')
                            self.sd_11.setText('')
                            self.sd_12.setText('')
                            
                            # Service
                            self.services_1.setText(inv_data['services'][0])
                            self.services_2.setText(inv_data['services'][1])
                            self.services_3.setText(inv_data['services'][2])
                            self.services_4.setText(inv_data['services'][3])
                            self.services_5.setText(inv_data['services'][4])
                            self.services_6.setText(inv_data['services'][5])
                            self.services_7.setText(inv_data['services'][6])
                            self.services_8.setText(inv_data['services'][7])
                            self.services_9.setText('')
                            self.services_10.setText('')
                            self.services_11.setText('')
                            self.services_12.setText('')
                            
                            # PC
                            self.pc_1.setText(inv_data['pro_codes'][0])
                            self.pc_2.setText(inv_data['pro_codes'][1])
                            self.pc_3.setText(inv_data['pro_codes'][2])
                            self.pc_4.setText(inv_data['pro_codes'][3])
                            self.pc_5.setText(inv_data['pro_codes'][4])
                            self.pc_6.setText(inv_data['pro_codes'][5])
                            self.pc_7.setText(inv_data['pro_codes'][6])
                            self.pc_8.setText(inv_data['pro_codes'][7])
                            self.pc_9.setText('')
                            self.pc_10.setText('')
                            self.pc_11.setText('')
                            self.pc_12.setText('')
                            
                            # code
                            self.code_1.setText(inv_data['code'][0])
                            self.code_2.setText(inv_data['code'][1])
                            self.code_3.setText(inv_data['code'][2])
                            self.code_4.setText(inv_data['code'][3])
                            self.code_5.setText(inv_data['code'][4])
                            self.code_6.setText(inv_data['code'][5])
                            self.code_7.setText(inv_data['code'][6])
                            self.code_8.setText(inv_data['code'][7])
                            self.code_9.setText('')
                            self.code_10.setText('')
                            self.code_11.setText('')
                            self.code_12.setText('')
                            
                            # Fees
                            self.fees_1.setText(inv_data['fees'][0])
                            self.fees_2.setText(inv_data['fees'][1])
                            self.fees_3.setText(inv_data['fees'][2])
                            self.fees_4.setText(inv_data['fees'][3])
                            self.fees_5.setText(inv_data['fees'][4])
                            self.fees_6.setText(inv_data['fees'][5])
                            self.fees_7.setText(inv_data['fees'][6])
                            self.fees_8.setText(inv_data['fees'][7])
                            self.fees_9.setText('')
                            self.fees_10.setText('')
                            self.fees_11.setText('')
                            self.fees_12.setText('')
                            
                            # Disc
                            self.disc_1.setText(inv_data['discount'][0])
                            self.disc_2.setText(inv_data['discount'][1])
                            self.disc_3.setText(inv_data['discount'][2])
                            self.disc_4.setText(inv_data['discount'][3])
                            self.disc_5.setText(inv_data['discount'][4])
                            self.disc_6.setText(inv_data['discount'][5])
                            self.disc_7.setText(inv_data['discount'][6])
                            self.disc_8.setText(inv_data['discount'][7])
                            self.disc_9.setText('')
                            self.disc_10.setText('')
                            self.disc_11.setText('')
                            self.disc_12.setText('')
                            
                            # AO
                            self.ao_1.setText(str(inv_data['total'][0]))
                            self.ao_2.setText(str(inv_data['total'][1]))
                            self.ao_3.setText(str(inv_data['total'][2]))
                            self.ao_4.setText(str(inv_data['total'][3]))
                            self.ao_5.setText(str(inv_data['total'][4]))
                            self.ao_6.setText(str(inv_data['total'][5]))
                            self.ao_7.setText(str(inv_data['total'][6]))
                            self.ao_8.setText(str(inv_data['total'][7]))
                            self.ao_9.setText('')
                            self.ao_10.setText('')
                            self.ao_11.setText('')
                            self.ao_12.setText('')
                            
                            # Terms and conditions
                            self.tnc_1.setText(tnc[0])
                            self.tnc_2.setText(tnc[1])
                            self.tnc_3.setText(tnc[2])
                            self.tnc_4.setText(tnc[3])
                            
                            # Banking deets
                            self.bd_5.setText(banking_db[0])
                            self.bd_6.setText(banking_db[1])
                            self.bd_7.setText(banking_db[2])
                            self.bd_8.setText(banking_db[3])
                            
                            # Totals
                            self.sub_total.setText(str(sub_total))
                            self.discount.setText(str(disc))
                            self.payment_received.setText(str(payment_received))
                            self.amount_owed.setText(str(total_due))
                            
                            # Save and print
                            printer = QPrinter()
                            printer.OutputFormat(1)            
                            printer.setOutputFileName(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf')
                            
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end()
                            
                            printer.OutputFormat(0)
                            painter = QPainter()
                            painter.begin(printer)
                            self.render(painter)
                            painter.end() 
                            
                            close_print = sg.popup_ok(f'Invoice {inv_num} - saved succefully as: \n {clients_db[values["CS1"]][-1]}_INV-{inv_num}_{file_date}.pdf',
                                    title='Invoice Saved', icon=pps_icon)
                            
                            if close_print == 'OK':
                                self.close()      
                            
                    if __name__ == '__main__':
                        
                        app = QApplication(sys.argv)
                        print_window = Invoice()
                        app.exec_()

            save_inv_data = open(client_dir + '\\' + f'{clients_db[values["CS1"]][-1]}.dat', 'wb')
            pickle.dump(inv_data, save_inv_data)
            save_inv_data.close()
            
            invoice_number['current'] = (inv_num +1)
            
            save_inv_num = open(f'{dll_dir}inumdb.dll','wb')  
            pickle.dump(invoice_number, save_inv_num)
            save_inv_num.close()
            
            invoice_history['client'].append(clients_db[values['CS1']][-1])
            invoice_history['inv num'].append(inv_num)
            invoice_history['date'].append(inv_date)
            
            save_inv_hist = open(f'{dll_dir}invhis.dll','wb')
            pickle.dump(invoice_history,save_inv_hist)
            save_inv_hist.close()
            
            window.close()
            new_invoice()

welcome_menu()