# Imported libraries
import pickle
import PySimpleGUI as sg
from datetime import date, timedelta

from mods.save_the_date import std


def check_date(v, dll_dir, dat_dir):
    if v == 0:
        # Capture date
        std(dat_dir)

    else:
        open_date = open(f"{dat_dir}std.dat", "rb")
        sub_date = pickle.load(open_date)

        # Check date
        check_date = date.today()
        difference = sub_date - check_date

        # Check if subscription is still valid or has expired
        if check_date == sub_date:
            sg.popup_ok(
                "Subscription has ended",
                "Your subscription has expired. To continue using PPStartUp Invoicing system, please renew your subscription.\nFor more information visit www.ppstartup.co.za or email info@ppstartup.co.za.\n Thank you.",
            )
            exit(code=2)  # Subscription expired

        elif difference < timedelta(days=30):
            sg.popup_ok(
                "Subscription ends in less than 30 days",
                "Your subscription expires in less than 30 days. To continue using PPStartUp Invoicing system, please renew your subscription.\nFor more information visit www.ppstartup.co.za or email info@ppstartup.co.za.\n Thank you.",
            )

        return v
