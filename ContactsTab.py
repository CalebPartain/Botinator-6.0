import customtkinter as CTK
import Contacts
import os

# Define DB path.
BASE_PATH = os.path.join(os.getenv('APPDATA'), 'EmailBot')
os.makedirs(BASE_PATH, exist_ok=True) 
DB_PATH = os.path.join(BASE_PATH,'SQLiteDatabase.db')

class ContactsTab(CTK.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = master
        self.master = master.tabview.tab("Contacts")

        #Read contacts from database
        self.contacts_db = Contacts.Contacts(DB_PATH)

        # List to store contact entries
        self.contacts_list = []
        self.delete_list = []

        # Create buttons
        self.add_row_button = CTK.CTkButton(master=self.master, text="Add Contact", command=self.add_row_button_event)
        self.add_row_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.save_button = CTK.CTkButton(master=self.master, text="Save", command=self.save_button_event)
        self.save_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.search_entry = CTK.CTkEntry(master=self.master, placeholder_text="Search by Name")
        self.search_entry.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.search_entry.bind("<KeyRelease>", self.search_button_event)

        # Table to display contacts
        self.contacts_table = CTK.CTkFrame(master=self.master)
        self.contacts_table.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.headers = ["Name", "Email"]
        self.name_entries = []
        self.email_entries = []
        self.delete_buttons = []

        # Add table headers
        for idx, header in enumerate(self.headers):
            header_label = CTK.CTkLabel(master=self.contacts_table, text=header)
            header_label.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")

        self.load_contacts()


    def load_contacts(self):

        # Iterate over all name, email entries and delete buttons
        for name_entry, email_entry, delete_button in zip(self.name_entries, self.email_entries, self.delete_buttons):
            if name_entry is not None:
                name_entry.grid_forget()
            if email_entry is not None:
                email_entry.grid_forget()
            if delete_button is not None:
                delete_button.grid_forget()

        # Clear the lists
        self.name_entries.clear()
        self.email_entries.clear()
        self.delete_buttons.clear()

        self.contacts_list = self.contacts_db.get_contacts()
   
        for contact in self.contacts_list:
            # Adding new row for name, email inputs, and a delete button
            row = len(self.name_entries) + 1

            name_entry = CTK.CTkEntry(master=self.contacts_table, placeholder_text=contact[0])
            name_entry.grid(row=row, column=0, padx=5, pady=5)
            self.name_entries.append(name_entry)

            email_entry = CTK.CTkEntry(master=self.contacts_table, placeholder_text=contact[1])
            email_entry.grid(row=row, column=1, padx=5, pady=5)
            self.email_entries.append(email_entry)

            delete_button = CTK.CTkButton(master=self.contacts_table, text="Delete", command=lambda r=row: self.delete_row_event(r))
            delete_button.grid(row=row, column=2, padx=5, pady=5)
            self.delete_buttons.append(delete_button)

    def add_row_button_event(self):
        # Adding new row for name, email inputs, and a delete button
        row = len(self.name_entries) + 1

        name_entry = CTK.CTkEntry(master=self.contacts_table, placeholder_text="Enter name")
        name_entry.grid(row=row, column=0, padx=5, pady=5)
        self.name_entries.append(name_entry)

        email_entry = CTK.CTkEntry(master=self.contacts_table, placeholder_text="Enter email")
        email_entry.grid(row=row, column=1, padx=5, pady=5)
        self.email_entries.append(email_entry)

        delete_button = CTK.CTkButton(master=self.contacts_table, text="Delete", command=lambda r=row: self.delete_row_event(r))
        delete_button.grid(row=row, column=2, padx=5, pady=5)
        self.delete_buttons.append(delete_button)

        self.contacts_list.append([name_entry.get(), email_entry.get()])

    def delete_row_event(self, row):
        self.delete_list.append(self.contacts_list[row - 1])

        # Delete the corresponding row entries
        self.name_entries[row - 1].grid_forget()
        self.email_entries[row - 1].grid_forget()
        self.delete_buttons[row - 1].grid_forget()

        # Clear the entries to maintain indexing consistency
        self.name_entries[row - 1] = None
        self.email_entries[row - 1] = None
        self.delete_buttons[row - 1] = None

    def save_button_event(self):
        for contact in self.delete_list:
            self.contacts_db.delete_contact(contact[0], contact[1])

        self.delete_list = []

        for name_entry, email_entry in zip(self.name_entries, self.email_entries):
            if name_entry is not None and email_entry is not None :
                name = name_entry.get()
                email = email_entry.get()


                #If the field hasn't changed
                if name == '':
                    name = self.contacts_list[self.name_entries.index(name_entry)][0]
                if email == '':
                    email = self.contacts_list[self.email_entries.index(email_entry)][1]

                #If the field is still placeholder text
                if name == "Enter name" or email == "Enter email":
                    continue

                self.contacts_db.add_contact(name, email)

        self.load_contacts()

    def search_button_event(self, event=None):
        search_term = self.search_entry.get().lower()
        if search_term == '': search_term = "!!!!"


        for name_entry in self.name_entries:
            if name_entry is not None:
                name = name_entry.get().lower()
                if name == "":
                    name = self.contacts_list[self.name_entries.index(name_entry)][0].lower()
                print(name, search_term)
                if search_term in name:
                    name_entry.configure(fg_color="green")  # Highlight the name field if match is found
                else:
                    name_entry.configure(fg_color="#383838")  # Remove highlight if no match
