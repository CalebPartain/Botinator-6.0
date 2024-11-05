import customtkinter as CTK
from datetime import datetime
import Movement
import threading
import TrackingWindow
import Email
import Utils

class HomeTab(CTK.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = master
        self.master = master.tabview.tab("Home")

        self.end_date = datetime.now().strftime('%m/%d/%Y 1300')
        self.email_template_option = CTK.StringVar(value="ISSUE")  # set initial value

        self.build_email = CTK.CTkButton(master=self.master, text ="Build Email", command = self.build_email_button_event)
        self.build_email.pack(padx=10, pady=10)

        self.email_template_combobox_label = CTK.CTkLabel(master=self.master, text="Email Template")
        self.email_template_combobox_label.pack(padx=10, pady=1)
        self.email_template_combobox = CTK.CTkComboBox(master=self.master,
                                            values=['ISSUE'],
                                            variable=self.email_template_option)
        self.email_template_combobox.pack(padx=20, pady=1)

        self.trackButton = CTK.CTkButton(master=self.master, text ="Track", command = self.track_button_event)
        self.trackButton.pack(padx=10, pady=15)

        self.end_date_label = CTK.CTkLabel(master=self.master, text="Tracking End Point")
        self.end_date_label.pack(padx=20, pady=1)
        self.end_date_entry = CTK.CTkEntry(master=self.master, placeholder_text=self.end_date)
        self.end_date_entry.pack(padx=20, pady=1)


    def track_button_event(self):
        if self.end_date_entry.get() == 't':
            self.end_date = Utils.time_add(datetime.now().strftime('%m/%d/%Y 1300'), 1440)
        elif self.end_date_entry.get() != '':
            self.end_date = self.end_date_entry.get()

        t1 = threading.Thread(target=TrackingWindow.TrackingWindow, args=([self]))
        t1.daemon = True
        t1.start()

    def build_email_button_event(self):
        Email.Email.create_email(self, self.email_template_option.get())

