#!/usr/bin/env python

from gpiozero import Button
from signal import pause

def say_hello():
    print("Hello!")

button = Button(pin=18, pull_up=False, bounce_time=1)

button.when_pressed = say_hello

pause()