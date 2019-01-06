from subprocess import call
from bottle import *

# Created Jan 2019, Stuart Ianna

#Using subprocess, so need the pin number as a string
LED = '44'

#PWM frequency, 1000Hz is a good value
pwmFrequency = '1000'

#Keep track of the number of times the post request occurs
#This is for demonstration of sending data to front-end from server
postRequests = 0

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

#The get request is sent from the front and JQuery app. Only from toggle switch
#This is one way data from front end to server
#This is how we can interact with the python and omega2+ side.
@get('/_state')
def toggle():

    #'request' is part of the get call, it is already a python dictionary 
    #so we can sent it straight to our function
    setPinOutput(request.query)
    return

#This is another method of sending data from front end to server, except now we send back data
#This is a better method as the data can be of any length, sent as a python dictionary type
#This method is called from the PWM slider
@post('/_state')
def toggle():

    #We need to make reference to the global variable
    #not sure how acceptable this is for bottle
    global postRequests

    #The request in this case is of type bottle.LocalRequest
    #We can convert it into a python dictionary with the following
    req = request.json

    #req is now a dictionary, we can use it to call setPinOutput
    setPinOutput(req)

    #Increment the number or requests
    postRequests = postRequests + 1

    #This is how to send some data back to front end.
    #This information is printed to console for the demo
    info = {}
    info['duty'] = 'Current duty cycle: {}'.format(req['duty'])
    info['state'] = 'Current LED state: {}'.format(req['state'])
    info['requests'] = 'Total PWM changes: {}'.format(postRequests)
    return info

#This function provides the interface between the server and Omegle2+
#It takes a dictionary with keys state and duty and sets the LED accordingly
def setPinOutput(pinStatus):

    if pinStatus['state'] == 'on':
        setOn(pinStatus['duty'])
    elif pinStatus['state'] == 'off':
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
    call(["fast-gpio","set", LED, "1"])

    #Run the server on 0.0.0.0 so its available over the local network.
    #The site can be viewed from a browser on 'omega2+ IP':5000
    #eg 192.168.0.5:5000
    run(host="0.0.0.0", port=5000,reload=True)
