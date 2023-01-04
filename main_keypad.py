import RPi.GPIO as GPIO
import sqlite3
import numpy as np
import time
from rpi_lcd import LCD
#import database

diode_list = [4, 14, 15, 17, 27, 22, 23, 24, 10, 25]
lcd = LCD()
basic_speed = 2.1
basic_elements = 0
level = -1
level_completed = 1
value = -1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for diode in diode_list:
    GPIO.setup(diode, GPIO.OUT)

L1 = 5
L2 = 6
L3 = 13
L4 = 19
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

C1 = 12
C2 = 16
C3 = 20
#C4 = 21
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



diode_list = [16, 20, 21]
button_list = [1, 2, 3, 4]

connection = sqlite3.connect('memory_game.db')
cursor = connection.cursor()


def readLine(line, characters):
    global value
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        value = characters[0]
    if(GPIO.input(C2) == 1):
        value = characters[1]
    if(GPIO.input(C3) == 1):
        value = characters[2]
#    if(GPIO.input(C4) == 1):
#        print(characters[3])
    GPIO.output(line, GPIO.LOW)


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
            readLine(L1, ["1", "2", "3"])
            readLine(L2, ["4", "5", "6"])
            readLine(L3, ["7", "8", "9"])
            readLine(L4, ["*", "0", "#"])
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
