import explorerhat, signal, time
import cherrypy
import string  

#pip install cherrypy
cherrypy.config.update("server.conf")

class RobotServer(object):
    def __init__(self, initialcommand="stop"):
        self.status = "stop"
        
        #Start listening for the IR sensors to change
        explorerhat.analog.one.changed(self.handle_analog)
        explorerhat.analog.two.changed(self.handle_analog)
        
        self.do_command(initialcommand)
        

    @cherrypy.expose
    def forward(self, speed=95):
        explorerhat.motor.one.forward(int(speed))
        explorerhat.motor.two.forward(int(speed))
        self.status = "forward"
        return self.status
    
    @cherrypy.expose
    def backward(self, speed=95):
        explorerhat.motor.one.backward(int(speed))
        explorerhat.motor.two.backward(int(speed))
        self.status = "backward"
        return self.status
        
    @cherrypy.expose
    def right(self, speed=95):
        explorerhat.motor.one.forward(int(speed))
        explorerhat.motor.two.backward(int(speed))
        self.status = "right"
        return self.status
    
    @cherrypy.expose
    def left(self, speed=95):
        explorerhat.motor.one.backward(int(speed))
        explorerhat.motor.two.forward(int(speed))
        self.status = "left"
        return self.status
    
    @cherrypy.expose
    def stop(self):
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        self.status = "stop"
        return self.status
    
    @cherrypy.expose
    def index(self):
        return self.status
    
    def do_command(self, cmd=""):
        if (cmd == "forward"):
            self.forward()
        elif cmd == "backward":
            self.backward()
        elif cmd == "left":
            self.left()
        elif cmd == "right":
            self.right()
        elif cmd == "stop":
            self.stop()
        return self.status
    
    #Replicate original k9 interface
    @cherrypy.expose
    def k9(self, motor=""):
        return self.do_command(motor)
        
  
    def handle_analog(self, pin, value):
        #print (pin.name, value, self.status)
        if (value > 2):
            if (self.status != "danger"):
                self.oldstatus = self.status
            self.status = "danger"
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            time.sleep(0.2)
            explorerhat.motor.one.backward()
            explorerhat.motor.two.backward()
            time.sleep(0.7)
            
            if (explorerhat.analog.one.read() > explorerhat.analog.two.read()): 
                explorerhat.motor.one.forward()
                explorerhat.motor.two.backward()
            else:
                explorerhat.motor.one.backward()
                explorerhat.motor.two.forward()
                
            time.sleep(0.5)
            
            self.do_command(self.oldstatus)
            
if __name__ == '__main__':
    cherrypy.quickstart(RobotServer(), config="app.conf")
    
    
    
