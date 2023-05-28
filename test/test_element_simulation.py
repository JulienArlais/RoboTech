import unittest
import numpy as np
import random
from module.modele.element_simulation import Objet, Robot, Environnement, Simulation


class TestObjet(unittest.TestCase):

	def setUp(self):
		self.random_x = random.randint(0, 10)
		self.random_y = random.randint(0, 10)
		self.random_rayon = random.randint(0, 5)
		self.o = Objet(self.random_x, self.random_y, self.random_rayon)

	def test_objet(self):
		self.assertEqual(self.o.x, self.random_x)
		self.assertEqual(self.o.y, self.random_y)
		self.assertEqual(self.o.rayon, self.random_rayon)

class TestRobot(unittest.TestCase):

	def setUp(self):
		self.random_x = random.randint(0, 10)
		self.random_y = random.randint(0, 10)
		self.random_theta = random.randint(0, 360)
		self.random_rayon = random.randint(0, 5)
		self.random_dist_roue = random.randint(0, 5)
		self.random_rayon_roue = random.randint(0, 5)
		self.r = Robot(self.random_x, self.random_y, self.random_theta, self.random_rayon, self.random_dist_roue, self.random_rayon_roue)

	def test_robot(self):
		self.assertEqual(self.r.x, self.random_x)
		self.assertEqual(self.r.y, self.random_y)
		self.assertEqual(self.r.theta, self.random_theta)
		self.assertEqual(self.r.rayon, self.random_rayon)
		self.assertEqual(self.r.dist_roue, self.random_dist_roue)
		self.assertEqual(self.r.rayon_roue, self.random_rayon_roue)
	
	def test_get_vitAng(self):
		self.assertEqual(self.r.vitAngD, 0)
		self.assertEqual(self.r.vitAngG, 0)

	def test_getXstep(self):
		self.assertAlmostEqual(self.r.getXstep(), 0)

	def test_getYstep(self):
		self.assertAlmostEqual(self.r.getYstep(), 0)

	#def test_get_distance(self):

class TestEnvironnement(unittest.TestCase):
		
	def setUp(self):
		self.r = Robot(2, 2, 0, 3, 2, 1)
		self.random_width = random.randint(50, 100)
		self.random_height = random.randint(50, 100)
		self.e = Environnement(self.random_width, self.random_height, 1)

	def test_environnement(self):
		self.assertEqual(self.e.width, self.random_width)
		self.assertEqual(self.e.height, self.random_height)
		self.assertEqual(len(self.e.objets), 0)
	
	def test_generer_un_obstacle(self):
		self.e.generer_un_obstacle(self.r)
		self.assertIsInstance(self.e.objets[0], Objet)

	def test_generer_obstacles(self):
		self.e.generer_obstacles(self.r, 2)
		self.assertEqual(len(self.e.objets), 2)
		for i in range(0, len(self.e.objets)):
			self.assertIsInstance(self.e.objets[i], Objet)

	def test_collision(self):
		self.assertFalse(self.e.collision(2, 2, 3))
		
class TestSimulation(unittest.TestCase):
	
	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.s = Simulation(self.e, self.r)

	def test_simulation(self):
		self.assertIsInstance(self.s.environnement, Environnement)
		self.assertIsInstance(self.s.robot, Robot)

if __name__ == '__main__':
	unittest.main()
