import customtkinter as CTK
import os
import Settings
from CTkMessagebox import CTkMessagebox

# Define DB path.
BASE_PATH = os.path.join(os.getenv('APPDATA'), 'EmailBot')
os.makedirs(BASE_PATH, exist_ok=True) 
DB_PATH = os.path.join(BASE_PATH,'SQLiteDatabase.db')


class SettingsTab(CTK.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #Read settings from database
        self.settings = Settings.Settings(DB_PATH)
        self.username = self.settings.get_setting('username') or ''
        self.password = self.settings.get_setting('password') or ''
        self.avg_mph = self.settings.get_setting('avg_mph') or '50'
        self.email_option = CTK.StringVar(value=self.settings.get_setting('email_option') or 'Online')
        self.custom_image_checkbox_val = CTK.StringVar(value=self.settings.get_setting('custom_image_checkbox_val') or 'off')
        self.sort_tracking_val = CTK.StringVar(value=self.settings.get_setting('sort_tracking_val') or 'on')
        self.master = master.tabview.tab('Settings')

        #Samsara Username
        self.username_label = CTK.CTkLabel(master=self.master, text="Samsara Username")
        self.username_label.pack(padx=20, pady=1)
        self.username_entry = CTK.CTkEntry(master=self.master, placeholder_text=self.username)
        self.username_entry.pack(padx=20, pady=1)

        #Samsara Password
        self.password_label = CTK.CTkLabel(master=self.master, text="Samsara Password")
        self.password_label.pack(padx=20, pady=1)
        self.password_entry = CTK.CTkEntry(master=self.master, placeholder_text=('*'*len(self.password)))
        self.password_entry.pack(padx=20, pady=1)

        #AVG MPH
        self.average_mph_label = CTK.CTkLabel(master=self.master, text="Average MPH")
        self.average_mph_label.pack(padx=20, pady=1)
        self.average_mph_entry = CTK.CTkEntry(master=self.master, placeholder_text=str(self.avg_mph))
        self.average_mph_entry.pack(padx=20, pady=1)

        #Email option
        self.email_combobox_label = CTK.CTkLabel(master=self.master, text="Email Version")
        self.email_combobox_label.pack(padx=10, pady=1)
        self.email_template_combobox = CTK.CTkComboBox(master=self.master,
                                            values=["Offline", "Online"],
                                            variable=self.email_option)
        self.email_template_combobox.pack(padx=20, pady=5)

        #Custom Images 
        self.custom_image_checkbox = CTK.CTkCheckBox(master=self.master, text="Custom Images", command=self.custom_image_checkbox_event,
                                     variable=self.custom_image_checkbox_val, onvalue="on", offvalue="off")
        self.custom_image_checkbox.pack(padx=20, pady=5)

        #Sort Tracking
        self.sort_tracking_checkbox = CTK.CTkCheckBox(master=self.master, text="Sort Tracking",
                                     variable=self.sort_tracking_val, onvalue="on", offvalue="off")
        self.sort_tracking_checkbox.pack(padx=20, pady=5)

        #Save Settings Button
        self.save_settings_button = CTK.CTkButton(master=self.master, text="Save", command=self.save_settings)
        self.save_settings_button.pack(padx=20, pady=10)

    def custom_image_checkbox_event(self):
        if self.custom_image_checkbox_val.get() == 'on':
            os.startfile(BASE_PATH)

    def save_settings(self):
        #Custom Images
        if self.custom_image_checkbox_val.get() == 'on':
            if not os.path.exists(os.path.join(BASE_PATH,'list.PNG')) or not os.path.exists(os.path.join(BASE_PATH,'movement.PNG')):
                CTkMessagebox(title="ERROR", message="No images found in directory. Please insert 'movement.PNG' and 'list.PNG' files and try again.",
                  icon="cancel", option_1="Ugh Fine I guess...")
                os.startfile(BASE_PATH)
                return
        self.settings.save_setting('custom_image_checkbox_val', self.custom_image_checkbox_val.get())

        #Username
        if self.username_entry.get() != "":
            self.username = self.username_entry.get()
            self.settings.save_setting('username', self.username)

        #Password
        if self.password_entry.get() != "":
            self.password = self.password_entry.get()
            self.settings.save_setting('password', self.password)

        #Average MPH
        if self.average_mph_entry.get() != "":
            self.avg_mph = self.average_mph_entry.get()
            self.settings.save_setting('avg_mph', self.avg_mph)

        #Email option
        self.settings.save_setting('email_option', self.email_option.get())

        #Sort tracking
        self.settings.save_setting('sort_tracking_val', self.sort_tracking_val.get())
        
        
