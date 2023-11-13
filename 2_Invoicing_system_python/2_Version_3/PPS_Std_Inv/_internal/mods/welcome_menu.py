# Imported libraries
import pickle
import PySimpleGUI as sg


# Variabes
next_menu: int = 0


# Welcome menu
def welcome_menu(theme, pps_icon, main_font, hf_size, btf_size, p_std, b_size, dll_dir):
    sg.theme(theme)

    layout = [
        [
            sg.Push(),
            sg.T(
                "Welcome to Private Practice StartUp Invoicing System.",
                font=(main_font, hf_size),
            ),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.T(
                "To start, we will capture all of the essential information,",
                font=(main_font, hf_size),
            ),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.T(
                "    so please get the following information ready before proceeding:    ",
                font=(main_font, hf_size),
            ),
            sg.Push(),
        ],
        [sg.T("", font=(main_font, hf_size))],
        [sg.T("     1. Practice Name", font=(main_font, hf_size))],
        [sg.T("     2. Practitioner Name and Surname", font=(main_font, hf_size))],
        [
            sg.T(
                "     3. Highest Qualification and Tertiary Institution",
                font=(main_font, hf_size),
            )
        ],
        [sg.T("     4. BHF Practice Number", font=(main_font, hf_size))],
        [sg.T("     5. HPCSA registration number", font=(main_font, hf_size))],
        [sg.T("", font=(main_font, hf_size))],
        [
            sg.Push(),
            sg.T(
                'Once you have all of this information ready, click "Proceed".',
                font=(main_font, hf_size),
            ),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.B(
                "Proceed",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            ),
            sg.Push(),
        ],
    ]

    window = sg.Window("Welcome to PPStartUp Invoicing System", layout, icon=pps_icon)

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        # Exit
        if event == sg.WIN_CLOSED:
            reset_v = 0
            new_v = open(f"{dll_dir}first.dll", "wb")
            pickle.dump(reset_v, new_v)
            new_v.close()

            window.close()
            exit()

        # Proceed
        if event in "Proceed":
            window.close()
            next_menu = 12
            return next_menu
