import win32com.client as win32
import time
import pyautogui
import webbrowser
import urllib.parse
import os

import Utils

LIST_IMAGE_FILEPATH = Utils.resource_path("list.PNG")
MOVEMENT_IMAGE_FILEPATH = Utils.resource_path("movement.PNG")

class Email(): 
    #Copies the data from McLeod for email
    def copy_from_list():
        data = []
        try:

            # Reset the clipboard
            Utils.reset_clipboard()

            #Open list and copy entry to datastring
            Utils.clickImage(LIST_IMAGE_FILEPATH, 0, 0)
            time.sleep(.5)
            pyautogui.press('down')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            data = Utils.get_clipboard_text().split("\t")
            pyautogui.hotkey('alt','f4')
            time.sleep(0.2)


        except Exception as e:
            pyautogui.alert(e)

        return data

    # build a string for the subject line
    def build_subject(data):
        if len(data) < 3:
            return ""
        subject = (data['issue'] + " - " + data['tractor'] + ' - ' + data['order_number'] + ' - ' + data['bol']
                    + " - " + data['shipper_city'] + " " + data['shipper_state'] + " - " + data['cons_city'] + " " + data['cons_state'])
        Utils.set_clipboard_text(subject) 
        return subject
    
    def create_email(window, email_template):
        #Setting the image to search based on settings
        global MOVEMENT_IMAGE_FILEPATH, LIST_IMAGE_FILEPATH
        MOVEMENT_IMAGE_FILEPATH = os.path.join(os.getenv('APPDATA'), 'EmailBot', 'movement.PNG')if window.parent.settings_tab.settings.get_setting('custom_image_checkbox_val') == 'on' else MOVEMENT_IMAGE_FILEPATH
        LIST_IMAGE_FILEPATH = os.path.join(os.getenv('APPDATA'), 'EmailBot', 'list.PNG')if window.parent.settings_tab.settings.get_setting('custom_image_checkbox_val') == 'on' else LIST_IMAGE_FILEPATH
        
        #Copy data from order/movement screen
        data = Email.copy_from_list()
        Utils.clickImage(MOVEMENT_IMAGE_FILEPATH, 0, 0)
        time.sleep(.5)
        data = data + Email.copy_from_list()
        if data == []:
            return
        
        banned_contacts = ["RBTW", "loadmaster"]
        
        #insert template data
        email_template = window.parent.templates_tab.templates.get_template_by_name(email_template)
        issue = email_template[0]
        csr = email_template[1]
        entered_by = email_template[2]
        dm = email_template[3]
        additional_to = email_template[4].split(',')
        additional_cc = email_template[5].split(',')
        update = email_template[6]
        
        #Create order dictionary from pulled data
        order = {'order_number': data[0], 'bol': data[1], 'po': data[2], 
                'shipper_city': data[3], 'shipper_state':data[4], 'shipper_appt': data[11],
                'cons_city': data[5], 'cons_state':data[6], 'cons_appt': data[12],
                'ordered_by': data[7], 'entered_by': data[8], 'csr':data[9], 'dm': data[14], 'tractor': data[13],
                'issue': issue, 'update': update,
                'customer_contact': window.parent.contacts_tab.contacts_db.get_contact_by_name(data[10]) or ''
                }

        #Create to list 
        to_list_contacts = [order['ordered_by']]
        if csr == 'True': to_list_contacts.append(order['csr'])
        if entered_by == 'True': to_list_contacts.append(order['entered_by'])
        if dm == 'True': to_list_contacts.append(order['dm'])
        if order['customer_contact'] != '': to_list_contacts.append(order['customer_contact'])
        to_list_contacts = to_list_contacts + additional_to


        #Remove banned contacts, contacts with number and duplicates
        toList = ""
        for contact in to_list_contacts:
            if  (contact not in toList
            and contact not in banned_contacts 
            and contact != '' 
            and not Utils.has_numbers(contact)):

                toList = toList + contact + ';'
        toList = toList[:-1]
                
        cc_list = ''
        for contact in additional_cc:
            cc_list = cc_list +contact+';'


        email = ('REG#: ' + order['order_number'] + "\n" +
                    "CUST REF#: " + order['bol'] + "\n" +
                    "PO#: " + order['po'] + "\n" +
                    "PICK UP APPT: " + order['shipper_city'] + ", " + order['shipper_state'] + ' ' + order['shipper_appt'] + "\n" +
                    "DELIVERY APPT: " + order['cons_city'] + ", " + order['cons_state'] + ' ' + order['cons_appt'] + "\n" +
                    "UPDATE: " + order['update'])


        match window.parent.settings_tab.settings.get_setting('email_option'):
            case 'Offline':
                Email.open_outlook_draft_offline(
                to=toList,
                subject=Email.build_subject(order),
                body=email,
                cc=cc_list,
                )
            case 'Online':
                Email.open_outlook_draft_online(
                to=toList,
                subject=Email.build_subject(order),
                body=email,
                cc=cc_list,
                )

    def open_outlook_draft_online(to: str, subject: str, body: str, cc: str = "", bcc: str = ""):
        # Base URL for opening an Outlook draft
        base_url = "https://outlook.office.com/mail/deeplink/compose?"

        # Encode the email fields
        params = {
            "to": to,
            "subject": subject,
            "body": body,
            "cc": cc,
            "bcc": bcc
        }

            # Manually URL-encode each parameter (spaces become %20 instead of +)
        encoded_params = {k: urllib.parse.quote(v) for k, v in params.items() if v}

        # Build the query string manually
        query_string = '&'.join([f"{k}={v}" for k, v in encoded_params.items()])

        # Create the full URL
        full_url = base_url + query_string

        # Open the URL in the default web browser
        webbrowser.open(full_url)

    def open_outlook_draft_offline(to: str, subject: str, body: str, cc: str = "", bcc: str = ""):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = to
        mail.CC = cc
        mail.Subject = subject
        mail.Body = body
        mail.Display(True)
        


