# Libraries to import
import sys

import PySimpleGUI as sg


def invoice_menu(
    theme,
    main_font,
    hf_size,
    btf_size,
    b_size,
    p_std,
    ebf_size,
    eb_size,
    p_ext,
    pps_icon,
    parent_dir,
):
    sg.theme(theme)

    # Initial folder directory
    inv_dir = parent_dir + "\\Client Invoices\\"

    layout = [
        [
            sg.T(
                "Do you want to create a New Invoice, Update an existing Invoice, or recreate a revious Client Invoice?",
                font=(main_font, hf_size),
                s=(33, 3),
                justification="centre",
                p=15,
            )
        ],
        [
            sg.B(
                "New Invoice",
                font=(main_font, btf_size),
                border_width="5px",
                s=(b_size + 5),
                p=p_std,
            )
        ],
        [
            sg.B(
                "Recreate Invoice",
                font=(main_font, btf_size),
                border_width="5px",
                s=(b_size + 5),
                p=p_std,
            )
        ],
        # [
        #    sg.B(
        #        "Update Invoice",
        #        font=(main_font, btf_size),
        #        border_width="5px",
        #        s=(b_size + 5),
        #        p=p_std,
        #    )
        # ],
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
    window = sg.Window("Invoice menu", layout, icon=pps_icon, element_justification="c")

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            sys.exit()

        # Back
        if event in "Back":
            window.close()
            next_menu = 0
            return next_menu

        # Create new invoice
        if event in "New Invoice":
            window.close()
            next_menu = 9
            return next_menu

        # Load Edit invoice
        if event in "Recreate Invoice":
            window.close()
            next_menu = 10
            return next_menu

        # Load update invoice
        if event in "Update Invoice":
            window.close()
            next_menu = 11
            return next_menu
