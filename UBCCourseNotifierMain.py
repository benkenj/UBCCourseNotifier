import os
from twilio.rest import Client
from urllib.request import urlopen

import re
import time
import smtplib

#need twilio credientials to run
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]
ubc_url = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=" 

WAIT_TIME = 20

def sendMessage(message, phonenumber):
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=phonenumber,
        from_=twilio_number,
        body=message
    )

def check_seats(url, user_info, regex_objects):
    web_page_text = urlopen(url).read()
    htmlText = web_page_text.decode("utf8")

    general = re.search(regex_objects["general_seats"], htmlText)
    restricted = re.search(regex_objects["restricted_seats"], htmlText)
    temp_unavailable = htmlText.find("Note: this section is temp. unavailable")

    print("Still looking...")
    print("Restricted Seats: ", restricted.group(1))
    print("General Seats: ", general.group(1))
    if temp_unavailable != -1:
        return 3
    if not general or not restricted:
        print("Something went wrong, maybe you put the wrong url in or lost internet connection, try restarting")
        return 0
    if general.group(1) != '0':
        return 1
    if restricted.group(1) != '0':
        return 2
    else:
        return 0

def compile_regex():
    regexs = {}
    regexs["general_seats"] = re.compile("<td width=&#39;200px&#39;>General Seats Remaining:</td><td align=&#39;left&#39;><strong>(.*?)</strong></td>")
    regexs["restricted_seats"] = re.compile("<td width=&#39;200px&#39;>Restricted Seats Remaining\*:</td><td align=&#39;left&#39;><strong>(.*?)</strong></td>")
    return regexs

#gathers nessesary user info
def gather_user_info():
    user_info = {}
    user_info['department'] = input("Enter department:")
    user_info["course_number"] = input("Enter course number: ")
    user_info["section"] = input("Enter section number: ")

    user_info["phone_number"] = input("Enter phone number:(in format +xxxxxxxxxxx) ")
    user_info["restricted"] = input("Are restricted seats okay?(yes/no)")
    return user_info

def main():
    user_info = gather_user_info()
    print(user_info['department'])
    defined_url = ubc_url + user_info["department"] + "&course=" + user_info["course_number"] + "&section=" + user_info["section"]
    regex_objects = compile_regex()
    compile_regex()
    while True:
        status = check_seats(defined_url, user_info, regex_objects)

        if status == 1:
            print("GENERAL SEAT AVAILABLE SENDING MESSAGE")
            sendMessage('There is a general seat available in ' + user_info["department"] + ' ' + user_info["course_number"] + '! Grab it here: ' + defined_url, user_info["phone_number"])
            break
        if status == 2:
            if user_info["restricted"] == "yes":
                print("RESTRICTED SEAT AVAILABLE")
                sendMessage('There is a restricted seat available in ' + user_info["department"] + ' ' + user_info["course_number"] + '! Grab it here: ' + defined_url, user_info["phone_number"])
            break
        if status == 3:
            print("The course is temporarily unavailable")
            time.sleep(WAIT_TIME)
        else:
            time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main()