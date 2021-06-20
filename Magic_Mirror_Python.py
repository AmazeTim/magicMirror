import tkinter as tk
from tkinter import *
from tkinter import messagebox
from utils import *
import time
from time import sleep
from newsapi import NewsApiClient
import os
#import boto3
import json
from datetime import datetime
from state import LoginStates
#from LED import LEDWS2812LED

states = LoginStates()


decrypt = list()

global iteration
global timecount
global repull
global sleep
iteration = 0
timecount = 0
repull = 0
sleep = 0


while True:
    def TakePic(pic_name):
        global states
        camera = PiCamera()
        media_dir = "./media/auth/"
        if states.login == True:
            media_dir = "./media/notselected/"
        st = 255
        camera.start_preview(alpha=st)
        sleep(5)

        camera.capture(media_dir + pic_name)
        camera.stop_preview()

    def _5times_takepic():
        LED = WS2812LED()
        LED.colorWipe()
        def des():
            picshower.destroy()
        def higher():
            LED.BrightnessAdj(HIGHER=True)
        def lower():
            LED.BrightnessAdj(HIGHER=False)
        for i in range(1,6):
            picshower = tk.Toplevel()
            picshower.geometry("1920x1080")
            picshower.attributes("-fullscreen", True)
            TakePic(str(i))
            im = PIL.Image.open("./media/notselected"+str(i))
            photo = PIL.ImageTk.PhotoImage(im)
            label = tk.Label(picshower, image=photo)
            label.image = photo  # keep a reference!
            Destroy = tk.Button(picshower, text='Sign up',command=des)
            High = tk.Button(picshower, text='Sign up', command=higher)
            Low = tk.Button(picshower, text='Sign up', command=lower)
            label.pack()
            Destroy.pack()
            High.pack()
            Low.pack()


    def GetPic_name():
        return "image{}.jpg".format(str(datetime.now()))

    def pic_identity_auth():
        global states
        again = False

        pic_name = GetPic_name()
        TakePic(pic_name)
        auth_url = "https://odyfi9y794.execute-api.us-east-1.amazonaws.com/default/image_rekognition_process"

        headers = {
            'x-api-key': "io6rHprxzM6NXfQE6GKUH37Hrip3lvO8v5ecpKo4",
            'Content-Type': "image/jpeg",
        }
        # successful reko
        file_name = "./media/auth/Jackey.jpg"

        # uncuccessful reko
        # file_name = "media/auth/fail_test.jpg"
        # on pi
        # file_name = "./media/auth/"+pic_name

        with open(file_name, 'rb') as f:
            data = f.read()

        response = requests.request("POST", auth_url, headers=headers, data=data)
        try:
            account_info = response.json()
            states.account = account_info['account']
            states.pwd = account_info['pwd']
            states.login = True
            states.display_name = account_info['display_name']
        except:
            #SHOW FAILED
            print('Failed to reko')
            sleep(1)
        if self.login:
            messagebox.showinfo('Success','Login!!')
        else:
            again = messagebox.askokcancel('Failed','Login Failed!! Auth Again?')

        if again == True:
            pic_identity_auth()

    def picbrowser():
        global states
        pic_folder = "./media/notselected"
        if states.login == True:
            picshower = tk.Toplevel()
            picshower.geometry("1920x1080")
            picshower.attributes("-fullscreen",True)

            pictures = [f for f in listdir(pic_folder) if isfile(join(pic_folder, f))]
            count_pic = len(pictures)




    def Pic_loginornot():
        global states
        if states.login == True:
            _5times_takepic()
        else:
            pic_identity_auth()


    def tick(time1=''):
        time2 = time.strftime("%H")
        if time2 != time1:
            time1 = time2
            clock_frame.config(text=time2)
        clock_frame.after(200, tick)

    def tickk(time3=''):
        time4 = time.strftime(":%M:%S")
        if time4 != time3:
            time3 = time4
            clock_frame2.config(text=time4)
        clock_frame2.after(200, tickk)

    #This function waits for a certain amount of 'tocks' and then initiates 'newsheader' -function
    def tock():
        global timecount
        global repull
        global sleep
        global decrypt
        newstitle.after(200, tock)
        if timecount < 20:
            timecount +=1
        else:
            timecount = 0
            newsheader()
        if repull < 200:
            repull +=1
        else:
            repull = 0
            headlines = api.get_top_headlines(sources='bbc-news')
            payload = headlines
            decrypt = (payload['articles'])
            maxrange = len(decrypt)
        if sleep < 800:
            sleep+=1
        else:
            sleep = 0
            motiondetector()

    api = NewsApiClient(api_key='a3343f0f96a346bc88eb74227bfe9f64')

    #This sequence decrypts the info feed for the script
    headlines = api.get_top_headlines(sources='bbc-news')
    #print(headlines)
    payload = headlines
    decrypt = (payload['articles'])
    maxrange = len(decrypt)

    #This function iterates over the news headlines. Iteration is the news number, 'itemlist' brings out only the title.
    def newsheader():
        global iteration
        global decrypt
        itemlist = decrypt[iteration]
        #print(itemlist['title'])
        newstitle.config(text=itemlist['title'])
        source.config(text=itemlist['author'])
        if iteration < 9:
            iteration +=1
        else:
            iteration = 0


    root = tk.Tk()
    root.title('Mirror')

    masterclock = tk.Label(root)
    masterclock.pack(anchor=NW, fill=X, padx=45)
    masterclock.configure(background='black')
    clock_frame = tk.Label(root, font = ('caviar dreams', 130), bg='black', fg='white')
    clock_frame.pack(in_=masterclock, side=LEFT)
    clock_frame2 = tk.Label(root, font = ('caviar dreams', 70), bg='black', fg='white')
    clock_frame2.pack(in_=masterclock, side=LEFT, anchor = N, ipady=15)
    newstitle = tk.Label(root, font = ('caviar dreams', 30), bg='black', fg='white')
    newstitle.pack(side=BOTTOM, anchor=W, fill=X)
    source = tk.Label(root, font = ('caviar dreams', 20), bg='black', fg='white')
    source.pack(side=BOTTOM, anchor=W, fill=X)

    #Take Pic for post or for Auth
    takepic = tk.Button(root, text="Camera", command=Pic_loginornot)
    takepic.pack(side=RIGHT, anchor=W, fill=X)

    #picture browser
    browser = tk.Button(root, text="Open gallery", command=picbrowser)
    browser.pack(side=RIGHT, anchor=W, fill=X)

    newsheader()
    tick()
    tickk()
    tock()

    root.attributes("-fullscreen", True)
    root.configure(background='black')
    root.mainloop()


