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

        self.speed_factors = {"one":1, "two":0.8}
        
        self.encoders = {"one":0, "two":0}

        self.speed_adjust = 0.05;

        explorerhat.input.one.on_changed(self.handle_encoder, 15)
        explorerhat.input.two.on_changed(self.handle_encoder, 15)
        
        self.do_command(initialcommand)

    def reset_encoders(self):
        self.encoders = {"one":0, "two":0}

    def tune_speed_factors(self):

        if (self.status == "forward"):
            ticks = (self.encoders["one"] + self.encoders["two"])
            #if ticks >= 30 and (ticks % 10) == 0:
            if (ticks % 8) == 0:
                #both start at 100 and slow the faster one until they match. if the one that isn't 100 is now the slower one speed it up.
                if self.encoders["one"] > self.encoders["two"]:
                    if self.speed_factors["two"] < 1:
                        self.speed_factors["two"] = min(self.speed_factors["two"] + self.speed_adjust, 1)
                    else:
                        self.speed_factors["one"] = max(self.speed_factors["one"] - self.speed_adjust, 0.5)
                elif self.encoders["one"] < self.encoders["two"]:
                    if self.speed_factors["one"] < 1:
                        self.speed_factors["one"] = min(self.speed_factors["one"] + self.speed_adjust, 1)
                    else:
                        self.speed_factors["two"] = max(self.speed_factors["two"] - self.speed_adjust, 0.5)

                print ("self.encoders", self.encoders, self.encoders["one"] - self.encoders["two"], "speed_factors", self.speed_factors)
                explorerhat.motor.one.forward(self.speed * self.speed_factors["one"])
                explorerhat.motor.two.forward(self.speed * self.speed_factors["two"])

    @cherrypy.expose
    def forward(self, speed=100):
        self.speed = int(speed)
        self.reset_encoders()
        explorerhat.motor.one.forward(self.speed * self.speed_factors["one"])
        explorerhat.motor.two.forward(self.speed * self.speed_factors["two"])
        self.status = "forward"
        return self.status
    
    @cherrypy.expose
    def backward(self, speed=100):
        self.speed = int(speed)
        self.reset_encoders()
        explorerhat.motor.one.backward(self.speed * self.speed_factors["one"])
        explorerhat.motor.two.backward(self.speed * self.speed_factors["two"])
        self.status = "backward"
        return self.status
        
    @cherrypy.expose
    def right(self, speed=100):
        self.speed = int(speed)
        self.reset_encoders()
        explorerhat.motor.one.forward(self.speed * self.speed_factors["one"])
        explorerhat.motor.two.backward(self.speed * self.speed_factors["two"])
        self.status = "right"
        return self.status
    
    @cherrypy.expose
    def left(self, speed=100):
        self.speed = int(speed)
        self.reset_encoders()
        explorerhat.motor.one.backward(self.speed * self.speed_factors["one"])
        explorerhat.motor.two.forward(self.speed * self.speed_factors["two"])
        self.status = "left"
        return self.status
    
    @cherrypy.expose
    def stop(self):
        self.reset_encoders()
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        self.status = "stop"
        return self.status
    
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/static/index.html")

    @cherrypy.expose
    def getstatus(self):
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
        
  
    def handle_encoder(self, pin):
        self.encoders[pin.name] += 1
        #print (pin.name, self.encoders[pin.name], pin.last, pin.read() )
        self.tune_speed_factors()
        

    def handle_analog(self, pin, value):
        #print (pin.name, value, self.status)
        if (value > 2 and self.status != "stop"):
            if (self.status != "bump"):
                self.oldstatus = self.status
            self.status = "bump"
            
            explorerhat.motor.one.stop()
            explorerhat.motor.two.stop()
            time.sleep(0.2)
            explorerhat.motor.one.backward()
            explorerhat.motor.two.backward()
            time.sleep(0.7)
            
            if (explorerhat.analog.one.read() < explorerhat.analog.two.read()): 
                explorerhat.motor.one.forward()
                explorerhat.motor.two.backward()
            else:
                explorerhat.motor.one.backward()
                explorerhat.motor.two.forward()
                
            time.sleep(0.5)
            
            self.do_command(self.oldstatus)
            
if __name__ == '__main__':
    cherrypy.quickstart(RobotServer("forward"), config="app.conf")
    
    
    
