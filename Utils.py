import datetime
import time
import os
import sys

import win32clipboard
import win32api
import win32con

import pyautogui



def to_24_time(minutes):
    return str(round(100*(minutes//60) + minutes%60))

#Converts time formats to minutes
def to_minutes(time):
    time = time.replace(':', "").zfill(4)
    return (int((time)[:2])*60) + (int((time)[-2:]))

def time_diff(time1, time2):
    time1_date = time1.split(" ")[0].split('/')
    time2_date = time2.split(" ")[0].split('/')

    time1_time = time1.split(" ")[1]
    time2_time = time2.split(" ")[1]

    date1 = datetime.datetime(int(time1_date[2]),int(time1_date[0]),int(time1_date[1]),int(time1_time[:2]), int(time1_time[-2:]), 0)
    date2 = datetime.datetime(int(time2_date[2]),int(time2_date[0]),int(time2_date[1]),int(time2_time[:2]), int(time2_time[-2:]), 0)
    diff = date2 - date1
    return round(diff.total_seconds() / 60)

def time_add(time, time_delta):
    time_date = time.split(" ")[0].split('/') # [9/28/2024, 1300] -> [9,28,2024]
    time_time = time.split(" ")[1]

    #datetime object takes in (YYYY,MM,DD,HH,MM,SS) 

    time = datetime.datetime(int(time_date[2]),int(time_date[0]),int(time_date[1]),int(time_time[:2]), int(time_time[-2:]), 0)
    
    # Calling the timedelta() function  
    time_change = datetime.timedelta(minutes=time_delta)
    new_time = time + time_change
    new_time = new_time.strftime("%m/%d/%Y %H%M")

    return new_time

def time_sub(time, time_delta):
    time_date = time.split(" ")[0].split('/')
    time_time = time.split(" ")[1]

    time = datetime.datetime(int(time_date[2]),int(time_date[0]),int(time_date[1]),int(time_time[:2]), int(time_time[-2:]), 0)
    
    # Calling the timedelta() function  
    time_change = datetime.timedelta(minutes=time_delta) 
    new_time = time - time_change
    new_time = new_time.strftime("%m/%d/%Y %H%M")
    return new_time

def get_now():
        return datetime.datetime.now().strftime("%m/%d/%Y %H%M")

#Get the date
def get_date(date):
    return int(date.split(" ")[0].split("/")[1])

# Reset the clipboard
def reset_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

# Set the clipboard to parameter text
def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

# return the value in clipboard
def get_clipboard_text():
    i = 0
    while i < 10:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            break
        except Exception:
            win32clipboard.OpenClipboard()
            win32clipboard.CloseClipboard()
            time.sleep(0.01)
            i+=1
            continue

    return data

def export_to_excel():
    data = None
    pyautogui.press('down', presses=5)
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(2)
    i=0
    while i < 1000 and data == None:
        data = get_clipboard_text()
        i+=1

    return data

def save_array_to_txt(array, file_name):
        # Open the file in write mode
        with open(file_name, 'w') as file:
            # Iterate over the array and write each element on a new line
            for item in array:
                file.write(f"{item}\n")

        os.startfile(file_name)

# check if string has numbers
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# Find an image and click it
def clickImage(imgName, xOffset, yOffset):
    # Search image
    img = pyautogui.locateOnScreen(imgName, confidence=.9)

    # click image
    win32api.SetCursorPos((pyautogui.center(img).x + xOffset, pyautogui.center(img).y + yOffset))
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
