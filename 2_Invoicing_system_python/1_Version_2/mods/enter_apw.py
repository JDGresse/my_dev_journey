import PySimpleGUI as sg
import hashlib
import pickle

def check_apw(main_font, hf_size, tf_size, p_std, b_size, pps_icon, dat_dir, theme):
    
    sg.theme(theme)
    
    layout = [
        [sg.T('Please enter the Administrator password:', font=(main_font, hf_size))],
        [sg.I(k='-APW-', password_char='*', do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.Push(), sg.B('Proceed', font=(main_font,tf_size), border_width='5px', s=b_size, p=p_std), 
         sg.Exit(font=(main_font, tf_size), size=b_size, p=p_std), sg.Push()]
    ]
    
    window = sg.Window(f'Please Enter Administrator password to proceed', layout, icon=pps_icon)

    # Event Loop to process "events"
    while True:    
        
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            window.close()
            return 'Do not proceed'
            
        if event in 'Proceed':
            
            tries = 0
            
            load_apw = open(f'{dat_dir}apw.dat','rb')
            apw = pickle.load(load_apw)
            
            entered_apw = hashlib.sha256(values['-APW-'].encode()).hexdigest()
            
            if entered_apw == apw:
                sg.popup_ok('Password correct, thank you.')
                window.close()
            
            elif entered_apw != apw:
                
                tries += 1
                
                if tries >= 4:
                    
                    sg.popup_ok('Number of attempts exceeded, please contact Administrator to gain access.',
                                title='Number of attempts exceeded', font=('Calibri',20), icon=pps_icon)
                    
                    return 'Too many attempts'
                    window.close()
                
                else:
                    
                    sg.popup_ok('The Entered password does not match the saved password.', 
                                title='Incorrect password', font=('Calibri',20), icon=pps_icon)
                    continue  