import customtkinter as CTK
import requests
import HomeTab
import SettingsTab
import ContactsTab
import TemplatesTab

AUTHENTICATION = False

class MyFrame(CTK.CTkScrollableFrame):
    def __init__(self, master, app_reference, **kwargs):
        super().__init__(master, **kwargs)

        self.app_reference = app_reference

        self.tabview = CTK.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.tabview.add("Home")  # add tab at the end
        self.tabview.add("Settings")  # add tab at the end
        self.tabview.add("Contacts") # add contacts at the end
        self.tabview.add("Templates") # add templates at the end
        #self.tabview.add("Help")  # add tab at the end

        if AUTHENTICATION is True:
            try:
                response = requests.get('http://162.193.76.30:5000/ping')
                if response.status_code == 200:
                    print("Server is running:", response.json())
                else:
                    print("Server is down, status code:", response.status_code)
            except requests.exceptions.RequestException as e:
                print("Error contacting server:", e)
                self.authorization_failed_labe = CTK.CTkLabel(master=self.tabview.tab("Home"), text="Authorization Failed")
                self.authorization_failed_labe.pack(padx=20, pady=10)

                self.access_denied_label = CTK.CTkLabel(master=self.tabview.tab("Home"), text="Access Denied..")
                self.access_denied_label.pack(padx=20, pady=10)
                return

        self.home_tab = HomeTab.HomeTab(master = self)
        self.settings_tab = SettingsTab.SettingsTab(master = self)
        self.contacts_tab = ContactsTab.ContactsTab(master = self)
        self.contacts_tab.pack(fill="both", expand=True)
        self.templates_tab = TemplatesTab.TemplatesTab(master = self)
        #self.help_tab = HelpTab.HelpTab(master = self)

        # Monitor tab changes via the tabview's 'set' method
        self.tabview.configure(command=self.tab_changed)

        self.app_reference.parent.geometry("200x300+50+50")

    def tab_changed(self):
        self.app_reference.update_window_size(self.tabview.get())




class MainApplication(CTK.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        CTK.CTkFrame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        parent.title("Botinator 6.0")
        parent.minsize(300, 100)  # width, height
        parent.geometry("250x300")
        parent.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.main_fram = MyFrame(master=self, app_reference=self, width=200, height=300, corner_radius=0, fg_color="transparent")
        self.main_fram.pack(fill="both", expand=True)

    def update_window_size(self, selected_tab):
        if selected_tab == "Contacts":
            self.parent.geometry("675x500")
        elif selected_tab == "Templates":
            self.parent.geometry("500x500")
        else: 
            self.parent.geometry("30x300") 


