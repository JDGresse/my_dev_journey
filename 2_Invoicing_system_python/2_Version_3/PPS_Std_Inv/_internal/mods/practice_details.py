import PySimpleGUI as sg
import pickle
import re
import sys

from email_validator import EmailNotValidError, validate_email


def practice_details(
    theme,
    main_font,
    tf_size,
    p_std,
    i_size,
    hf_size,
    b_size,
    ebf_size,
    eb_size,
    p_ext,
    pps_icon,
    v,
    dll_dir,
):
    sg.theme(theme)

    col_1 = [
        [sg.T("Office Number:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Email address:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Address:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("", text_color="white", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Suburb:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("City:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Postal Code:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Website:", font=(main_font, tf_size), p=(p_std))],
    ]

    col_2 = [
        [sg.I(k=1, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=2, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=3, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=4, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=5, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=6, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=7, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=8, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
    ]

    layout = [
        [
            sg.T(
                "Please update the Practice Contact Details:",
                font=(main_font, hf_size),
                s=(35, 2),
                p=10,
            )
        ],
        [
            sg.Column(col_1, element_justification="l"),
            sg.Column(col_2, element_justification="l"),
        ],
        [
            sg.B(
                "Update",
                font=(main_font, tf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Back",
                font=(main_font, ebf_size),
                border_width="4px",
                s=eb_size,
                p=p_ext,
            ),
            sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext),
        ],
    ]

    window = sg.Window(
        "Practice Details menu:",
        layout,
        icon=pps_icon,
        element_justification="c",
        finalize=True,
    )

    try:
        pd_load = open(f"{dll_dir}practice.dll", "rb")
        practice_db = pickle.load(pd_load)

        for i in range(1, 9):
            window[i].Update(practice_db[i - 1])

    except FileNotFoundError:
        practice_db = []

    # Event Loop
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            # Save practice_db
            if practice_db == []:
                window.close()
                sys.exit()
            else:
                save_file = open(f"{dll_dir}practice.dll", "wb")
                pickle.dump(practice_db, save_file)
                save_file.close()
                break

        # Back
        if event in "Back":
            # Save practice_db
            if practice_db == []:
                window.close()
                next_menu = 0
                return next_menu
            else:
                save_file = open(f"{dll_dir}practice.dll", "wb")
                pickle.dump(practice_db, save_file)
                save_file.close()
                window.close()
                next_menu = 0
                return next_menu

        # Update
        if event in "Update":
            practice_details = []
            counter = 8

            practice_details = [i * " " for i in range(0, 8)]

            while counter != 0:
                # Check Phone number
                if (
                    re.match("(\\d{10})", values[1]) is None
                    and re.match("\\W\\d{3}\\W \\d{3} \\d{4}", values[1]) is None
                    and re.match("\\d{3} \\d{3} \\d{4}", values[1]) is None
                    and re.match("\\+(27) \\d{2} \\d{3} \\d{4}", values[1]) is None
                ):
                    sg.popup_ok(
                        "Please enter a valid Contact Number: \nAccepted formats: \n\t 000 000 0000, \n\t (000) 000 0000, \n\t 0000000000, \n\t +27 00 000 0000",
                        title="Invalid Contact Number",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    practice_details[0] = values[1]
                    counter -= 1

                # Check email
                try:
                    validate_email(values[2])

                    practice_details[1] = values[2]
                    counter -= 1

                except EmailNotValidError as e:
                    sg.popup_ok(
                        str(e),
                        title="Invalid Email",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                # Address 1
                if values[3] == "":
                    sg.popup_ok(
                        "Please enter a valid Address:",
                        title="Invalid Address",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    practice_details[2] = values[3]
                    practice_details[3] = values[4]
                    practice_details[4] = values[5]
                    practice_details[5] = values[6]
                    counter = counter - 4

                # Postal Code
                if values[7] == "" or re.match("\\d{4}", values[7]) is None:
                    sg.popup_ok(
                        "Please enter a valid Postal Code:",
                        title="Invalid Postal Code",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    practice_details[6] = values[7]
                    practice_details[7] = values[8]
                    counter = counter - 2

                # Updating pracice_db
                practice_db = practice_details

                # Saving practice_db
                save_file = open(f"{dll_dir}practice.dll", "wb")
                pickle.dump(practice_db, save_file)
                save_file.close()

                window.close()

                if v != 0:
                    next_menu = 0
                    return next_menu

                elif v == 0:
                    break
