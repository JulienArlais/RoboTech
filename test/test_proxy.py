import unittest
import random
import numpy as np
from module.modele.element_simulation import Robot, Environnement
from module.modele.proxy import Proxy_Virtuel


class TestProxyVirtuel(unittest.TestCase):

	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.pv = Proxy_Virtuel(self.r, self.e)
		self.random_vitesse = random.randint(45, 90)
		self.random_dps = random.randint(-45, 45)
		
	def test_proxy(self):
		self.assertIsInstance(self.pv.robot, Robot)
		self.assertIsInstance(self.pv.env, Environnement)
		self.assertEqual(self.pv.dist_roue, self.r.dist_roue)
		self.assertEqual(self.pv.rayon, self.r.rayon)
		self.assertEqual(self.pv.rayon_roue, self.r.rayon_roue)
		self.assertEqual(self.pv.distance_parcourue, 0)
		self.assertEqual(self.pv.angle_parcouru, 0)
		self.assertEqual(self.pv.last_update, 0)

	def test_set_vitesse(self):
		self.pv.set_vitesse(self.random_vitesse, self.random_vitesse)
		self.assertEqual(self.r.vitAngD, self.random_vitesse/20)
		self.assertEqual(self.r.vitAngG, self.random_vitesse/20)

	def test_reset_distance(self):
		self.pv.distance_parcourue = 50
		self.assertEqual(self.pv.distance_parcourue, 50)
		self.pv.reset_distance()
		self.assertEqual(self.pv.distance_parcourue, 0)

	def test_reset_angle(self):
		self.pv.angle_parcouru = 90
		self.assertEqual(self.pv.angle_parcouru, 90)
		self.pv.reset_angle()
		self.assertEqual(self.pv.angle_parcouru, 0)

	def test_get_vitAng(self):
		self.pv.set_vitesse(self.random_vitesse, self.random_vitesse)
		self.assertEqual(self.pv.get_vitAng(), (self.random_vitesse/20, self.random_vitesse/20))

	def test_tourner(self):
		self.pv.tourner(self.random_dps)
		delta = (self.pv.dist_roue * np.abs(self.random_dps))/self.pv.rayon_roue/2
		if self.random_dps > 0:
			self.assertEqual(self.r.vitAngG, delta/20)
			self.assertEqual(self.r.vitAngD, -delta/20)
		else:
			self.assertEqual(self.r.vitAngG, -delta/20)
			self.assertEqual(self.r.vitAngD, delta/20)

	def test_reset(self):
		self.pv.distance_parcourue = 50
		self.pv.angle_parcouru = 90
		self.pv.reset()
		self.assertEqual(self.pv.distance_parcourue, 0)
		self.assertEqual(self.pv.angle_parcouru, 0)

if __name__ == '__main__':
	unittest.main()