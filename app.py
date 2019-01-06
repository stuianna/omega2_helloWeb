from subprocess import call
from bottle import *

# Created Jan 2019, Stuart Ianna

#Using subprocess, so need the pin number as a string
LED = '44'

#PWM frequency, 1000Hz is a good value
pwmFrequency = '1000'

#'call' works like the command was entered into a terminal.
# The normal terminal command for setting a pin is 'fast-gpio set PIN STATE'
def setOn(dutyCycle):

    #Becuase the LED is active LOW, we need to reverse the duty cycle value
    dutyCycle = str(100 - int(dutyCycle))

    #Because we are using PWM, the on function actually writes PWM value
    call(["fast-gpio","pwm", LED, pwmFrequency, dutyCycle])

def setOff():

    #The LED is active low, so a high write (1) turns the LED off
    call(["fast-gpio","set", LED, "1"])

#The get request is sent from the front and JQuery app.
#This is how we can interact with the python and omega2+ side.
@get('/_state')
def toggle():

    #'request' is part of the get call, this matches the data sent from jQuery
    state = request.query["state"]
    dutyCycle = request.query["duty"]

    if state == 'on':
        setOn(dutyCycle)
    elif state == 'off':
        setOff()
    else:
    	#This shouldn't happen
        print('Error: invalid state received')
    return
    
#The 'route' is the address of the request relative the base address
#Additional pages can be added with @route('/pageName')
#The @view is the name of the file in the views directory
@route('/')
@view('index')
def mainView():
    return

#This is where code starts executing from:
if __name__ == '__main__':

    #Set the LED state to off initially
    #The LED is active low, so need to set the pin high
    #call(["fast-gpio","set", LED, "1"])

    #Run the server on 0.0.0.0 so its available over the local network.
    #The site can be viewed from a browser on 'omega2+ IP':5000
    #eg 192.168.0.5:5000
    run(host="0.0.0.0", port=5000,reload=True)
