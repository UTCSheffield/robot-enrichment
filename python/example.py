#python library use example

from pimote import PiMote

pm = PiMote()

try:
    # We will just loop round switching the units on and off
    while True:
        raw_input('hit return key to send socket 1 ON code')
        # Set K0-K3
        print "sending code 1111 socket 1 on"
        pm.power(1, True)
        
        raw_input('hit return key to send socket 1 OFF code')
        # Set K0-K3
        print "sending code 0111 Socket 1 off"
        pm.power(1, False)
        
        raw_input('hit return key to send socket 2 ON code')
        # Set K0-K3
        print "sending code 1110 socket 2 on"
        pm.power(2, True)
        
        raw_input('hit return key to send socket 2 OFF code')
        # Set K0-K3
        print "sending code 0110 socket 2 off"
        pm.power(2, False)
        
        raw_input('hit return key to send ALL ON code')
        # Set K0-K3
        print "sending code 1011 ALL on"
        pm.power(0, True)
        
        raw_input('hit return key to send ALL OFF code')
        # Set K0-K3
        print "sending code 0011 All off"
        pm.power(0, False)
        
# Clean up the GPIOs for next time
except KeyboardInterrupt:
    GPIO.cleanup()

