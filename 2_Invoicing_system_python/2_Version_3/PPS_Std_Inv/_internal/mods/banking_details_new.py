import PySimpleGUI as sg
import pickle
import re
import sys


def banking_details_new(
    main_font,
    hf_size,
    tf_size,
    p_std,
    b_size,
    pps_icon,
    theme,
    i_size,
    bank_codes,
    banks,
    banking_db,
    dll_dir,
):
    selected = True

    sg.theme(theme)

    banks = []

    for bank in bank_codes.keys():
        banks.append(bank)

    col_1 = [
        [sg.T("Account Name:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Bank:", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Branch Code", font=(main_font, tf_size), p=(p_std))],
        [sg.T("Account Number:", font=(main_font, tf_size), p=(p_std))],
    ]

    col_2 = [
        [
            sg.I(
                k=1,
                do_not_clear=selected,
                font=(main_font, tf_size),
                s=i_size,
                p=(p_std),
            )
        ],
        [
            sg.Combo(
                values=banks,
                enable_events=True,
                k="COMBO",
                font=(main_font, tf_size),
                s=i_size,
                p=(p_std),
            )
        ],
        [
            sg.T(
                "Universal branch code:",
                k="U_CODE",
                font=(main_font, tf_size),
                p=(p_std),
            )
        ],
        [
            sg.I(
                k=4,
                do_not_clear=selected,
                font=(main_font, tf_size),
                s=i_size,
                p=(p_std),
            )
        ],
    ]

    layout = [
        [
            sg.T(
                "Please update any Banking Details that have changed:",
                font=(main_font, hf_size),
                s=35,
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
    ]

    # Create the Window
    window = sg.Window(
        "Banking Details Menu:",
        layout,
        icon=pps_icon,
        element_justification="c",
        finalize=True,
    )

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            # Clear inputs
            selected = False

            # Save banking_db
            if banking_db == []:
                window.close()
                sys.exit()
            else:
                save_file = open(f"{dll_dir}practice.dll", "wb")
                pickle.dump(banking_db, save_file)
                save_file.close()
                window.close()
                sys.exit()

        # Update universal bank codes based on bank selection
        if event in "COMBO":
            window["U_CODE"].Update(bank_codes[values["COMBO"]])
            u_code = bank_codes[values["COMBO"]]

        # Update
        if event in "Update":
            if values[1] == "":
                sg.popup_ok(
                    "Please enter a valid Account Name:",
                    title="Invalid Account Name",
                    font=("Calibri", 20),
                    icon=pps_icon,
                )

            else:
                banking_db[0] = values[1]
                banking_db[1] = values["COMBO"]
                banking_db[2] = u_code

                if re.match("^(\\d{7,11})$", values[4]) is None or values[4] == "":
                    sg.popup_ok(
                        "Please enter a valid Account Number:",
                        title="Invalid Account Number",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )

                else:
                    banking_db[3] = values[4]

                    # Clear inputs
                    selected = False

                    # Save banking_db
                    save_file = open(f"{dll_dir}banking.dll", "wb")
                    pickle.dump(banking_db, save_file)
                    save_file.close()

                    window.close()
                    next_menu = 0
                    return next_menu

        # Back to Main Menu
        if event in "Back":
            # Save banking_db
            save_file = open(f"{dll_dir}banking.dll", "wb")
            pickle.dump(banking_db, save_file)
            save_file.close()

            window.close()
            next_menu = 0
            return next_menu
