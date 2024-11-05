import os
import customtkinter as CTK
import MainWindow

#py -m PyInstaller -F -w --icon="icon.ico" --add-data="*.PNG;." --noupx --noconsole "Botinator 6.0.py"

if __name__ == '__main__':
    root = CTK.CTk()
    MainWindow.MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    os._exit(1)
