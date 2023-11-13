# Libraries to import
import pickle
import PySimpleGUI as sg
import sys


def icd_menu(
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
    icd_codes,
    icd_descriptions,
    dll_dir,
    pro_codes,
):
    sg.theme(theme)

    selected = True

    col_1 = [
        [sg.T("ICD10 Code:", font=(main_font, tf_size), p=p_std)],
        [
            sg.I(
                k="SEARCH",
                do_not_clear=selected,
                font=(main_font, tf_size),
                s=i_size,
                p=p_std,
            )
        ],
        [sg.T("ICD10 Code:", font=(main_font, tf_size), p=((10, 10), (27, 10)))],
        [
            sg.I(
                k="NEW_CODE",
                do_not_clear=selected,
                font=(main_font, tf_size),
                s=10,
                p=p_std,
            )
        ],
    ]

    col_2 = [
        [sg.T("", text_color="white", font=(main_font, tf_size), p=(p_std))],
        [sg.B("Search for Code", font=(main_font, tf_size), border_width="5px", s=13)],
        [sg.T("Description:", font=(main_font, tf_size), p=(p_std))],
        [
            sg.I(
                k="NEW_DESCRIPTION",
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
                "Please enter the ICD10 code you would like to search for, or add:",
                font=(main_font, hf_size),
                s=(28, 2),
                p=((30, 15), (15, 15)),
            )
        ],
        [
            sg.Column(col_1, element_justification="l"),
            sg.Column(col_2, element_justification="l"),
        ],
        [
            sg.B(
                "Add New Code",
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
            sg.Exit(font=(main_font, ebf_size), s=eb_size, p=p_ext),
        ],
    ]

    window = sg.Window(
        "ICD10 Codes menu:", layout, icon=pps_icon, element_justification="c"
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            sys.exit()

        # Search
        if event in "Search for Code":
            counter = 0

            search_code = values["SEARCH"]

            for i in range(0, len(icd_codes)):
                while search_code == icd_codes[i]:
                    sg.popup_ok(
                        "This ICD10 Code is already in the database.",
                        title="ICD10 Code found:",
                        font=("Calibri", 20),
                        icon=pps_icon,
                    )
                    counter = 1
                    break

            if counter == 0:
                not_found = sg.popup_yes_no(
                    "This ICD10 Code is NOT in the database. \nWould you like to add it now?",
                    title="Add ICD10 Code?",
                    font=("Calibri", 20),
                    icon=pps_icon,
                )

                if not_found == "Yes":
                    window["NEW_CODE"].Update(values["SEARCH"])

                elif not_found == "No":
                    window.close()
                    next_menu = 2
                    return next_menu

        # Add codes
        if event in "Add New Code":
            # if values["NEW_CODE"] != 0 and str(values["NEW_DESCRIPTION"]).isalpha():
            icd_codes.append(values["NEW_CODE"])
            icd_descriptions.append(values["NEW_DESCRIPTION"])

            selected = False

            # Code added notification
            more_codes = sg.popup_yes_no(
                "ICD10 Code added successfully! \nWould you like to add another code?",
                title="ICD10 Code Added",
                font=("Calibri", 20),
                icon=pps_icon,
            )

            if more_codes == "No":
                # Save codes and descriptions
                c_save_file = open(f"{dll_dir}icdcodes.dll", "wb")
                pickle.dump(icd_codes, c_save_file)
                c_save_file.close()

                d_save_file = open(f"{dll_dir}icddescript.dll", "wb")
                pickle.dump(icd_descriptions, d_save_file)
                d_save_file.close()

                window.close()
                next_menu = 2
                return next_menu

            # else:
            #    sg.popup_ok(
            #        "Please add a valid description - it may #only contain letters and grammatical symbols.",
            #        title="Invalid Description",
            #        font=("Calibri", 20),
            #        icon=pps_icon,
            #   )

        # Back
        elif event in "Back":
            window.close()
            next_menu = 0
            return next_menu
