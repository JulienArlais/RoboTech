import unittest
import random
from module.modele.element_simulation import Robot, Environnement
from module.modele.proxy import Proxy_Virtuel
from module.controleur.controleur import StrategieAvance, StrategieAngle, StrategieArretMur, StrategieSeq


class TestStrategieAvance(unittest.TestCase):

	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.pv = Proxy_Virtuel(self.r, self.e)
		self.random_vitesse = random.randint(50, 100)
		self.sa = StrategieAvance(0, self.random_vitesse, self.pv)
		
	def test_stavance(self):
		self.assertIsInstance(self.sa.proxy, Proxy_Virtuel)
		self.assertEqual(self.sa.distance, 0)
		self.assertEqual(self.sa.vitesse, self.random_vitesse)

class TestStrategieAngle(unittest.TestCase):

	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.pv = Proxy_Virtuel(self.r, self.e)
		self.random_dps = random.randint(15, 45)
		self.sa = StrategieAngle(0, self.random_dps, self.pv)
		
	def test_stangle(self):
		self.assertIsInstance(self.sa.proxy, Proxy_Virtuel)
		self.assertEqual(self.sa.angle, 0)
		self.assertEqual(self.sa.dps, self.random_dps)

class TestStrategieArretMur(unittest.TestCase):

	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.pv = Proxy_Virtuel(self.r, self.e)
		self.random_vitesse = random.randint(50, 100)
		self.sa = StrategieArretMur(0, self.random_vitesse, self.pv)
		
	def test_starret(self):
		self.assertIsInstance(self.sa.proxy, Proxy_Virtuel)
		self.assertEqual(self.sa.dist, 0)
		self.assertEqual(self.sa.vitesse, self.random_vitesse)

class TestStrategieSeq(unittest.TestCase):

	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.pv = Proxy_Virtuel(self.r, self.e)
		st1 = StrategieAvance(0, 0, self.pv)
		st2 = StrategieAngle(0, 0, self.pv)
		st3 = StrategieArretMur(0, 0, self.pv)
		self.ss = StrategieSeq([st1, st2, st3], self.pv)
		
	def test_stseq(self):
		self.assertIsInstance(self.ss.proxy, Proxy_Virtuel)
		self.assertIsInstance(self.ss.liste[0], StrategieAvance)
		self.assertIsInstance(self.ss.liste[1], StrategieAngle)
		self.assertIsInstance(self.ss.liste[2], StrategieArretMur)
		self.assertEqual(self.ss.indlist, 0)

if __name__ == '__main__':
	unittest.main()