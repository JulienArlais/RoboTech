import unittest
import numpy as np
from module.module_projet import Roue, Objet, Robot, Environnement

class TestRoue(unittest.TestCase):

	def setUp(self):
		self.r1 = Roue(90, 1)
		self.r2 = Roue(90, 1)

class TestObjet(unittest.TestCase):

	def setUp(self):
		self.o1 = Objet(0, 0, 0, 0, 2)
		self.o2 = Objet(2, 2, 0, 0, 1)

class TestRobot(unittest.TestCase):

	def setUp(self):
		self.rob = Robot(5, 6, 0, 3, Roue(90, 1), Roue(90, 1))
	
	def test_tourner(self):
		self.rob.tourner(47)
		self.assertEqual(self.rob.theta, np.radians(47))

class TestEnvironnement(unittest.TestCase):
		
	def setUp(self):
		self.env = Environnement(20, 20, 1)
		self.rob = Robot(0, 0, 0, 3, Roue(90, 1), Roue(90, 1))
		self.obj = Objet(4, 2, 0, 0, 2)

	def test_generer_obstacles(self):
		self.lo = self.env.generer_obstacles(3)
		self.assertEqual(len(self.lo), 3)
		for i in range(0, len(self.lo)):
			self.assertIsInstance(self.lo[i], Objet)

	def test_avancer_robot(self):
		self.env.avancer_robot(self.rob, 1)
		self.assertAlmostEqual(self.rob.x, np.radians(90))
		self.assertAlmostEqual(self.rob.y, 0)

	def test_collision_robot_objet(self):
		self.assertTrue(self.env.collision_robot_objet(self.rob, self.obj))

	def test_collision_entre_objets(self):
		self.assertTrue(self.env.collision_entre_objets(0, 0, 3, self.obj))

if __name__ == '__main__':
	unittest.main()