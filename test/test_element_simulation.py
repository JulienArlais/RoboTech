import unittest
import numpy as np
from module.element_simulation import Objet, Robot, Environnement, Simulation


class TestObjet(unittest.TestCase):

	def setUp(self):
		self.o1 = Objet(0, 0, 0, 0, 2)
		self.o2 = Objet(2, 2, 0, 0, 1)

class TestRobot(unittest.TestCase):

	def setUp(self):
		self.rob = Robot(5, 6, 0, 3, 5, 90, 90, 1)
		self.env = Environnement(20, 20, 1)
	
	def test_set_vitesse(self):
		self.rob.set_vitesse(78,79)
		self.assertEqual(self.rob.vitAngD, 78)
		self.assertEqual(self.rob.vitAngG, 79)

	def test_getXstep(self):
		self.assertAlmostEqual(self.rob.getXstep(1), np.radians(90))

	def test_getYstep(self):
		self.assertAlmostEqual(self.rob.getYstep(1), 0)

	def test_capteur(self):
		self.assertAlmostEqual(self.rob.capteur(self.env,20,[]), 12.0008839)

class TestEnvironnement(unittest.TestCase):
		
	def setUp(self):
		self.env = Environnement(20, 20, 1)
		self.rob = Robot(0, 0, 0, 3, 5, 90, 90, 1)
		self.obj = Objet(4, 2, 0, 0, 2)
	
	def test_generer_obstacles(self):
		self.lo = self.env.generer_obstacles(self.rob,3)
		self.assertEqual(len(self.lo), 3)
		for i in range(0, len(self.lo)):
			self.assertIsInstance(self.lo[i], Objet)

	def test_avancer_robot(self):
		self.env.avancer_robot(self.rob, 1)
		self.assertAlmostEqual(self.rob.x, np.radians(90))
		self.assertAlmostEqual(self.rob.y, 0)

	def test_collision(self):
		self.assertTrue(self.env.collision(0, 0, 3, self.obj))
		
class TestSimulation(unittest.TestCase):
    
    def setUp(self):
        self.env = Environnement(80, 80, 1)
        self.robot = Robot(40, 55.7, 0, 1.6, 3, 720, 720, 1)
        self.objets = self.env.generer_obstacles(self.robot, 5)
        self.simulation = Simulation(self.env, self.robot, self.objets)

if __name__ == '__main__':
	unittest.main()
