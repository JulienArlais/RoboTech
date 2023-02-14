import unittest
from module.element_simulation import Robot, Environnement, Objet
from projet import Simulation


class TestSimulation(unittest.TestCase):
    
    def setUp(self):
        self.env = Environnement(80, 80, 1)
        self.robot = Robot(40, 55.7, 0, 1.6, 720, 720, 1)
        self.objets = self.env.generer_obstacles(self.robot, 5)
        self.simulation = Simulation(self.env, self.robot, self.objets)

if __name__ == '__main__':
    unittest.main()
