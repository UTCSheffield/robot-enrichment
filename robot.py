import explorerhat, signal
def handle_analog(pin, value):



  print (pin.name, value)
  if (pin.name == "one" and value > 2):
    
    explorerhat.motor.one.forward()
    explorerhat.motor.two.backward()
  else:
    explorerhat.motor.two.forward()


explorerhat.analog.one.changed(handle_analog)
#signal.pause()


explorerhat.motor.one.forward()
explorerhat.motor.two.forward()

while True:
  explorerhat.light.red.write(explorerhat.touch.eight.is_pressed())
  if (explorerhat.touch.four.is_pressed()):
    break;

explorerhat.motor.one.stop()
explorerhat.motor.two.stop()

