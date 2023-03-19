class simulation_proxy:
def __init__(self, robot, env, obj):
self.robot = robot
self.env = env
self.obj = obj
distmax = 200
dt = 1
        
def avancer(self, vitesse):
self.robot.set_vitesse(vitesse, vitesse)
self.env.avancer_robot(robot, dt)
    
def tournerD(self, vitesse):
self.robot.set_vitesse(vitesse, -vitesse)
    
def tournerG(self, vitesse):
self.robot.set_vitesse(-vitesse, vitesse)
        
def capter(self):
''' retourne la distance par rapport au mur/obstacle '''
return self.robot.capteur(env, distmax, obj)
	

def stop(self):
self.robot.set_vitesse(0, 0)
        
class realite_proxy:
def __init__(self, robot):
self.robot = robot
        
def avancer(self, vitesse):
self.robot.set_motor_dps(self, self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT, vitesse)
    
def tournerD(self, vitesse):
self.robot.set_motor_dps(self, self.robot.MOTOR_RIGHT, vitesse)
self.robot.set_motor_dps(self, self.robot.MOTOR_LEFT, -vitesse)

def tournerG(self, vitesse):
self.robot.set_motor_dps(self, self.robot.MOTOR_RIGHT, -vitesse)
self.robot.set_motor_dps(self, self.robot.MOTOR_LEFT, vitesse)
    
def capter(self):
return self.robot.get_distance()

def stop(self):
self.robot.stop()
