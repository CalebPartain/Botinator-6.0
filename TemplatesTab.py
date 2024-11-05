import customtkinter as CTK
import Templates
import os

# Define DB path.
BASE_PATH = os.path.join(os.getenv('APPDATA'), 'EmailBot')
os.makedirs(BASE_PATH, exist_ok=True) 
DB_PATH = os.path.join(BASE_PATH,'SQLiteDatabase.db')

class TemplatesTab(CTK.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = master
        self.master = master.tabview.tab('Templates')
        self.templates = Templates.Templates(DB_PATH)
        self.template_names = self.templates.get_template_names()
        self.parent.home_tab.email_template_combobox.configure(values=self.template_names)
        self.template_names.append('<new>')



        #Template selection
        self.email_template_option = CTK.StringVar(value="<new>")
        self.email_template_label = CTK.CTkLabel(master=self.master, text="Template")
        self.email_template_label.pack(padx=10, pady=1)
        self.email_template_combobox = CTK.CTkComboBox(master=self.master,
                                            command=self.refresh_tab,
                                            values=self.template_names,
                                            variable=self.email_template_option)
        self.email_template_combobox.pack(padx=20, pady=5)

        #CSR 
        self.csr_checkbox_val = CTK.StringVar(value="True")
        self.csr_checkbox = CTK.CTkCheckBox(master=self.master, text="CSR", variable=self.csr_checkbox_val,
                                             onvalue="True", offvalue="False")
        self.csr_checkbox.pack(padx=20, pady=5)

        #Entered By 
        self.entered_by_checkbox_val = CTK.StringVar(value="True")
        self.entered_by_checkbox = CTK.CTkCheckBox(master=self.master, text="Entered By", variable=self.entered_by_checkbox_val,
                                             onvalue="True", offvalue="False")
        self.entered_by_checkbox.pack(padx=20, pady=5)

        #DM
        self.dm_checkbox_val = CTK.StringVar(value="True")
        self.dm_checkbox = CTK.CTkCheckBox(master=self.master, text="Driver Manager", variable=self.dm_checkbox_val,
                                             onvalue="True", offvalue="False")
        self.dm_checkbox.pack(padx=20, pady=5)

        #ISSUE 
        self.issue_label = CTK.CTkLabel(master=self.master, text="Issue")
        self.issue_label.pack(padx=20, pady=1)
        self.issue_entry = CTK.CTkEntry(master=self.master, placeholder_text='Issue')
        self.issue_entry.pack(padx=20, pady=1)

        #Added To Contacts
        self.to_contacts_label = CTK.CTkLabel(master=self.master, text='Added "To" Contacts')
        self.to_contacts_label.pack(padx=20, pady=1)
        self.to_contacts_entry = CTK.CTkEntry(master=self.master, placeholder_text='Example1@gmail.com; Emaple2@gmail.com')
        self.to_contacts_entry.pack(padx=20, pady=1)

        #CC Contacts
        self.cc_contacts_label = CTK.CTkLabel(master=self.master, text='CC Contacts')
        self.cc_contacts_label.pack(padx=20, pady=1)
        self.cc_contacts_entry = CTK.CTkEntry(master=self.master, placeholder_text='Example1@gmail.com; Emaple2@gmail.com')
        self.cc_contacts_entry.pack(padx=20, pady=1)

        #Update
        self.update_label = CTK.CTkLabel(master=self.master, text='Update')
        self.update_label.pack(padx=20, pady=1)
        self.update_entry = CTK.CTkEntry(master=self.master, placeholder_text='What the email says')
        self.update_entry.pack(padx=20, pady=1)

        #Save template Button
        self.save_template_button = CTK.CTkButton(master=self.master, text="Save", command=self.save_template)
        self.save_template_button.pack(padx=20, pady=10)

        #Delete template Button
        self.delete_template_button = CTK.CTkButton(master=self.master, text="Delete", command=self.delete_template)
        self.delete_template_button.pack(padx=20, pady=10)

    def save_template(self):
        self.templates.save_template(
            issue = self.issue_entry.get(),
            csr = self.csr_checkbox_val.get(),
            entered_by = self.entered_by_checkbox_val.get(),
            dm = self.dm_checkbox_val.get(),
            added_contacts = self.to_contacts_entry.get(),
            cc_contacts = self.cc_contacts_entry.get(),
            email = self.update_entry.get()
        )
        self.template_names = self.templates.get_template_names()
        self.parent.home_tab.email_template_combobox.configure(values=self.template_names)
        self.template_names.append('<new>')
        self.email_template_combobox.configure(values=self.template_names)
        self.email_template_combobox.set('<new>')
        self.refresh_tab()

    def delete_template(self):
        self.templates.delete_template(self.email_template_combobox.get())
        self.template_names = self.templates.get_template_names()
        self.parent.home_tab.email_template_combobox.configure(values=self.template_names)
        self.template_names.append('<new>')
        self.email_template_combobox.configure(values=self.template_names)
        self.email_template_combobox.set('<new>')
        self.refresh_tab()

    def refresh_tab(self, *args):
        if self.email_template_combobox.get() == '<new>': template=['','True','True','True','','','']
        else:template = self.templates.get_template_by_name(self.email_template_combobox.get())

        #ISSUE
        self.issue_entry.delete(0, CTK.END)  # Clear any existing text
        self.issue_entry.insert(0, template[0])

        #CSR
        if template[1] == 'True': self.csr_checkbox.select()
        else: self.csr_checkbox.deselect()

        #Entered By
        if template[2] == 'True': self.entered_by_checkbox.select()
        else: self.entered_by_checkbox.deselect()

        #DM
        if template[3] == 'True': self.dm_checkbox.select()
        else: self.dm_checkbox.deselect()

        #Added To Contacts
        self.to_contacts_entry.delete(0, CTK.END)  # Clear any existing text
        self.to_contacts_entry.insert(0, template[4])

        #CC Contacts
        self.cc_contacts_entry.delete(0, CTK.END)  # Clear any existing text
        self.cc_contacts_entry.insert(0, template[5])

        #Update
        self.update_entry.delete(0, CTK.END)  # Clear any existing text
        self.update_entry.insert(0, template[6])

