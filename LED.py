#!/usr/bin/env python
#coding=utf-8

import time
from time import sleep
from rpi_ws281x import PixelStrip, Color
import argparse

class WS2812LED():
    def __init__(self):
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


    def Setup(self):
        self.strip = self.SetStrip()
        self.strip.begin()

    def SetStrip(self):
        return PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

    def colorWipe(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(255,255,255))
            self.strip.show()

    def BrightnessAdj(self,Higher=True):
        if Higher:
            if self.LED_BRIGHTNESS > 205:
                self.LED_BRIGHTNESS = 255
                self.Setup()
                self.colorWipe()

            else:
                self.LED_BRIGHTNESS += 50
                self.Setup()
        else:
            if self.LED_BRIGHTNESS < 50:
                self.LED_BRIGHTNESS = 0
                self.Setup()
                self.colorWipe()
            else:
                self.LED_BRIGHTNESS -=50
                self.Setup()
                self.colorWipe()
        return 0
if __name__ == "__main__":
    a = WS2812LED()
    a.colorWipe()
    a.BrightnessAdj(Higher=False)
    sleep(2)
    a.BrightnessAdj(Higher=False)
    sleep(2)
    a.BrightnessAdj(Higher=False)
    sleep(2)
    a.BrightnessAdj(Higher=False)
