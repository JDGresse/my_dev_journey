import PySimpleGUI as sg
import hashlib
import pickle

def set_apw(main_font, hf_size, tf_size, p_std, b_size, pps_icon, dat_dir, dll_dir, theme):
    
    sg.theme(theme)
    
    apw_col1 = [
        [sg.T('Enter password:', font=(main_font, hf_size))],
        [sg.T('Confirm password:', font=(main_font, hf_size))],
    ]

    apw_col2 = [
        [sg.I(k='-APW-', password_char='*', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k='-CONFIRM-', password_char='*', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
    ]

    layout = [
        [sg.T('Please set the Administrator password below:', font=(main_font, hf_size))],
        [sg.Column(apw_col1, element_justification='l' ), sg.Column(apw_col2, element_justification='l')],
        [sg.Push(), sg.B('Set password', font=(main_font,tf_size), border_width='5px', s=b_size, p=p_std), sg.Push()],
        ]
        
    window = sg.Window(f'Please set Administrator password', layout, icon=pps_icon)

    # Event Loop to process "events"
    while True:    
        
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            window.close()
            v = 1
            
            save_v = open(f'{dll_dir}v.dll','wb')
            pickle.dump(v, save_v)
            save_v.close()
            
            exit()
            
        if event in 'Set password':
            
            if values['-APW-'] == '' or values['-CONFIRM-'] == '':
                sg.popup_ok('Please enter and confirm the password.')
                continue
                
            elif values['-APW-'] != values['-CONFIRM-']:
                sg.popup_ok('Password does not match, please retype carefully.')
                continue
                
            elif values['-APW-'] == values['-CONFIRM-']:
                sg.popup_ok('Password saved successfully.')
                
                apw = hashlib.sha256(values['-APW-'].encode()).hexdigest()
                
                save_apw = open(f'{dat_dir}apw.dat','wb')
                pickle.dump(apw, save_apw)
                save_apw.close()
                
                window.close()    