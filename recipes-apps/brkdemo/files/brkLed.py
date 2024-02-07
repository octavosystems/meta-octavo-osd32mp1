"""
--------------------------------------------------------------------------
Octavo Systems - OSD33MP157c-BRK Demo
--------------------------------------------------------------------------
License:
Copyright 2020 - Octavo Systems LLC
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
This file contains the physical interfaces to the OSD32MP1-BRK User LEDs
It provides basic functions like on, off, and blink. It is part of the 
Webserver demo for the BRK
--------------------------------------------------------------------------
"""
import os
import subprocess
import time
import threading

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# Command
GPIO_SET                = "echo {1} > /sys/class/leds/{0}/brightness"
GPIO_GET                = "cat /sys/class/leds/{0}/brightness"

LED_ON                  = "255"
LED_OFF                 = "0"


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

debug                   = True

#LED GPIO definitions
D1G                     = "LED1_GRN"
D1R                     = "LED1_RED"
D2G                     = "LED2_GRN"

#Dictionary that maps the LED string name to the actual GPIO and its status, and if it is Flashing
LEDS                    = {"d1g" : [D1G, LED_OFF, False],
                           "d1r" : [D1R, LED_OFF, False],
                           "d2g" : [D2G, LED_OFF, False]}

# ------------------------------------------------------------------------
# Basic On and Off and Status Functions
# ------------------------------------------------------------------------
def ledRest():
    '''funtion that resets all of the LEDs to the default state LED_OFF'''

    for led in LEDS.keys():
        ledOFF(led)

def ledStatus(led):
    '''
    returns the status of the LED in a String
    :param led: the string that represnets the LED
    :return: a string representating the status of the LED
            On, Off, Flashing.  Returns Off if the led is not valid
    '''
    #make sure the LED is in the dictionary
    if led in LEDS:

        # see if it is flashing
        if LEDS[led][2] == True:
            return "FLASHING"

        #get the status
        status = LEDS[led][1]

        #return the appropriate string
        if status == LED_ON:
            return "ON"
        elif status == LED_OFF:
            return  "OFF"
    #else return off
    return "OFF"

def setLED(led, value):
    """
    Function that physically sets the GPIO
    :param led: the string for the LED
    :param value: the value to set the gpio to
    :return: True if successfull otherwise False
    """
    # make sure the LED is in the dictionary
    if led in LEDS:
        # actually set the GPIO pin to the appropriate value
        os.popen(GPIO_SET.format(LEDS[led][0], value))
        return  True
    return False

def ledON(led):
    '''
    Turns on the specified LED
    :param led: string representing the LED
    :return: True if the LED is set False otherwise
    '''
    # make sure the led is in the dictionary
    if led in LEDS:
        # set the flashing to False to stop flashing
        LEDS[led][2] = False

        # set the led to ON
        if setLED(led, LED_ON):
            LEDS[led][1] = LED_ON
            return True

    return False


def ledOFF(led):
    '''
    Turns off the specified LED
    :param led: string representing the LED
    :return: True if the LED is set False otherwise
    '''
    # make sure the led is in the dictionary
    if led in LEDS:
        #set the flashing variable to false to stop flashing
        LEDS[led][2] = False

        #set the LED to off
        if setLED(led, LED_OFF):
            LEDS[led][1] = LED_OFF
            return True
    return False

def ledFLASH(led):
    """
    A function that starts flashing the specified LED
    :param led: the LED to flash
    :return: True is succcessful false otherwise
    """
    #make sure the led is in the dictionary
    if led in LEDS:
        # set the flashing variable to True
        LEDS[led][2] = True
        #try to start the flashing thread
        try:
              th = threading.Thread(target=_flashThread, args=(led, .5))
              th.start()
              return True
        except:
            #if it fails return False
            LEDS[led][2] = False
            return False

def _flashThread(led, duration = 1):
    """
    Helper function that is used in a thread to actually flash the specified led
    :param led: the led to flash
    :param duration: the time in seconds to wait in between switching modes.  Default is 1 second
    :return: nothing
    """
    # while the flashing variable is true
    while LEDS[led][2]:
        #make sure the flashing variable is still true.  Somebody might have changed it since we last checked
        if LEDS[led][2]:
            # turn the LED on
            setLED(led, LED_ON)
        #sleep for the duration
        time.sleep(duration)
        # make sure the flashing variable is still true.  Somebody might have changed it since we last checked
        if LEDS[led][2]:
            # turn the LED off
            setLED(led, LED_OFF)
        # sleep for the duration
        time.sleep(duration)

def ledSET(led, command):
    '''
    Sets the LED to the passed command
    :param led: the string of the LED
    :param command: a string representing the Command either (On, Off, Blink)
    :return: True if successful, otherwise false
    '''
    #valid commands
    valid_commands = {"on" : ledON, "off" : ledOFF, 'flash' : ledFLASH}
    #make sure the led is in the disctionary
    if led in LEDS:
        #make sure the command is valid
        if command in valid_commands :
            #execute the command
             return valid_commands[command](led)
    return False


