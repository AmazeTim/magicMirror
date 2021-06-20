import threading
from time import sleep
from LEd import  WS2812LED
from rpi_ws281x import PixelStrip, Color
import argparse
class control(WS2812LED):
    def __init__(self):
        self.t_list=[]
        self.LED_COUNT = 30  # Count of LED light
        self.LED_PIN = 18  # DI端接GPIO18
        # 以下可以不用改
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()
    # 子執行緒的工作函數
    def runColorWipe(self):
        self.t_list.append(
            threading.Thread(target=self.colorwipe)
            )
        self.t_list[-1].start()
        for i in self.t_list :
            i.join()
    def runBrightnessAdj(self,Higher=True):
        self.t_list.append(
            threading.Thread(target=self.colorwipe,args= (Higher,))
            )
        self.t_list[-1].start()
        for i in self.t_list :
            i.join()
