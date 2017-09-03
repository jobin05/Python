""" fauxmo_minimal.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""
import ptvsd
import fauxmo
import logging
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"spot light": 52000,"cove light": 52001,"chandelier":52002,"all":52003}

    def act(self, client_address, state, name):
        print "State", state, "on ", name, "from client @", client_address   
        if state:
            print "LED on"
            GPIO.output(24,GPIO.HIGH)
        else: 
            print "LED off"
            GPIO.output(24,GPIO.LOW)
        return True

if __name__ == "__main__":
    #ptvsd.enable_attach(secret=None)
    #ptvsd.wait_for_attach()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24,GPIO.OUT)
    
    # client = mqtt.Client()
    #client.connect("localhost", 1883, 60)
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    #client.publish("test", "no")

   

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
