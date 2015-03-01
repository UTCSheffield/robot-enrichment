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
        
        self.do_command(initialcommand)
        

    @cherrypy.expose
    def forward(self, speed=90):
        explorerhat.motor.one.forward(speed)
        explorerhat.motor.two.forward(speed)
        self.status = "forward"
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
        elif cmd == "stop":
            self.stop()
        
        return self.status
    
    #Replicate original k9 interface
    @cherrypy.expose
    def k9(self, motor=""):
        return self.do_command(motor)
        
  
    def handle_analog(self, pin, value):
        print (pin.name, value)
        if (pin.name == "one" and value > 2):
            self.oldstatus = self.status
            self.status = "danger"
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            time.sleep(0.4)
            explorerhat.motor.one.backward()
            explorerhat.motor.two.backward()
            time.sleep(1.5)
            explorerhat.motor.one.forward()
            explorerhat.motor.two.backward()
            time.sleep(1)
            
            self.do_command(self.oldstatus)
            
if __name__ == '__main__':
    cherrypy.quickstart(RobotServer(), config="app.conf")
    
    
    
