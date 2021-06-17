
# ------------__ Hacking STEM – wind_turbine.py – micro:bit __-----------
# For use with the Increasing Power Through Design Lesson plan available 
# from Microsoft Education Workshop at 
# https://www.microsoft.com/en-us/education/education-workshop/windmill.aspx
# http://aka.ms/hackingSTEM
#
#  Overview:
#  This code is used with a DC motor that is operates as a generator. It 
#  reads analog pin 0, which is connected to a DC motor, and converts 
#  the vakue to voltage. It then take a second reading at pin 1, which 
#  has a 100 Ohm resistor before it, and using Ohms law calcuates the 
#  current. It then write those 2 values to serial.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *

# Frequency of code looping
dataSpeed = 10

# End of Line Character
EOL='\n'

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate

def readSensors():
    # Each time the loop repeats, voltage reading is reset to 0
    voltage = 0.0000

    # Take 100 voltage readings and keep the highest as "voltage" variable
    for i in range(99):
        pin0_reading = pin0.read_analog()
        # Filter out low readings to 0
        if pin0_reading <= 3:
            pin0_reading = 0
        if pin0_reading > voltage:
            voltage = pin0_reading
            sleep(1)  # Sleep for stability
    
    # Convert the "voltage" variable to an actual voltage value. We now the 
    # range of the reading is between 0 and 1023, which is a total of 1024 
    # values, so we first divide "voltage" by 1024. Second we mulptiple it
    # byt the refrence voltage of the board in milli volts. For the micro:bit
    # that value 3.3 volts or 3300 milli volts.
    voltage = voltage/1024*3300
 
    pin1_reading = pin1.read_analog()
    # Filter out low readings to 0
    if pin1_reading <= 3:
        pin1_reading = 0

    # Convert the "voltage" variable to an actual voltage value. Same as above
    current = pin1_reading/1024*3300

    # In order to derive the current in amps we need to use Ohm's Law.
    # Ohm's Law: Current(Amperage) = Voltage / Resistance
    # This is why there is a 100 Ohm resistor before pin 1. We know the voltage
    # that we calcuated in the pervious step and we know the resistance. So now
    # we simply devide voltage by resistance and get current.
    current = current/100

    # Print Voltage , Current
    uart.write('{},{}'.format(voltage, current)+EOL)

    # Sleep for the dataSpeed before looping the code
    sleep(dataSpeed)


while True:
    readSensors()
