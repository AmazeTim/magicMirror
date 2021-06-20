#!/usr/bin/env python
#coding=utf-8

import time
from rpi_ws281x import PixelStrip, Color
import argparse

'''

'''
class WS2812LED():
    def __init__(self):
        self.LED_COUNT = 30       # LED燈
        self.LED_PIN = 18          # DI端接GPIO18

        # 基本設定
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz
        self.LED_DMA = 10          # DMA channel to use for generating signal
        self.LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    def colorWipe(strip, color, wait_ms=20):

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(strip, color, wait_ms=50, iterations=10):

        for j in range(iterations):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)

    def wheel(pos):

        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(strip, wait_ms=20, iterations=1):

        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbowCycle(strip, wait_ms=10, iterations=5):

        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel(
                    (int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(strip, wait_ms=50):

        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print('Color wipe animations.')
            colorWipe(strip, Color(255, 255, 0))  # Red wipe
            colorWipe(strip, Color(0, 0, 0), 30)
            colorWipe(strip, Color(0, 255, 255))  # Blue wipe
            colorWipe(strip, Color(0, 0, 0), 30)
            colorWipe(strip, Color(255, 0, 255))  # Green wipe
            colorWipe(strip, Color(0, 0, 0), 30)
            
            print('Theater chase animations.')
            print('Rainbow animations.')
            rainbow(strip)
            colorWipe(strip, Color(0, 0, 0), 50)
            rainbowCycle(strip)
            colorWipe(strip, Color(0, 0, 0), 40)
            break
        while True:
            rainbowCycle(strip)
            colorWipe(strip, Color(0, 0, 0), 100)

    except:
        colorWipe(strip, Color(0, 0, 0), 100)
