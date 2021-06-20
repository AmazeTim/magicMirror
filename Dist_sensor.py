import RPi.GPIO as GPIO
import time
import pyautogui

class Sensor():
    def __init__(self, trig, echo):
        #GPIO Pins
        self.GPIO_TRIGGER = trig
        self.GPIO_ECHO = echo


    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def send_trigger_pulse(self):
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.001)
        GPIO.output(self.GPIO_TRIGGER, False)


    def wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.GPIO_ECHO) != value and count > 0:
            count = count - 1


    def get_distance(self):
        self.send_trigger_pulse()
        self.wait_for_echo(value=True, timeout=5000)
        start = time.time()
        self.wait_for_echo(value=False, timeout=5000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len * 340 * 100 / 2
        return distance_cm

def right_hand():
    pyautogui.click(x=1905, y=970)

def left_hand():
    pyautogui.click(x=1905, y=1000)

def both_hand():
    pyautogui.click(x=1905, y=1030)

def yes():
    pyautogui.click(x=907,y=603)

def no():
    pyautogui.click(x=1000,y=603)


if __name__ == "__main__":
    Sensor_1 = Sensor(trig=17, echo=27) #右手
    Sensor_2 = Sensor(trig=23, echo=24) #左手

    while True:
        sensor1 = Sensor_1.get_distance()
        sensor2 = Sensor_2.get_distance()

        if sensor1 <100 and sensor2 <100:
            both_hand()
        elif 10 < sensor1 < 100:
            right_hand()
        elif 10 < sensor2 < 100:
            left_hand()
        elif sensor1 <=10:

        elif sensor2 <=10:

        print("Sensor 1 : cm =%f" % sensor1)
        print("Sensor 2 : cm =%f" % sensor2)
        time.sleep(1)


