import explorerhat, signal, time

#What to do when an IR sensor changes
def handle_analog(pin, value):
  print (pin.name, value)
  if (pin.name == "one" and value > 2):
    explorerhat.motor.one.backward()
    explorerhat.motor.two.backward()
    time.sleep(1.5)
    
    explorerhat.motor.one.forward()
    explorerhat.motor.two.backward()
    time.sleep(1)
    explorerhat.motor.one.forward()
    explorerhat.motor.two.forward()
    
#Start waiting for changes on the IR sensor
explorerhat.analog.one.changed(handle_analog)
#signal.pause()

#Start the motors
explorerhat.motor.one.forward()
explorerhat.motor.two.forward()

#Keep looping round
while True:
  explorerhat.light.red.write(explorerhat.touch.eight.is_pressed())
  if (explorerhat.touch.four.is_pressed()):
    break;

#if we break out of the loop stop the motors
explorerhat.motor.one.stop()
explorerhat.motor.two.stop()

