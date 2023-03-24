import time
import math
from easygopigo3 import EasyGoPiGo3,Servo,DistanceSensor,MotionSensor
import picamera
from io import BytesIO
from di_sensors import distance_sensor as ds_sensor
from di_sensors import  inertial_measurement_unit as imu
import threading
from collections import deque
import numpy as np

class Robot2IN013:
	""" 
	Classe d'encapsulation du robot et des senseurs.
	Constantes disponibles : 
	LED (controle des LEDs) :  LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI
	MOTEURS (gauche et droit) : MOTOR_LEFT, MOTOR_RIGHT
	et les constantes ci-dessous qui definissent les elements physiques du robot
	"""

	WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
	WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
	WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
	WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)

	def __init__(self,nb_img=10,fps=25,resolution=(640,480),servo_port="SERVO1"):
		""" 
		    Initialise le robot
		    :resolution: resolution de la camera
		"""

		self._gpg= EasyGoPiGo3()
		self.fps=fps
		self._img_queue = None
		self.nb_img = nb_img
		self.resolution = resolution
		self.servo = None
		try:
		    self.servo = Servo(servo_port,self._gpg)
		except Exception as e:
		       pass
		try:
		    self.distanceSensor = ds_sensor.DistanceSensor()
		except Exception as e:
		    print("Distance Sensor not found",e)
		try:
		    self.imu = imu.inertial_measurement_unit()
		except Exception as e:
		    print("IMU sensor not found",e)
		self._gpg.set_motor_limits(self._gpg.MOTOR_LEFT+self._gpg.MOTOR_RIGHT,0)
		self._recording = False
		self._thread = None
		self.start_recording()


	def stop(self):
		""" Arrete le robot """
		pass

	def get_image(self):
		pass

	def get_images(self):
		pass

	def set_motor_dps(self, port, dps):
		"""
		Fixe la vitesse d'un moteur en nombre de degres par seconde
		:port: une constante moteur,  MOTOR_LEFT ou MOTOR_RIGHT (ou les deux MOTOR_LEFT+MOTOR_RIGHT).
		:dps: la vitesse cible en nombre de degres par seconde
		"""
		pass

	def get_motor_position(self):
		"""
		Lit les etats des moteurs en degre.
		:return: couple du  degre de rotation des moteurs
		"""
		pass

	def offset_motor_encoder(self, port, offset):
		"""
		Fixe l'offset des moteurs (en degres) (permet par exemple de reinitialiser a 0 l'etat 
		du moteur gauche avec offset_motor_encode(self.MOTOR_LEFT,self.read_encoders()[0])
		
		:port: un des deux moteurs MOTOR_LEFT ou MOTOR_RIGHT (ou les deux avec +)
		:offset: l'offset de decalage en degre.
		Zero the encoder by offsetting it by the current position
		"""
		pass

	def get_distance(self):
		"""
		Lit le capteur de distance (en mm).
		:returns: entier distance en millimetre.
		    1. L'intervalle est de **5-8,000** millimeters.
		    2. Lorsque la valeur est en dehors de l'intervalle, le retour est **8190**.
		"""
		pass

	def servo_rotate(self,position):
		"""
		Tourne le servo a l'angle en parametre.
		:param int position: Angle de rotation, de **0** a **180** degres, 90 pour le milieu.
		"""
		pass

	def start_recording(self):
		pass

	def _stop_recording(self):
		pass
		
	def _start_recording(self):
		pass

	def __getattr__(self,attr):
		""" Méthodes héritées de GPG : 
		* set_led(self, led, red = 0, green = 0, blue = 0) 
		    Allume une led.
		    
		    :led: une des constantes LEDs (ou plusieurs combines avec +) : LED_LEFT_EYE, LED_RIGHT_EYE, LED_LEFT_BLINKER, LED_RIGHT_BLINKER, LED_WIFI.
		    :red: composante rouge (0-255)
		    :green:  composante verte (0-255)
		    :blue: composante bleu (0-255)
		"""
		pass
