# Libraries to import
import sys

from datetime import date
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSizeF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PyQt5.uic import loadUi

# Variables
selected_list: list


def print_client_list(
    clients_db,
    inv_dir,
    ui_dir,
    registry,
    practice_db,
) -> any:
    class Print_Client_Form(QDialog):
        def __init__(self):
            super(Print_Client_Form, self).__init__()
            loadUi(f"{ui_dir}print_contact_form.ui", self)

            # Define Widgets lists
            self.client_widgets = [
                self.client_01,
                self.client_02,
                self.client_03,
                self.client_04,
                self.client_05,
                self.client_06,
                self.client_07,
                self.client_08,
                self.client_09,
                self.client_10,
                self.client_11,
                self.client_12,
                self.client_13,
                self.client_14,
                self.client_15,
                self.client_16,
                self.client_17,
                self.client_18,
                self.client_19,
                self.client_20,
                self.client_21,
                self.client_22,
                self.client_23,
                self.client_24,
                self.client_25,
            ]
            self.number_widgets = [
                self.number_01,
                self.number_02,
                self.number_03,
                self.number_04,
                self.number_05,
                self.number_06,
                self.number_07,
                self.number_08,
                self.number_09,
                self.number_10,
                self.number_11,
                self.number_12,
                self.number_13,
                self.number_14,
                self.number_15,
                self.number_16,
                self.number_17,
                self.number_18,
                self.number_19,
                self.number_20,
                self.number_21,
                self.number_22,
                self.number_23,
                self.number_24,
                self.number_25,
            ]
            self.email_widgets = [
                self.email_01,
                self.email_02,
                self.email_03,
                self.email_04,
                self.email_05,
                self.email_06,
                self.email_07,
                self.email_08,
                self.email_09,
                self.email_10,
                self.email_11,
                self.email_12,
                self.email_13,
                self.email_14,
                self.email_15,
                self.email_16,
                self.email_17,
                self.email_18,
                self.email_19,
                self.email_20,
                self.email_21,
                self.email_22,
                self.email_23,
                self.email_24,
                self.email_25,
            ]

    class Print_Client_List(QWidget):
        def __init__(self):
            super(Print_Client_List, self).__init__()
            loadUi(f"{ui_dir}print_client_select.ui", self)

            # Create client list
            client_list = list(clients_db.keys())

            self.client_list.addItems(client_list)
            self.client_list.sortItems(0)

            # Selecting a client
            self.client_list.itemSelectionChanged.connect(self.count_list)

            self.print_selection_button.clicked.connect(self.print_selection)

            self.print_all_button.clicked.connect(self.print_all)

            self.back_button.clicked.connect(self.back)

            self.exit_button.clicked.connect(self.exit_program)

        def count_list(self):
            client_count = len(self.client_list.selectedItems())

            self.client_count.setText(str(client_count))

        def print_selection(self):
            # List of selected Clients
            selected_clients = self.client_list.selectedItems()
            selected_list = ["" * i for i in range(len(selected_clients))]

            for i in range(len(selected_clients)):
                selected_list[i] = selected_clients[i].text()
                count = len(selected_list)

            # Create Print list
            print_list: dict = {"client": [], "number": [], "email": []}

            for i in range(0, count):
                for key in clients_db.keys():
                    if selected_list[i] == key:
                        print_list["client"].append(str(key))
                        print_list["number"].append(clients_db[key][1])
                        print_list["email"].append(clients_db[key][2])

            # Create Print form
            print_form = Print_Client_Form()

            # Populate data
            print_form.practice_name.setText(registry[0])

            # Practice Address
            print_form.l1.setText(practice_db[2])
            print_form.l2.setText(practice_db[3])
            print_form.l3.setText(practice_db[4])
            print_form.l4.setText(practice_db[5])
            print_form.l5.setText(practice_db[6])

            # Practice contacts
            print_form.l6.setText(practice_db[0])
            print_form.l7.setText(practice_db[1])
            print_form.l8.setText(practice_db[7])

            # registration details:
            print_form.psyc.setText(registry[1])
            print_form.quali.setText(registry[2])
            print_form.bhf_num.setText(registry[3])
            print_form.hpcsa_num.setText(registry[4])

            # Populate selected Client data
            for i in range(0, count):
                print_form.client_widgets[i + 1].setText(f"{print_list['client'][i]}")
                print_form.number_widgets[i + 1].setText(f"{print_list['number'][i]}")
                print_form.email_widgets[i + 1].setText(f"{print_list['email'][i]}")

            # Save and Print Form
            ## Print
            printer = QPrinter()
            printer.setPaperSize(QSizeF(210, 297), QPrinter.Millimeter)
            painter = QPainter()
            painter.begin(printer)
            print_form.render(painter)
            painter.end()

            today = date.today()
            today_str = today.strftime("%w %b %y")

            # Save
            printer.OutputFormat(1)
            printer.setOutputFileName(inv_dir + f"{today_str}.dat")
            painter = QPainter()
            painter.begin(printer)
            print_form.render(painter)
            painter.end()

            QMessageBox.information(
                self,
                f"Client List saved:",
                f"Selected Client list successfully saved as: \n{today_str}.dat inside the Client Invoices folder.",
            )

            self.close()
            self.next_up = 2

        def print_all(self):
            # List of All Clients
            client_list = list(clients_db.keys())
            count = len(client_list)

            # Create Print list
            # Create Print list
            print_list: dict = {"client": [], "number": [], "email": []}

            for i in range(0, count):
                for key in clients_db.keys():
                    print_list["client"].append(str(key))
                    print_list["number"].append(clients_db[key][1])
                    print_list["email"].append(clients_db[key][2])

            # Create Print form
            print_form = Print_Client_Form()

            # Populate data
            print_form.practice_name.setText(registry[0])

            # Practice Address
            print_form.l1.setText(practice_db[2])
            print_form.l2.setText(practice_db[3])
            print_form.l3.setText(practice_db[4])
            print_form.l4.setText(practice_db[5])
            print_form.l5.setText(practice_db[6])

            # Practice contacts
            print_form.l6.setText(practice_db[0])
            print_form.l7.setText(practice_db[1])
            print_form.l8.setText(practice_db[7])

            # registration details:
            print_form.psyc.setText(registry[1])
            print_form.quali.setText(registry[2])
            print_form.bhf_num.setText(registry[3])
            print_form.hpcsa_num.setText(registry[4])

            # Populate selected Client data
            # Populate selected Client data
            for i in range(0, count):
                print_form.client_widgets[i + 1].setText(f"{print_list['client'][i]}")
                print_form.number_widgets[i + 1].setText(f"{print_list['number'][i]}")
                print_form.email_widgets[i + 1].setText(f"{print_list['email'][i]}")

            # Save and Print Form
            ## Print
            printer = QPrinter()
            printer.setPaperSize(QSizeF(210, 297), QPrinter.Millimeter)
            painter = QPainter()
            painter.begin(printer)
            print_form.render(painter)
            painter.end()

            today = date.today()
            today_str = today.strftime("%w %b %y")

            # Save
            printer.OutputFormat(1)
            printer.setOutputFileName(inv_dir + f"{today_str}.dat")
            painter = QPainter()
            painter.begin(printer)
            print_form.render(painter)
            painter.end()

            QMessageBox.information(
                self,
                f"Client List saved:",
                f"Selected Client list successfully saved as: \n{today_str}.dat inside the Client Invoices folder.",
            )

            self.close()
            self.next_up = 2

        def back(self):
            self.close()
            self.next_up = 2

        def exit_program(self):
            sys.exit()

    print_client_app = QApplication(sys.argv)
    print_client_window = Print_Client_List()
    print_client_window.show()
    print_client_app.exec_()
    return print_client_window.next_up
