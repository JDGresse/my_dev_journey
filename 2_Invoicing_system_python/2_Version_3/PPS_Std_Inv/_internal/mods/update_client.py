# Libraries to import
import os
import pickle
import PySimpleGUI as sg
import re
import sys

from email_validator import EmailNotValidError, validate_email


## Edit Client Menu
def update_client(
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
    clients_db,
    dll_dir,
    parent_dir,
):
    # List to capture Client details
    new_client_db = {}
    client_list = []

    for key in clients_db.keys():
        client_list.append(key)

    sg.theme(theme)

    # Client details text boxes
    col_1 = [
        [sg.T("Client Name:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Identity number:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Mobile number:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Email address:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Address:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Suburb:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("City\\ Town:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Postal Code:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Emergeny Contact:", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Name:", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Contact number:", font=(main_font, tf_size), p=(p_std))],
    ]

    # Client details input boxes
    col_2 = [
        [
            sg.Combo(
                values=client_list,
                enable_events=True,
                k="CLIENTS",
                font=(main_font, tf_size),
                s=19,
                p=(p_std),
            )
        ],
        [sg.I(k=2, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=3, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=4, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=5, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=6, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=7, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=8, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=9, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.T("", font=(main_font, tf_size), p=(p_std))],
        [sg.I(k=10, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=11, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
    ]

    # Medical Aid text boxes
    col_3 = [
        [sg.T("Medical Aid:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Medical Aid number:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Principal Memeber Details", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Principal Member:", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Identity number:", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Address:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   Suburb:", font=(main_font, tf_size), p=(p_std))],
        [sg.T(" ->   City\\ Town:", font=(main_font, tf_size), p=(p_std))],
        [
            sg.T(
                " ->   Postal code:",
                text_color="white",
                font=(main_font, tf_size),
                p=(p_std),
            )
        ],
    ]

    # Medical Aid input boxes
    col_4 = [
        [sg.I(k=12, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=13, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [
            sg.Combo(
                values=("Yes", "No"),
                enable_events=True,
                k="PRINCE",
                font=(main_font, tf_size),
                s=5,
                p=(p_std),
            )
        ],
        [sg.I(k=14, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=15, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=16, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=17, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=18, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=19, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
        [sg.I(k=20, do_not_clear=True, font=(main_font, tf_size), s=i_size, p=(p_std))],
    ]

    layout = [
        [
            sg.T(
                "Please select and update Client details:",
                font=(main_font, hf_size),
                s=35,
                p=10,
            )
        ],
        [
            sg.Column(col_1, element_justification="l"),
            sg.Column(col_2, element_justification="l"),
            sg.Column(col_3, element_justification="l"),
            sg.Column(col_4, element_justification="l"),
        ],
        [
            sg.B(
                "Update Client",
                font=(main_font, tf_size),
                border_width="5px",
                s=b_size,
                p=(p_std),
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

    # Create the Window
    window = sg.Window("Client menu", layout, icon=pps_icon, element_justification="c")

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            # Saving client_db
            if new_client_db == []:
                window.close()
                sys.exit()
            else:
                save_file = open(f"{dll_dir}ci.dll", "wb")
                pickle.dump(clients_db, save_file)
                save_file.close()

                window.close()
                sys.exit()

        # Back
        if event in "Back":
            # Saving client_db
            if new_client_db == []:
                window.close()
                next_menu = 2
                return next_menu
            else:
                save_file = open(f"{dll_dir}ci.dll", "wb")
                pickle.dump(clients_db, save_file)
                save_file.close()

                window.close()
                next_menu = 2
                return next_menu

        # Select Client
        if event in "CLIENTS":
            cs = values["CLIENTS"]

            for i in range(0, 19):
                window[i + 2].update(clients_db[cs][i])

        # Update Client
        if event in "Update Client":
            counter = 20

            while counter != 0:
                # Name
                if (
                    values["CLIENTS"] == ""
                    or re.search("(\\d)", values["CLIENTS"]) is not None
                ):
                    sg.popup_ok(
                        "Please enter a valid Client Name (letters only please):",
                        title="Invalid Client Name",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][0] = values["CLIENTS"]
                    counter -= 1

                # ID Num
                if (
                    re.match("(\\d{13})", values[2]) is None
                    and re.match("\\d{6} \\d{4} \\d{3}", values[2]) is None
                    and re.match("\\d{2}\\D\\d{2}\\D\\d{2}", values[2]) is None
                    and re.match("\\d{2}\\D\\d{2}\\D\\d{4}", values[2]) is None
                    and re.match("\\d{2}\\D\\d{3}\\D\\d{2}", values[2]) is None
                    and re.match("\\d{2}\\D\\d{3}\\D\\d{4}", values[2]) is None
                ):
                    sg.popup_ok(
                        "Please enter a valid ID number \n Valid formats: \n\t XXXXXX XXXX XXX, \n\t XXXXXXXXXXXXX \n\t dd/mm/YY \n\t dd/mm/YYYY \n\t dd/mmm/YY \n\t dd/mmm/YYYY:",
                        title="Invalid ID Number",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][1] = values[2]
                    counter -= 1

                # Contact Number
                if (
                    re.match("(\\d{10})", values[3]) is None
                    and re.match("\\W\\d{3}\\W \\d{3} \\d{4}", values[3]) is None
                    and re.match("\\d{3} \\d{3} \\d{4}", values[3]) is None
                ):
                    sg.popup_ok(
                        "Please enter a valid Contact Number: \nAccepted formats: \n\t 000 000 0000, \n\t (000) 000 0000, \n\t0000000000",
                        title="Invalid Contact Number",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][2] = values[3]
                    counter -= 1

                # Email:
                try:
                    validate_email(values[4])
                    clients_db[cs][3] = values[4]
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
                if values[5] == "":
                    sg.popup_ok(
                        "Please enter a valid Address:",
                        title="Invalid Address",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][4] = values[5]
                    clients_db[cs][5] = values[6]
                    clients_db[cs][6] = values[7]
                    clients_db[cs][7] = values[8]
                    counter = counter - 4

                # Postal Code
                if values[9] == "" or re.match("\\d{4}", values[9]) is None:
                    sg.popup_ok(
                        "Please enter a valid Postal Code:",
                        title="Invalid Postal Code",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][8] = values[9]
                    counter -= 1

                # Emergency Contact
                if values[10] == "" or re.search("(\\d)", values[10]) is not None:
                    sg.popup_ok(
                        "Please enter a valid Emergency Contact Name (letters only please):",
                        title="Invalid Emergency Contact Name",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][9] = values[10]
                    counter -= 1

                # Emergency Contact Number
                if (
                    re.match("(\\d{10})", values[11]) is None
                    and re.match("\\W\\d{3}\\W \\d{3} \\d{4}", values[11]) is None
                    and re.match("\\d{3} \\d{3} \\d{4}", values[11]) is None
                ):
                    sg.popup_ok(
                        "Please enter a valid Contact Number: \nAccepted formats: \n\t(000) 000 0000, \n\t000 000 0000, \n\t 0000000000",
                        title="Invalid Phone Number",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    break

                else:
                    clients_db[cs][10] = values[11]
                    counter -= 1

                for i in range(12, 21):
                    clients_db[cs][i - 1] = values[i]
                    counter -= 1

                if clients_db[cs][0] == cs:  # Name not changed
                    # Saving client_db
                    save_file = open(f"{dll_dir}ci.dll", "wb")
                    pickle.dump(clients_db, save_file)
                    save_file.close()

                elif clients_db[cs][0] != cs:  # Name changed
                    new_cs = clients_db[cs][0]
                    old_client_dir = parent_dir + "\\Client Invoices\\" + cs
                    new_client_dir = parent_dir + "\\Client Invoices\\" + new_cs

                    # Rename folder to new cs
                    try:
                        # Rename Client Folder
                        os.rename(old_client_dir, new_client_dir)

                    except FileExistsError:
                        pass
                        # Client Folder already exists

                    # Saving client_db
                    save_file = open(f"{dll_dir}ci.dll", "wb")
                    pickle.dump(clients_db, save_file)
                    save_file.close()

                # Client added notification
                more_clients = sg.popup_yes_no(
                    "Client updated successfully! \nWould you like to update another Client?",
                    title="Client Added ",
                    font=("Calibri", 20),
                    icon=pps_icon,
                )

                if more_clients == "Yes":
                    window.close()
                    update_client()

                elif more_clients == "No":
                    window.close()
                    next_menu = 2
                    return next_menu
