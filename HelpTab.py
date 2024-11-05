import customtkinter as CTK

class HelpTab(CTK.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master.tabview.tab('Help')

        self.help_label = CTK.CTkLabel(master=self.master, text="No:)")
        self.help_label.pack(padx=20, pady=10)