# from picamera import PiCamera
from time import sleep
import time
import boto3
import json
import requests
from datetime import datetime
import tkinter as tk
from tkinter import *

def TakePic(pic_name):
    global states
    media_dir = "./media/notselected/"
    if states.login == False:
        media_dir = "./media/auth/"
    camera = PiCamera()
    st = 255
    camera.start_preview(alpha=st)
    sleep(5)
    camera.capture(media_dir+pic_name)
    camera.start_preview()

def GetPic_name():
    return "image{}.jpg".format(str(datetime.now()))

def pic_identity_auth():
    while True:
        pic_name = GetPic_name()
        TakePic(pic_name)
        auth_url = "https://odyfi9y794.execute-api.us-east-1.amazonaws.com/default/image_rekognition_process"

        headers = {
            'x-api-key': "io6rHprxzM6NXfQE6GKUH37Hrip3lvO8v5ecpKo4",
            'Content-Type': "image/jpeg",
        }
        #successful reko
        file_name = "./media/auth/Jackey.jpg"

        #uncuccessful reko
        #file_name = "media/auth/fail_test.jpg"
        #on pi
        #file_name = "./media/auth/"+pic_name

        with open(file_name,'rb') as f:
            data = f.read()

        response = requests.request("POST", auth_url, headers=headers,data=data)
        try:
            account_info = response.json()
            account = account_info['account']
            pwd = account_info['pwd']
            display_name = account_info['display_name']
            break
        except:
            print('Failed to reko')
            sleep(1)

    return (account, pwd, display_name)



if __name__ == "__main__":
    a = pic_identity_auth()
    print(a)