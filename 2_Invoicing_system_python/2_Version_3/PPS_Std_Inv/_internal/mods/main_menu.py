# Libraries to import
import pickle
import PySimpleGUI as sg
import sys


def main_menu(
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
    dll_dir,
    media_dir,
):
    # Load registry details
    p_load = open(f"{dll_dir}registry.dll", "rb")
    loaded_p = pickle.load(p_load)
    practitioner = str(loaded_p[1])
    practitioner_name = list(practitioner.split(" ", -1))
    psychologist = practitioner_name[0]

    sg.theme(theme)  # Add a little color to your windows
    # All the stuff inside your window. This is the PSG magic code compactor...

    layout = [
        [
            sg.T(
                f"Welcome {psychologist}, what would you like to do today?",
                font=(main_font, hf_size),
                s=(25, 2),
                justification="centre",
            ),
            sg.Image(f"{media_dir}logo.png"),
        ],
        [
            sg.B(
                "Invoices",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Add or Update a Client",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Add ICD10Code",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Update Practice Details",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [
            sg.B(
                "Update Banking Details",
                font=(main_font, btf_size),
                border_width="5px",
                s=b_size,
                p=p_std,
            )
        ],
        [sg.Exit(font=(main_font, ebf_size), size=eb_size, p=p_ext)],
    ]

    # Create the Window
    window = sg.Window(
        f"Welcome to PPStartUp Invoicing System {practitioner}",
        layout,
        element_justification="c",
        icon=pps_icon,
    )

    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            window.close()
            sys.exit()

        # Open Invoice menu
        if event in "Invoices":
            window.close()
            next_menu = 1
            return next_menu

        # Open Client menu
        if event in "Add or Update a Client":
            window.close()
            next_menu = 2
            return next_menu

        # Open ICD10 menu
        if event in "Add ICD10Code":
            window.close()
            next_menu = 3
            return next_menu

        # Open Practice details menu menu
        if event in "Update Practice Details":
            window.close()
            next_menu = 4
            return next_menu

        # Open Banking details menu
        if event in "Update Banking Details":
            window.close()
            next_menu = 5
            return next_menu
