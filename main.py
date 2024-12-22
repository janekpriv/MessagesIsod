import requests
from dotenv import load_dotenv
import os
import time 

load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
APIKEY = os.getenv("APIKEY")
NOTIFICATION_API_KEY = os.getenv("NOTIFICATION_API_KEY")

def main():
    new_notification = {}
    while True:
        

        message = get_info_from_isod()

        if check_message(message,new_notification):
            new_notification=message
            send_notification(new_notification)
        time.sleep(60)

def get_info_from_isod():
    response = requests.get(
        f"http://isod.ee.pw.edu.pl/isod-portal/wapi?q=mynewsfull&username={USERNAME}&apikey={APIKEY}&from=0&to=1"
    ).json()
  
    message = {
        "title": response['items'][0]['subject'],
        "author" : response['items'][0]['modifiedBy'],
        "content" : response['items'][0]['content'],
        "date": response['items'][0]['modifiedDate']
    }
    return message



def check_message(message, new_notification):
    if message != new_notification:
        return True
    return False

def send_notification(new_notifications):    
    response = requests.post(
        "https://push.techulus.com/api/v1/notify",
        headers={
            "Content-Type":"application/json",
            "x-api-key" : NOTIFICATION_API_KEY
        },
        json={
            "title": new_notifications['title'],
            "body": new_notifications['author']
        }
    )
    print("Notification sent!")

if __name__=="__main__":
    main()
