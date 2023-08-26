import RPi.GPIO as GPIO
import requests
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
GPIO_TRIGGER = 14
GPIO_ECHO = 15

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

TOKEN = "BBFF-zctvUtkR4beVQWueHDaBzvsKiQCaRa"  # Put your TOKEN here
DEVICE_LABEL = "demo"  # Put your device label here
ULTRASONIC1 = "ultrasonic"

# Ubidots API Endpoint
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"

HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json"
}

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            
            # Prepare data to be sent to Ubidots
            data = {
                ULTRASONIC1: dist
            }

            response = requests.post(
                UBIDOTS_URL,
                headers=HEADERS,
                json=data
            )

            if response.status_code == 200:
                print("Data sent to Ubidots successfully.")
            else:
                print("Failed to send data to Ubidots. Status code:", response.status_code)
            
            time.sleep(0.5)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
