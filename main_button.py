import RPi.GPIO as GPIO
import sqlite3
import numpy as np
import time
from rpi_lcd import LCD
#import database

diode_list = [4, 14, 15, 17, 27, 22, 23, 24, 10, 25]
button_list = [7, 5, 12, 6, 13, 16, 19, 20, 26, 21]
lcd = LCD()
basic_speed = 2.1
basic_elements = 0
level = -1
level_completed = 1
value = -1
GPIO.setmode(GPIO.BCM)

for diode in diode_list:
    GPIO.setup(diode, GPIO.OUT)

for button in button_list:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(7, GPIO.RISING, callback=button0, bouncetime=300)
GPIO.add_event_detect(5, GPIO.RISING, callback=button1, bouncetime=300)
GPIO.add_event_detect(12, GPIO.RISING, callback=button2, bouncetime=300)
GPIO.add_event_detect(6, GPIO.RISING, callback=button3, bouncetime=300)
GPIO.add_event_detect(13, GPIO.RISING, callback=button4, bouncetime=300)
GPIO.add_event_detect(16, GPIO.RISING, callback=button5, bouncetime=300)
GPIO.add_event_detect(19, GPIO.RISING, callback=button6, bouncetime=300)
GPIO.add_event_detect(20, GPIO.RISING, callback=button7, bouncetime=300)
GPIO.add_event_detect(26, GPIO.RISING, callback=button8, bouncetime=300)
GPIO.add_event_detect(21, GPIO.RISING, callback=button9, bouncetime=300)


def button0(channel):
    global value
    value = 0


def button1(channel):
    global value
    value = 1


def button2(channel):
    global value
    value = 2


def button3(channel):
    global value
    value = 3


def button4(channel):
    global value
    value = 4


def button5(channel):
    global value
    value = 5


def button6(channel):
    global value
    value = 6


def button7(channel):
    global value
    value = 7


def button8(channel):
    global value
    value = 8


def button9(channel):
    global value
    value = 9


def game_level(speed=basic_speed, elements=basic_elements):
    global value
    elements_list = np.random.choice(len(diode_list), elements, replace=True)
    for i in elements_list:
        print(diode_list[i])
        GPIO.output(i, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(i, GPIO.LOW)
    for i in elements_list:
        while value == -1:
            continue
        if value != i:
            print("Błąd, przegrana!\nTwój wynik to:", level)
            lcd.text("Fail!", 1)
            lcd.text("Score: " + str(level), 2)
            time.sleep(5)
            lcd.clear()
            return 0
        value = -1
    print("Level zaliczony!\n")
    lcd.text("Level " + str(level), 1)
    lcd.text("complited!", 2)
    time.sleep(2)
    lcd.clear()
    value = -1
    return 1


while True:
    lcd.text("Select user", 1)
    lcd.text("default button1", 2)
    time.sleep(2)
    lcd.clear()
    lcd.text("Select user", 1)
    lcd.text("custom button2", 2)
    time.sleep(2)
    lcd.clear()
    if GPIO.input(5) == GPIO.HIGH: #button1
        user_id = "default user"
        password = ""
        break
    if GPIO.input(6) == GPIO.HIGH: #button2
        # user data from telegram TO DO

while level_completed:

    level += 1
    if basic_speed > 0.4:
        basic_speed -= 0.1
    basic_elements += 1
    print(f"Level: {level}\nSpeed: {basic_speed}\nElements: {basic_elements}")
    level_completed = game_level(basic_speed, basic_elements)
