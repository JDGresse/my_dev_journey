# Libraries to load
import os
import pickle
from posixpath import splitext
from re import split
import sys
import PySimpleGUI as sg

from datetime import date
from PyQt5.QtCore import QDate, QSizeF
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.uic import loadUi

from lib.ui import pps_media_rc

# Define variables
invoice_data = ["" * i for i in range(0, 7)]
sd_data = ["" * i for i in range(0, 12)]
service_data = ["" * i for i in range(0, 12)]
pc_data = ["" * i for i in range(0, 12)]
icd_data = ["" * i for i in range(0, 12)]
fees_data = [0.00 * i for i in range(0, 12)]
disc_data = [0.00 * i for i in range(0, 12)]
pr_data = [0.00 * i for i in range(0, 12)]
total_data = [0.00 * i for i in range(0, 12)]
sub_total: float = 0.00
discount: float = 0.00
payments_received: float = 0.00
amount_due: float = 0.00
str_inv_date: str = None
inv_number_dict = {"start": 1000, "current": 1000}
invoice_history = {}
client = ["" * i for i in range(20)]
date_changed: bool = False
##


def invoice_recreate(
    icd_codes,
    icd_descriptions,
    ui_dir,
    dll_dir,
    pps_icon,
    clients_db,
    parent_dir,
) -> any:
    counter = 0

    class Full_Invoice(QWidget):
        def __init__(self):
            super(Full_Invoice, self).__init__()
            loadUi(f"{ui_dir}full_invoice.ui", self)

            # Define fees_widgets, disc_widgets and tot_widgets lists
            self.fees_widgets = [
                self.fees_1,
                self.fees_2,
                self.fees_3,
                self.fees_4,
                self.fees_5,
                self.fees_6,
                self.fees_7,
                self.fees_8,
                self.fees_9,
                self.fees_10,
                self.fees_11,
                self.fees_12,
            ]
            self.disc_widgets = [
                self.disc_1,
                self.disc_2,
                self.disc_3,
                self.disc_4,
                self.disc_5,
                self.disc_6,
                self.disc_7,
                self.disc_8,
                self.disc_9,
                self.disc_10,
                self.disc_11,
                self.disc_12,
            ]
            self.tot_widgets = [
                self.ao_1,
                self.ao_2,
                self.ao_3,
                self.ao_4,
                self.ao_5,
                self.ao_6,
                self.ao_7,
                self.ao_8,
                self.ao_9,
                self.ao_10,
                self.ao_11,
                self.ao_12,
            ]
            self.client_widgets = [
                self.c1,
                self.c2,
                self.c3,
                self.c4,
                self.c5,
                self.c6,
                self.c7,
                self.c8,
                self.c9,
                self.c10,
                self.c11,
            ]
            self.s_date_widgets = [
                self.sd_1,
                self.sd_2,
                self.sd_3,
                self.sd_4,
                self.sd_5,
                self.sd_6,
                self.sd_7,
                self.sd_8,
                self.sd_9,
                self.sd_10,
                self.sd_11,
                self.sd_12,
            ]
            self.services_widgets = [
                self.services_1,
                self.services_2,
                self.services_3,
                self.services_4,
                self.services_5,
                self.services_6,
                self.services_7,
                self.services_8,
                self.services_9,
                self.services_10,
                self.services_11,
                self.services_12,
            ]
            self.pc_widgets = [
                self.pc_1,
                self.pc_2,
                self.pc_3,
                self.pc_4,
                self.pc_5,
                self.pc_6,
                self.pc_7,
                self.pc_8,
                self.pc_9,
                self.pc_10,
                self.pc_11,
                self.pc_12,
            ]
            self.icd_widgets = [
                self.icd_1,
                self.icd_2,
                self.icd_3,
                self.icd_4,
                self.icd_5,
                self.icd_6,
                self.icd_7,
                self.icd_8,
                self.icd_9,
                self.icd_10,
                self.icd_11,
                self.icd_12,
            ]
            self.fees_widgets = [
                self.fees_1,
                self.fees_2,
                self.fees_3,
                self.fees_4,
                self.fees_5,
                self.fees_6,
                self.fees_7,
                self.fees_8,
                self.fees_9,
                self.fees_10,
                self.fees_11,
                self.fees_12,
            ]

    class Display_Invoice(QWidget):
        def __init__(self, next_up=1):
            self.next_up = next_up

            super(Display_Invoice, self).__init__()
            loadUi(f"{ui_dir}display_invoice.ui", self)

            self.disc_widgets = [
                self.disc1,
                self.disc2,
                self.disc3,
                self.disc4,
                self.disc5,
                self.disc6,
                self.disc7,
                self.disc8,
                self.disc9,
                self.disc10,
                self.disc11,
                self.disc12,
            ]  # Add all QLineEdit objects here
            self.tot_widgets = [
                self.tot_1,
                self.tot_2,
                self.tot_3,
                self.tot_4,
                self.tot_5,
                self.tot_6,
                self.tot_7,
                self.tot_8,
                self.tot_9,
                self.tot_10,
                self.tot_11,
                self.tot_12,
            ]  # Add all QLabel objects here
            self.scb_widgets = [
                self.s1cb,
                self.s2cb,
                self.s3cb,
                self.s4cb,
                self.s5cb,
                self.s6cb,
                self.s7cb,
                self.s8cb,
                self.s9cb,
                self.s10cb,
                self.s11cb,
                self.s12cb,
            ]
            self.icd_widgets = [
                self.icd1,
                self.icd2,
                self.icd3,
                self.icd4,
                self.icd5,
                self.icd6,
                self.icd7,
                self.icd8,
                self.icd9,
                self.icd10,
                self.icd11,
                self.icd12,
            ]
            self.fees_widgets = [
                self.fees1,
                self.fees2,
                self.fees3,
                self.fees4,
                self.fees5,
                self.fees6,
                self.fees7,
                self.fees8,
                self.fees9,
                self.fees10,
                self.fees11,
                self.fees12,
            ]
            self.pc_widgets = [
                self.pc1,
                self.pc2,
                self.pc3,
                self.pc4,
                self.pc5,
                self.pc6,
                self.pc7,
                self.pc8,
                self.pc9,
                self.pc10,
                self.pc11,
                self.pc12,
            ]

            file_dialog = QFileDialog()
            # Set the starting directory
            file_dialog.setDirectory(parent_dir + "\\Client Invoices\\")
            # Set the file dialog box title
            file_dialog.setWindowTitle("Load File")
            # Set the file dialog box filter
            file_dialog.setNameFilter("*.dat")
            # Show the file dialog box
            file_dialog.exec_()

            # Get the selected file name
            try:
                file_name = file_dialog.selectedFiles()[0]

                # Open the file
                load_file = open(file_name, "rb")
                save_data = pickle.load(load_file)

            except IndexError:
                save_data = {
                    "invoice data": [],
                    "sd_data": [],
                    "service_data": [],
                    "pc_data": [],
                    "icd_data": [],
                    "fees_data": [],
                    "disc_data": [],
                    "pr_data": [],
                    "total_data": [],
                    "sub_total": [],
                    "discount": [],
                    "payments_received": [],
                    "amount_due": [],
                }

            # Load inv_num
            ## inv_num
            try:
                i_load_file = open(f"{dll_dir}inumdb.dll", "rb")
                inv_number_dict = pickle.load(i_load_file)
                inv_num = inv_number_dict["current"]

            except FileNotFoundError:
                self.next_up = 1
                inv_num = "INV #"

            # Load Inv num
            self.inv_num.setText(str(inv_num))

            # Set inv_date and SD1 combobox to today's date
            inv_date = date.today()
            now = QDate.currentDate()
            first_day = now.addDays(-now.day() + 1)

            ## Inv date
            self.dateEdit.setDate(inv_date)

            self.cbox_select.addItem(save_data["invoice data"][2])
            self.cbox_select.setCurrentIndex(0)

            ## Selected Client
            self.cbox_select.activated.connect(self.client)

            ## Session dates
            self.sd1.setDate(first_day)
            self.sd2.setDate(first_day)
            self.sd3.setDate(first_day)
            self.sd4.setDate(first_day)
            self.sd5.setDate(first_day)
            self.sd6.setDate(first_day)
            self.sd7.setDate(first_day)
            self.sd8.setDate(first_day)
            self.sd9.setDate(first_day)
            self.sd10.setDate(first_day)
            self.sd11.setDate(first_day)
            self.sd12.setDate(first_day)

            # Set Services
            services = [
                "Payment Received",
                "Appointment not kept",
                "Assessment",
                "Consultation",
                "Psychotherapy",
                "Training",
                "Supervision",
                "Group Psychotherapy",
                "Group Consultation",
            ]

            self.s1cb.addItems(services)
            self.s2cb.addItems(services)
            self.s3cb.addItems(services)
            self.s4cb.addItems(services)
            self.s5cb.addItems(services)
            self.s6cb.addItems(services)
            self.s7cb.addItems(services)
            self.s8cb.addItems(services)
            self.s9cb.addItems(services)
            self.s10cb.addItems(services)
            self.s11cb.addItems(services)
            self.s12cb.addItems(services)

            # Set ICD codes
            icd_display = ["" * i for i in range(0, len(icd_codes))]

            for i in range(0, len(icd_codes)):
                icd_display[i] = icd_codes[i] + " - " + icd_descriptions[i]

            for i in range(12):
                if getattr(self, f"icd{i + 1}").currentText() == "":
                    getattr(self, f"icd{i + 1}").addItems(icd_display)
                    icd_position = getattr(self, f"icd{i + 1}")
                    icd_position.view().setMinimumWidth(
                        icd_position.view().sizeHintForColumn(0)
                    )

            # Set Pro Codes
            self.s1cb.currentIndexChanged.connect(lambda: self.pro_codes(1))
            self.s2cb.currentIndexChanged.connect(lambda: self.pro_codes(2))
            self.s3cb.currentIndexChanged.connect(lambda: self.pro_codes(3))
            self.s4cb.currentIndexChanged.connect(lambda: self.pro_codes(4))
            self.s5cb.currentIndexChanged.connect(lambda: self.pro_codes(5))
            self.s6cb.currentIndexChanged.connect(lambda: self.pro_codes(6))
            self.s7cb.currentIndexChanged.connect(lambda: self.pro_codes(7))
            self.s8cb.currentIndexChanged.connect(lambda: self.pro_codes(8))
            self.s9cb.currentIndexChanged.connect(lambda: self.pro_codes(9))
            self.s10cb.currentIndexChanged.connect(lambda: self.pro_codes(10))
            self.s11cb.currentIndexChanged.connect(lambda: self.pro_codes(11))
            self.s12cb.currentIndexChanged.connect(lambda: self.pro_codes(12))

            # Capture events and Data
            self.dateEdit.editingFinished.connect(self.invoice_date)

            invoice_data[1] = str(inv_num)

            ## Session dates
            self.sd1.dateChanged.connect(lambda date: self.sd_data(0))
            self.sd2.dateChanged.connect(lambda date: self.sd_data(1))
            self.sd5.dateChanged.connect(lambda date: self.sd_data(4))
            self.sd3.dateChanged.connect(lambda date: self.sd_data(2))
            self.sd4.dateChanged.connect(lambda date: self.sd_data(3))
            self.sd6.dateChanged.connect(lambda date: self.sd_data(5))
            self.sd7.dateChanged.connect(lambda date: self.sd_data(6))
            self.sd8.dateChanged.connect(lambda date: self.sd_data(7))
            self.sd9.dateChanged.connect(lambda date: self.sd_data(8))
            self.sd10.dateChanged.connect(lambda date: self.sd_data(9))
            self.sd11.dateChanged.connect(lambda date: self.sd_data(10))
            self.sd12.dateChanged.connect(lambda date: self.sd_data(11))

            ## Services
            self.s1cb.currentIndexChanged.connect(lambda: self.service_data(0))
            self.s2cb.currentIndexChanged.connect(lambda: self.service_data(1))
            self.s3cb.currentIndexChanged.connect(lambda: self.service_data(2))
            self.s4cb.currentIndexChanged.connect(lambda: self.service_data(3))
            self.s5cb.currentIndexChanged.connect(lambda: self.service_data(4))
            self.s6cb.currentIndexChanged.connect(lambda: self.service_data(5))
            self.s7cb.currentIndexChanged.connect(lambda: self.service_data(6))
            self.s8cb.currentIndexChanged.connect(lambda: self.service_data(7))
            self.s9cb.currentIndexChanged.connect(lambda: self.service_data(8))
            self.s10cb.currentIndexChanged.connect(lambda: self.service_data(9))
            self.s11cb.currentIndexChanged.connect(lambda: self.service_data(10))
            self.s12cb.currentIndexChanged.connect(lambda: self.service_data(11))

            ## Pro Codes
            self.pc1.currentIndexChanged.connect(lambda: self.pro_data(0))
            self.pc2.currentIndexChanged.connect(lambda: self.pro_data(1))
            self.pc3.currentIndexChanged.connect(lambda: self.pro_data(2))
            self.pc4.currentIndexChanged.connect(lambda: self.pro_data(3))
            self.pc5.currentIndexChanged.connect(lambda: self.pro_data(4))
            self.pc6.currentIndexChanged.connect(lambda: self.pro_data(5))
            self.pc7.currentIndexChanged.connect(lambda: self.pro_data(6))
            self.pc8.currentIndexChanged.connect(lambda: self.pro_data(7))
            self.pc9.currentIndexChanged.connect(lambda: self.pro_data(8))
            self.pc10.currentIndexChanged.connect(lambda: self.pro_data(9))
            self.pc11.currentIndexChanged.connect(lambda: self.pro_data(10))
            self.pc12.currentIndexChanged.connect(lambda: self.pro_data(11))

            ## ICD
            self.icd1.currentIndexChanged.connect(lambda: self.icd_data(0))
            self.icd2.currentIndexChanged.connect(lambda: self.icd_data(1))
            self.icd3.currentIndexChanged.connect(lambda: self.icd_data(2))
            self.icd4.currentIndexChanged.connect(lambda: self.icd_data(3))
            self.icd5.currentIndexChanged.connect(lambda: self.icd_data(4))
            self.icd6.currentIndexChanged.connect(lambda: self.icd_data(5))
            self.icd7.currentIndexChanged.connect(lambda: self.icd_data(6))
            self.icd8.currentIndexChanged.connect(lambda: self.icd_data(7))
            self.icd9.currentIndexChanged.connect(lambda: self.icd_data(8))
            self.icd10.currentIndexChanged.connect(lambda: self.icd_data(9))
            self.icd11.currentIndexChanged.connect(lambda: self.icd_data(10))
            self.icd12.currentIndexChanged.connect(lambda: self.icd_data(11))

            ## fees
            self.fees1.textEdited.connect(lambda: self.update_fee_data(0))
            self.fees2.textEdited.connect(lambda: self.update_fee_data(1))
            self.fees3.textEdited.connect(lambda: self.update_fee_data(2))
            self.fees4.textEdited.connect(lambda: self.update_fee_data(3))
            self.fees5.textEdited.connect(lambda: self.update_fee_data(4))
            self.fees6.textEdited.connect(lambda: self.update_fee_data(5))
            self.fees7.textEdited.connect(lambda: self.update_fee_data(6))
            self.fees8.textEdited.connect(lambda: self.update_fee_data(7))
            self.fees9.textEdited.connect(lambda: self.update_fee_data(8))
            self.fees10.textEdited.connect(lambda: self.update_fee_data(9))
            self.fees11.textEdited.connect(lambda: self.update_fee_data(10))
            self.fees12.textEdited.connect(lambda: self.update_fee_data(11))

            ## disc
            self.disc1.textEdited.connect(lambda: self.update_disc_data(0))
            self.disc2.textEdited.connect(lambda: self.update_disc_data(1))
            self.disc3.textEdited.connect(lambda: self.update_disc_data(2))
            self.disc4.textEdited.connect(lambda: self.update_disc_data(3))
            self.disc5.textEdited.connect(lambda: self.update_disc_data(4))
            self.disc6.textEdited.connect(lambda: self.update_disc_data(5))
            self.disc7.textEdited.connect(lambda: self.update_disc_data(6))
            self.disc8.textEdited.connect(lambda: self.update_disc_data(7))
            self.disc9.textEdited.connect(lambda: self.update_disc_data(8))
            self.disc10.textEdited.connect(lambda: self.update_disc_data(9))
            self.disc11.textEdited.connect(lambda: self.update_disc_data(10))
            self.disc12.textEdited.connect(lambda: self.update_disc_data(11))

            ## Set up initial display
            for i in range(12):
                service_data[i] = save_data["service_data"][i]
                pc_data[i] = save_data["pc_data"][i]
                icd_data[i] = save_data["icd_data"][i]
                fees_data[i] = save_data["fees_data"][i]
                disc_data[i] = save_data["disc_data"][i]
                total_data[i] = save_data["total_data"][i]
                pr_data[i] = save_data["pr_data"][i]

            invoice_data[2] = save_data["invoice data"][2]  # client
            invoice_data[3] = save_data["invoice data"][3]  # sub_total
            invoice_data[4] = save_data["invoice data"][4]  # discount
            invoice_data[5] = save_data["invoice data"][5]  # payments_received
            invoice_data[6] = save_data["invoice data"][6]  # amount_due

            # Set ICD index
            icd_index = [20 for i in range(12)]
            for i in range(12):
                for d in range(0, len(icd_codes)):
                    if icd_data[i] == icd_codes[d]:
                        icd_index[i] = d

            # Display saved values
            for i in range(12):
                # Set serivce
                if service_data[i] != "":
                    index = getattr(self, f"s{i + 1}cb").findText(service_data[i])
                    getattr(self, f"s{i + 1}cb").setCurrentIndex(index)

                    if getattr(self, f"s{i + 1}cb").currentText() == "Payment Received":
                        getattr(self, f"fees{i + 1}").setText(f"R ({pr_data[i]})")
                        getattr(self, f"tot_{i + 1}").setText(
                            f"R ({str(total_data[i])})"
                        )
                    else:
                        getattr(self, f"fees{i + 1}").setText(f"R {fees_data[i]}")
                        getattr(self, f"tot_{i + 1}").setText(f"R {str(total_data[i])}")

                    # Set Pro Codes
                    index = getattr(self, f"pc{i + 1}").findText(pc_data[i])
                    getattr(self, f"pc{i + 1}").setCurrentIndex(index)

                    # Set ICD
                    if icd_index[i] != 20:
                        getattr(self, f"icd{i + 1}").setCurrentIndex(icd_index[i])

                    # Set Disc
                    if disc_data[i] != "":
                        getattr(self, f"disc{i + 1}").setText(f"R {disc_data[i]}")

            self.sub_total.setText(f"R {str(invoice_data[3])}")
            self.discount.setText(f"R {str(invoice_data[4])}")
            self.payment_received.setText(f"R {str(invoice_data[5])}")
            self.amount_owed.setText(f"R {str(invoice_data[6])}")

            # Save
            self.save_button.clicked.connect(self.save_1)

            # Save and Print
            self.save_print_button.clicked.connect(self.save_2)

            # T's and C's
            self.tnc_button.clicked.connect(self.tnc)

            # Back
            self.back_button.clicked.connect(self.back)

            # Exit
            self.exit_button.clicked.connect(self.finished)

        # Capture invoice date
        def invoice_date(self):
            date = self.dateEdit.date()
            invoice_data[0] = date.toString("dd MMM yyyy")

        # Capture selected Client
        def client(self):
            invoice_data[2] = self.cbox_select.currentText()

        # Capture Session dates
        def sd_data(self, index):
            try:
                date = getattr(self, f"sd{index + 1}").date()
                sd_data[index] = date.toString("dd MMM yy")  # Convert QDate to string
            except IndexError:
                print(f"Error: Index {index} is out of range for sd_data.")

        # Services
        def service_data(self, index):
            try:
                service_data[index] = getattr(self, f"s{index + 1}cb").currentText()
            except IndexError:
                print(f"Error: Index {index} is out of range for service_data.")

        # Pro Codes
        def pro_codes(self, index):
            pc = getattr(self, "pc{}".format(index))
            current_text = getattr(self, "s{}cb".format(index)).currentText()
            pc.clear()

            if current_text == "Payment Received":
                pc.addItem("0")
            elif current_text == "Appointment not kept":
                pc.addItem("86007")
            elif (
                current_text == "Assessment"
                or current_text == "Consultation"
                or current_text == "Psychotherapy"
                or current_text == "Training"
                or current_text == "Supervision"
            ):
                pc.addItems(
                    [
                        "86200",
                        "86201",
                        "86202",
                        "86203",
                        "86204",
                        "86205",
                        "86206",
                        "86207",
                        "86208",
                        "86209",
                        "86210",
                        "86211",
                        "86290",
                    ]
                )
            elif (
                current_text == "Group Psychotherapy"
                or current_text == "Group Consultation"
            ):
                pc.addItems(
                    [
                        "86300",
                        "86301",
                        "86302",
                        "86303",
                        "86304",
                        "86305",
                        "86306",
                        "86307",
                        "86308",
                        "86309",
                        "86310",
                        "86311",
                        "86390",
                    ]
                )

        ## Pro codes
        def pro_data(self, index):
            try:
                pc_data[index] = getattr(self, f"pc{index + 1}").currentText()
            except IndexError:
                print(f"Error: Index {index} is out of range for pc_data.")

        ## ICD codes
        def icd_data(self, index):
            try:
                icd_data[index] = icd_codes[index]
            except IndexError:
                print(f"Error: Index {index} is out of range for icd_data.")

        ## Fees
        def update_fee_data(self, index):
            fee_input = getattr(self, f"fees{index + 1}").text()

            if not fee_input:
                # Handle the case when the input is empty
                return

            try:
                fee_value = float(fee_input)
            except ValueError:
                return

            if service_data[index] != "Payment Received":
                """Calculate the total for services rendered."""

                fees_data[index] = fee_input
                disc_input = disc_data[index]

                if not disc_input:
                    disc_value = 0.00
                else:
                    try:
                        disc_value = float(disc_input)
                    except ValueError:
                        disc_value = 0.00

                total_data[index] = fee_value - disc_value

                fees_total = sum(
                    float(fees_data[i]) for i in range(index + 1) if fees_data[i] != ""
                )
                disc_total = sum(
                    float(disc_data[i]) for i in range(index + 1) if disc_data[i] != ""
                )
                pr_total = sum(
                    float(pr_data[i]) for i in range(index + 1) if pr_data[i] != ""
                )

                tot = fees_total - disc_total - pr_total

                invoice_data[3] = fees_total
                invoice_data[4] = disc_total
                invoice_data[5] = pr_total
                invoice_data[6] = tot

                getattr(self, f"tot_{index + 1}").setText(f"R{total_data[index]}")
                self.payment_received.setText(f"R ({pr_total})")
                self.sub_total.setText(f"R {fees_total}")
                self.amount_owed.setText(f"R {tot}")

            else:
                """Calculate the total when there is a payment received."""

                pr_data[index] = fee_input
                total_data[index] = fee_value

                fees_total = sum(
                    float(fees_data[i]) for i in range(index + 1) if fees_data[i] != ""
                )
                disc_total = sum(
                    float(disc_data[i]) for i in range(index + 1) if disc_data[i] != ""
                )
                pr_total = sum(
                    float(pr_data[i]) for i in range(index + 1) if pr_data[i] != ""
                )

                tot = fees_total - disc_total - pr_total

                invoice_data[3] = fees_total
                invoice_data[4] = disc_total
                invoice_data[5] = pr_total
                invoice_data[6] = tot

                getattr(self, f"tot_{index + 1}").setText(f"R ({total_data[index]})")
                self.payment_received.setText(f"R ({pr_total})")
                self.sub_total.setText(f"R {fees_total}")
                self.amount_owed.setText(f"R {tot}")

        ## Disc
        def update_disc_data(self, index):
            discount_input = getattr(self, f"disc{index + 1}").text()
            disc_data[index] = discount_input

            try:
                disc_value = float(discount_input)
            except ValueError:
                disc_value = 0.00

            total_data[index] = float(fees_data[index]) - disc_value

            fees_total = sum(
                float(fees_data[i]) for i in range(index + 1) if fees_data[i] != ""
            )
            disc_total = sum(
                float(disc_data[i]) for i in range(index + 1) if disc_data[i] != ""
            )
            pr_total = sum(
                float(pr_data[i]) for i in range(index + 1) if pr_data[i] != ""
            )

            tot = fees_total - disc_total - pr_total

            invoice_data[3] = fees_total
            invoice_data[4] = disc_total
            invoice_data[5] = pr_total
            invoice_data[6] = tot

            getattr(self, f"tot_{index + 1}").setText(f"R {total_data[index]}")

            self.discount.setText(f"R ({disc_total})")
            self.payment_received.setText(f"R ({pr_total})")
            self.sub_total.setText(f"R {fees_total}")
            self.amount_owed.setText(f"R {tot}")

        # Save
        def save_1(self):
            if invoice_data[0] == "":
                sg.popup_notify(
                    title="Please select an Invoice Date!", display_duration_in_ms=4000
                )
            else:
                # Load dbs
                open_pdb = open(f"{dll_dir}practice.dll", "rb")
                open_regdb = open(f"{dll_dir}registry.dll", "rb")
                open_tnc = open(f"{dll_dir}tnc.dll", "rb")
                open_bdb = open(f"{dll_dir}banking.dll", "rb")
                practice_db = pickle.load(open_pdb)
                registry = pickle.load(open_regdb)
                tnc_data = pickle.load(open_tnc)
                banking_db = pickle.load(open_bdb)

                open_bdb.close()
                open_pdb.close()
                open_regdb.close()
                open_tnc.close()

                # Identify client
                for key in clients_db.keys():
                    if key == invoice_data[2]:
                        for j in range(0, 20):
                            client[j] = clients_db[key][j]

                # Practice Name
                save_invoice = Full_Invoice()

                # Practice Address
                save_invoice.p1.setText(practice_db[2])
                save_invoice.p2.setText(practice_db[3])
                save_invoice.p3.setText(practice_db[4])
                save_invoice.p4.setText(practice_db[5])
                save_invoice.p5.setText(practice_db[6])

                # Practice contacts
                save_invoice.p6.setText(practice_db[0])
                save_invoice.p7.setText(practice_db[1])
                save_invoice.p8.setText(practice_db[7])

                # registration details:
                save_invoice.psyc.setText(registry[1])
                save_invoice.quali.setText(registry[2])
                save_invoice.bhf_num.setText(registry[3])
                save_invoice.hpcsa_num.setText(registry[4])

                # Inv num and date
                save_invoice.inv_num.setText(invoice_data[1])
                save_invoice.inv_date.setText(invoice_data[0])

                # Client details values['CS1']
                save_invoice.c1.setText(invoice_data[2])  # acc name
                save_invoice.c2.setText(client[0])  # id
                save_invoice.c3.setText(client[3])  # ad 1
                save_invoice.c4.setText(client[4])  # ad 2
                save_invoice.c5.setText(client[5])  # sub
                save_invoice.c6.setText(client[6])  # city
                save_invoice.c7.setText(client[7])  # postal
                save_invoice.c8.setText(client[10])  # med aid
                save_invoice.c9.setText(client[11])  # med aid num
                save_invoice.c10.setText(client[12])  # prince
                save_invoice.c11.setText(client[13])  # prince id

                # Inv data
                # SD
                for i in range(12):
                    save_invoice.s_date_widgets[i].setText(f"{sd_data[i]}")

                # Service
                for i in range(12):
                    save_invoice.services_widgets[i].setText(f"{service_data[i]}")

                # PC
                for i in range(12):
                    save_invoice.pc_widgets[i].setText(f"{pc_data[i]}")

                # ICD
                for i in range(12):
                    save_invoice.icd_widgets[i].setText(f"{icd_data[i]}")

                save_invoice.ref_email.setText(practice_db[1])

                # Fees
                for i in range(12):
                    if fees_data[i] != 0.00:
                        save_invoice.fees_widgets[i].setText(f"R {fees_data[i]}")
                    else:
                        save_invoice.fees_widgets[i].setText("")

                # Disc
                for i in range(12):
                    if disc_data[i] != 0.00:
                        save_invoice.disc_widgets[i].setText(f"R {disc_data[i]}")
                    else:
                        save_invoice.disc_widgets[i].setText("")

                # Payment received
                for i in range(12):
                    if pr_data[i] != 0.00:
                        save_invoice.fees_widgets[i].setText(f"R ({pr_data[i]})")

                    else:
                        pass

                # AO
                for i in range(12):
                    if total_data[i] != 0.00:
                        save_invoice.tot_widgets[i].setText(f"R {total_data[i]}")
                    else:
                        save_invoice.tot_widgets[i].setText("")

                # Terms and conditions
                save_invoice.tnc_1.setText(tnc_data[0])
                save_invoice.tnc_2.setText(tnc_data[1])
                save_invoice.tnc_3.setText(tnc_data[2])
                save_invoice.tnc_4.setText(tnc_data[3])

                # Banking deets
                save_invoice.bd_5.setText(banking_db[0])
                save_invoice.bd_6.setText(banking_db[1])
                save_invoice.bd_7.setText(banking_db[2])
                save_invoice.bd_8.setText(banking_db[3])

                # Totals
                save_invoice.sub_total.setText(f"R {invoice_data[3]}")
                save_invoice.discount.setText(f"R {invoice_data[4]}")
                save_invoice.payment_received.setText(f"R ({invoice_data[5]})")
                save_invoice.amount_owed.setText(f"R {invoice_data[6]}")

                ## Creating \\ Opening save folder
                inv_dir = parent_dir + "\\Client Invoices\\"
                client_dir = inv_dir + invoice_data[2]

                # Create save data dictionary
                save_data = {
                    "invoice data": invoice_data,
                    "sd_data": sd_data,
                    "service_data": service_data,
                    "pc_data": pc_data,
                    "icd_data": icd_data,
                    "fees_data": fees_data,
                    "disc_data": disc_data,
                    "pr_data": pr_data,
                    "total_data": total_data,
                    "sub_total": sub_total,
                    "discount": discount,
                    "payments_received": payments_received,
                    "amount_due": amount_due,
                }

                try:
                    # Create Client Invoices Folderd
                    os.mkdir(inv_dir)

                    try:
                        # Create Client Folder
                        os.mkdir(client_dir)

                    except FileExistsError:
                        pass
                        # Client Folder already exists

                except FileExistsError:
                    # Client Invoices Folder already exists, try creating Client Folder
                    try:
                        # Create Client Folder
                        os.mkdir(client_dir)

                    except FileExistsError:
                        pass
                        # Client Folder already exists

                # Save Dat file
                save_save_data = open(f"{client_dir}\\{invoice_data[2]}.dat", "wb")
                pickle.dump(save_data, save_save_data)
                save_save_data.close()

                # Save
                printer = QPrinter()
                printer.setPaperSize(QSizeF(210, 297), QPrinter.Millimeter)

                printer.OutputFormat(1)
                printer.setOutputFileName(
                    client_dir
                    + "\\"
                    + f"{client[-1]}_INV-{invoice_data[1]}_{invoice_data[0]}.pdf"
                )
                painter = QPainter()
                painter.begin(printer)
                save_invoice.render(painter)
                painter.end()

                QMessageBox.information(
                    self,
                    f"Invoice {invoice_data[1]} saved:",
                    f"Invoice successfully saved as: \n{client[-1]}_INV-{invoice_data[1]}_{invoice_data[0]}",
                )

                inv_num = int(invoice_data[1])
                inv_num += 1
                inv_number_dict["current"] = inv_num
                save_inv_num = open(f"{dll_dir}inumdb.dll", "wb")
                pickle.dump(inv_number_dict, save_inv_num)
                save_inv_num.close()

                self.close()
                self.next_up = 1
                return self.next_up

                # Load Invoice History
                # try:
                #    ih_load_file = open(f"{dll_dir}inv_hist.dll", "rb")
                #    invoice_history = pickle.load(ih_load_file)

                # except FileNotFoundError:
                #    invoice_history = {}
                ###

                # if inv_num == 1000:
                #    invoice_history["client"] = invoice_data[2]
                #    invoice_history["inv"] = invoice_data[1]
                #    invoice_history["date"] = invoice_data[0]

                #    save_inv_hist = open(f"{dll_dir}inv_hist.dll", "wb")
                #    pickle.dump(invoice_history, save_inv_hist)
                #    save_inv_hist.close()

                # elif inv_num >= 1001:
                #    invoice_history["client"].append(invoice_data[2])
                #    invoice_history["inv"].append(invoice_data[1])
                #    invoice_history["date"].append(invoice_data[0])

                #    save_inv_hist = open(f"{dll_dir}inv_hist.dll", "wb")
                #    pickle.dump(invoice_history, save_inv_hist)
                #    save_inv_hist.close()

        # Save and Print
        def save_2(self):
            if invoice_data[0] == "":
                sg.popup_notify(
                    title="Please select an Invoice Date!", display_duration_in_ms=4000
                )
            else:
                # Load dbs
                open_pdb = open(f"{dll_dir}practice.dll", "rb")
                open_regdb = open(f"{dll_dir}registry.dll", "rb")
                open_tnc = open(f"{dll_dir}tnc.dll", "rb")
                open_bdb = open(f"{dll_dir}banking.dll", "rb")
                practice_db = pickle.load(open_pdb)
                registry = pickle.load(open_regdb)
                tnc_data = pickle.load(open_tnc)
                banking_db = pickle.load(open_bdb)

                open_bdb.close()
                open_pdb.close()
                open_regdb.close()
                open_tnc.close()

                # Identify client
                for key in clients_db.keys():
                    if key == invoice_data[2]:
                        for j in range(0, 20):
                            client[j] = clients_db[key][j]

                # Practice Name
                save_invoice = Full_Invoice()

                # Practice Address
                save_invoice.p1.setText(practice_db[2])
                save_invoice.p2.setText(practice_db[3])
                save_invoice.p3.setText(practice_db[4])
                save_invoice.p4.setText(practice_db[5])
                save_invoice.p5.setText(practice_db[6])

                # Practice contacts
                save_invoice.p6.setText(practice_db[0])
                save_invoice.p7.setText(practice_db[1])
                save_invoice.p8.setText(practice_db[7])

                # registration details:
                save_invoice.psyc.setText(registry[1])
                save_invoice.quali.setText(registry[2])
                save_invoice.bhf_num.setText(registry[3])
                save_invoice.hpcsa_num.setText(registry[4])

                # Inv num and date
                save_invoice.inv_num.setText(invoice_data[1])
                save_invoice.inv_date.setText(invoice_data[0])

                # Client details values['CS1']
                save_invoice.c1.setText(invoice_data[2])  # acc name
                save_invoice.c2.setText(client[0])  # id
                save_invoice.c3.setText(client[3])  # ad 1
                save_invoice.c4.setText(client[4])  # ad 2
                save_invoice.c5.setText(client[5])  # sub
                save_invoice.c6.setText(client[6])  # city
                save_invoice.c7.setText(client[7])  # postal
                save_invoice.c8.setText(client[10])  # med aid
                save_invoice.c9.setText(client[11])  # med aid num
                save_invoice.c10.setText(client[12])  # prince
                save_invoice.c11.setText(client[13])  # prince id

                # Inv data
                # SD
                for i in range(12):
                    save_invoice.s_date_widgets[i].setText(f"{sd_data[i]}")

                # Service
                for i in range(12):
                    save_invoice.services_widgets[i].setText(f"{service_data[i]}")

                # PC
                for i in range(12):
                    save_invoice.pc_widgets[i].setText(f"{pc_data[i]}")

                # ICD
                for i in range(12):
                    save_invoice.icd_widgets[i].setText(f"{icd_data[i]}")

                save_invoice.ref_email.setText(practice_db[1])

                # Fees
                for i in range(12):
                    if fees_data[i] != 0.00:
                        save_invoice.fees_widgets[i].setText(f"R {fees_data[i]}")
                    else:
                        save_invoice.fees_widgets[i].setText("")

                # Disc
                for i in range(12):
                    if disc_data[i] != 0.00:
                        save_invoice.disc_widgets[i].setText(f"R {disc_data[i]}")
                    else:
                        save_invoice.disc_widgets[i].setText("")

                # Payment received
                for i in range(12):
                    if pr_data[i] != 0.00:
                        save_invoice.fees_widgets[i].setText(f"R ({pr_data[i]})")

                    else:
                        pass

                # AO
                for i in range(12):
                    if total_data[i] != 0.00:
                        save_invoice.tot_widgets[i].setText(f"R {total_data[i]}")
                    else:
                        save_invoice.tot_widgets[i].setText("")

                # Terms and conditions
                save_invoice.tnc_1.setText(tnc_data[0])
                save_invoice.tnc_2.setText(tnc_data[1])
                save_invoice.tnc_3.setText(tnc_data[2])
                save_invoice.tnc_4.setText(tnc_data[3])

                # Banking deets
                save_invoice.bd_5.setText(banking_db[0])
                save_invoice.bd_6.setText(banking_db[1])
                save_invoice.bd_7.setText(banking_db[2])
                save_invoice.bd_8.setText(banking_db[3])

                # Totals
                save_invoice.sub_total.setText(f"R {invoice_data[3]}")
                save_invoice.discount.setText(f"R {invoice_data[4]}")
                save_invoice.payment_received.setText(f"R ({invoice_data[5]})")
                save_invoice.amount_owed.setText(f"R {invoice_data[6]}")

                ## Creating \\ Opening save folder
                inv_dir = parent_dir + "\\Client Invoices\\"
                client_dir = inv_dir + invoice_data[2]

                # Create save data dictionary
                save_data = {
                    "invoice data": invoice_data,
                    "sd_data": sd_data,
                    "service_data": service_data,
                    "pc_data": pc_data,
                    "icd_data": icd_data,
                    "fees_data": fees_data,
                    "disc_data": disc_data,
                    "pr_data": pr_data,
                    "total_data": total_data,
                    "sub_total": sub_total,
                    "discount": discount,
                    "payments_received": payments_received,
                    "amount_due": amount_due,
                }

                try:
                    # Create Client Invoices Folderd
                    os.mkdir(inv_dir)

                    try:
                        # Create Client Folder
                        os.mkdir(client_dir)

                    except FileExistsError:
                        pass
                        # Client Folder already exists

                except FileExistsError:
                    # Client Invoices Folder already exists, try creating Client Folder
                    try:
                        # Create Client Folder
                        os.mkdir(client_dir)

                    except FileExistsError:
                        pass
                        # Client Folder already exists

                # Save Dat file
                save_save_data = open(f"{client_dir}\\{invoice_data[2]}.dat", "wb")
                pickle.dump(save_data, save_save_data)
                save_save_data.close()

                # Save and Print
                printer = QPrinter()
                printer.setPaperSize(QSizeF(210, 297), QPrinter.Millimeter)

                # Print
                painter = QPainter()
                painter.begin(printer)
                save_invoice.render(painter)
                painter.end()

                # Save
                printer.OutputFormat(1)
                printer.setOutputFileName(
                    client_dir
                    + "\\"
                    + f"{client[-1]}_INV-{invoice_data[1]}_{invoice_data[0]}.pdf"
                )
                painter = QPainter()
                painter.begin(printer)
                save_invoice.render(painter)
                painter.end()

                QMessageBox.information(
                    self,
                    f"Invoice {invoice_data[1]} saved:",
                    f"Invoice successfully saved as: \n{client[-1]}_INV-{invoice_data[1]}_{invoice_data[0]}",
                )

                inv_num = int(invoice_data[1])
                inv_num += 1
                inv_number_dict["current"] = inv_num
                save_inv_num = open(f"{dll_dir}inumdb.dll", "wb")
                pickle.dump(inv_number_dict, save_inv_num)
                save_inv_num.close()

                self.close()
                self.next_up = 1
                return self.next_up

                # Load Invoice History
                # try:
                #    ih_load_file = open(f"{dll_dir}inv_hist.dll", "rb")
                #    invoice_history = pickle.load(ih_load_file)

                # except FileNotFoundError:
                #    invoice_history = {}
                ###

                # if inv_num == 1000:
                #    invoice_history["client"] = invoice_data[2]
                #    invoice_history["inv"] = invoice_data[1]
                #    invoice_history["date"] = invoice_data[0]

                #    save_inv_hist = open(f"{dll_dir}inv_hist.dll", "wb")
                #    pickle.dump(invoice_history, save_inv_hist)
                #    save_inv_hist.close()

                # elif inv_num >= 1001:
                #    invoice_history["client"].append(invoice_data[2])
                #    invoice_history["inv"].append(invoice_data[1])
                #    invoice_history["date"].append(invoice_data[0])

                #    save_inv_hist = open(f"{dll_dir}inv_hist.dll", "wb")
                #    pickle.dump(invoice_history, save_inv_hist)
                #    save_inv_hist.close()

        # T's and C's
        def tnc(self):
            try:
                load_tnc = open(f"{dll_dir}tnc.dll", "rb")
                tnc = pickle.load(load_tnc)
                load_tnc.close()
            except FileNotFoundError:
                tnc = ["" * i for i in range(4)]

            layout = [
                [sg.Text("Please enter any Terms and Conditions below:")],
                [sg.Input(default_text=(f"{tnc[0]}"), key="t1")],
                [sg.Input(default_text=(f"{tnc[1]}"), key="t2")],
                [sg.Input(default_text=(f"{tnc[2]}"), key="t3")],
                [sg.Input(default_text=(f"{tnc[3]}"), key="t4")],
                [sg.Button("Save")],
                [sg.Button("Back")],
            ]

            tnc_window = sg.Window("T's and C's", layout=layout)

            while True:
                event, values = tnc_window.read()

                if event == sg.WIN_CLOSED:
                    tnc_window.close()
                    sys.exit()

                if event == "Back" or event == "Save":
                    for i in range(4):
                        if tnc[i] is not None:
                            tnc[i] = values[f"t{i + 1}"]
                        else:
                            tnc[i] = ""
                        save_tnc = open(f"{dll_dir}tnc.dll", "wb")
                        pickle.dump(tnc, save_tnc)
                        save_tnc.close()
                    tnc_window.close()
                    break

        # Back
        def back(self):
            self.close()
            self.next_up = 1
            return self.next_up

        def finished(self):
            sys.exit()

    if counter == 0:
        counter += 1
        inv_app = QApplication(sys.argv)
        invoice_window = Display_Invoice()
        invoice_window.show()
        inv_app.exec_()
        return invoice_window.next_up
    else:
        counter += 1
        new_inv_app = QApplication(sys.argv)
        new_invoice_window = Display_Invoice()
        new_invoice_window.show()
        new_inv_app.exec_()
        return new_invoice_window.next_up
