from .constante import dt
import numpy as np
from .toolbox import distance
import cv2
from .camera import detect, BaliseException


class StrategieAvancerIRL(object):
    def __init__(self, distance, vitesse, robot_irl):
        """constructeur de la stratégie_avancer_IRL pour avancer d'une distance voulu

		Args:
			distance (float): distance
			vitesse (int): vitesse des roues ( degré par seconde )
			robot_irl (Robot réel): robot_irl
		"""
        self.distance = distance
        self.vitesse = vitesse
        self.robot_irl = robot_irl
        self.parcouruIRL = 0.
        self.lastUpdate = 0

    def update(self):
		"""itération de la stratégie
		"""
		if self.stop():
			return
		self.robot_irl.set_vitesse(self.vitesse, self.vitesse)
		self.parcouruIRL += self.robot_irl.dist_parcourue()
		x= self.robot_irl.distance_parcouruIRL() # A RETIRER PLUS TARD, UTILE POUR TESTER LA FCT


    def stop(self):
		"""condition d'arrêt

		Returns:
			boolean: arrêt ou non
		"""
		if (self.parcouruIRL >= self.distance):
			self.robot_irl.set_vitesse(0, 0)
			self.parcouruIRL = 0
			return True
		return False



   