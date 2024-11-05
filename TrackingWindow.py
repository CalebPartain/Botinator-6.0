from tkinter import *
import customtkinter as CTK
import Movement
import win32api
import time

class TrackingWindow(CTK.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        CTK.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.root = CTK.CTkToplevel(self.parent)
        self.root.transient(self.parent)
        self.root.protocol('WM_DELETE_WINDOW', self.destroy())

        self.root.title("Tracking in Progress")
        self.root.geometry("300x100") 

        self.track()



    def track(self):
        INSTRUCTIONS = ''' Simply right click any oder on the specific Order 
        Planning Screen you wish to track'''
        self.label = CTK.CTkLabel(master=self.root, text = INSTRUCTIONS)
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)

        #Wait for user to right click 
        state_right = win32api.GetKeyState(0x02)
        b = state_right
        while b == state_right:
            b = win32api.GetKeyState(0x02)
            time.sleep(0.1)

        self.progressbar = CTK.CTkProgressBar(master=self.root)
        self.progressbar.set(0)
        self.progressbar.pack(padx=10, pady=10)

        response = Movement.Movement.copy_all_from_McLeod(self, self.parent.parent.settings_tab.username, self.parent.parent.settings_tab.password, self.parent.parent.settings_tab.avg_mph)

        if response == 1:
            self.label.configure(text="Tracking Complete.")

    
