import RPi.GPIO as GPIO
import time

def send_trigger_pulse(GPIO_TRIGGER):
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.001)
    GPIO.output(GPIO_TRIGGER,False)

def wait_for_echo(value,timeout,GPIO_ECHO):
    count = timeout
    while GPIO.input(GPIO_ECHO) != value and count > 0 :
        count = count -1

def get_distance(trigger,echo):
    send_trigger_pulse(trigger)
    wait_for_echo(True, 5000,echo)
    start = time.time()
    wait_for_echo(False, 5000,echo)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 * 100 /2
    return distance_cm

def main():


    GPIO.setmode(GPIO.BCM)
    #GPIO Pins
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24
    GPIO_TRIGGER_2 = 17
    GPIO_ECHO_2 = 27
    
    #set GPIO direction(IN/OUT)
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER_2,GPIO.OUT)
    GPIO.setup(GPIO_ECHO_2, GPIO.IN)

    while True:
        sensor1 = get_distance(GPIO_TRIGGER, GPIO_ECHO)
        sensor2 = get_distance(GPIO_TRIGGER_2,GPIO_ECHO_2)
        
        print("Sensor 1 : cm =%f" %sensor1)
        print("Sensor 2 : cm =%f" %sensor2)
        time.sleep(1)
        
main()