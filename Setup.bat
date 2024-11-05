

@echo off

start https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe
Echo "Please continue when Python is installed."
Pause 
cls
echo "| LOADING |"
echo "|-        |"
py -m ensurepip --default-pip
cls
echo "| LOADING |"
echo "|--       |"
py -m pip install --upgrade pip setuptools wheel
cls
echo "| LOADING |"
echo "|---      |"
py -m pip install "Pillow" --upgrade
cls
echo "| LOADING |"
echo "|----     |"
py -m pip install "pywin32" --upgrade
cls
echo "| LOADING |"
echo "|-----    |"
py -m pip install "pyautogui" --upgrade
cls
echo "| LOADING |"
echo "|------   |"
py -m pip install "pysimpleGUI" --upgrade
cls
echo "| LOADING |"
echo "|---------|"
py -m pip install "requests"
py -m pip install "beautifulsoup4
py -m pip install "selenium"
py -m pip install "customtkinter"
py -m pip install "opencv-python"
py "EmailBot5.py"

exit
