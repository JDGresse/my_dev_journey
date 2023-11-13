# Libraries to import
import PySimpleGUI as sg
import sys


def client_menu(
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
):
    sg.theme(theme)

    layout = [
        [
            sg.T(
                "Do you want to add a New Client, or update an Existing Client?",
                font=(main_font, hf_size),
                s=(33, 2),
                justification="centre",
                p=15,
            )
        ],
        [
            sg.B(
                "Add a New Client",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Update an existing Client",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Print Contact List",
                font=(main_font, btf_size),
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

    # Create the Window
    window = sg.Window(
        "Client menu", layout, icon=pps_icon, element_justification="centre"
    )

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

        # Add Client
        elif event in "Add a New Client":
            window.close()
            next_menu = 6
            return next_menu

        # Update Client
        elif event in "Update an existing Client":
            window.close()
            next_menu = 7
            return next_menu

        # Print Contact List
        elif event in "Print Contact List":
            window.close()
            next_menu = 8
            return next_menu
