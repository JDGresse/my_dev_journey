# Libraries imported
import PySimpleGUI as sg
import pickle


def reg_deets(theme, pps_icon, main_font, hf_size, p_std, b_size, tf_size, dll_dir):
    sg.theme(theme)

    reg_col1 = [
        [sg.T("1. Practice Name", font=(main_font, hf_size))],
        [sg.T("2. Practitioner Name and Surname", font=(main_font, hf_size))],
        [
            sg.T(
                "3. Highest Qualification and Tertiary Institution",
                font=(main_font, hf_size),
            )
        ],
        [sg.T("4. BHF Practice Number", font=(main_font, hf_size))],
        [sg.T("5. HPCSA registration number", font=(main_font, hf_size))],
    ]

    reg_col2 = [
        [sg.I(k="PP", do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [sg.I(k="PSY", do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [
            sg.I(
                k="QUALI", do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std)
            )
        ],
        [sg.I(k="BHF", do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std))],
        [
            sg.I(
                k="HPCSA", do_not_clear=True, font=(main_font, tf_size), s=35, p=(p_std)
            )
        ],
    ]

    layout = [
        [
            sg.Column(reg_col1, element_justification="l"),
            sg.Column(reg_col2, element_justification="l"),
        ],
        [
            sg.Push(),
            sg.B(
                "Save",
                font=(main_font, tf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            ),
            sg.Push(),
        ],
    ]

    window = sg.Window("Registration Details:", layout, icon=pps_icon)

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        # Save
        if event == "Save":
            practice = str(values["PP"])
            practice = practice.split(" ", -1)

            practitioner = values["PSY"].split()
            practitioner = practitioner[0]

            reg_details = [
                str(values["PP"]),  # Practice name
                str(values["PSY"]),  # Practitioner name
                str(values["QUALI"]),  # Highest quali and Uni
                str(values["BHF"]),  # BHF
                str(values["HPCSA"]),  # HPCSA
            ]

            reg_save = open(f"{dll_dir}registry.dll", "wb")
            pickle.dump(reg_details, reg_save)
            reg_save.close()

            window.close()
            break
