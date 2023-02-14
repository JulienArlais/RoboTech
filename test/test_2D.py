import unittest
import tkinter as tk
import sys
sys.path.append('$pwd')

from module.element_simulation import Roue, Objet, Robot, Environnement
from module.toolbox import format, distance
from module._2D import GUI


class TestGUI(unittest.TestCase):

    def setUp(self):
        self.env = Environnement(100, 100, 1)
        self.rob = Robot(50, 50, 50, self.env, 10, 5) 
        self.gui = GUI(self.env, self.rob, self.env.objets)


if __name__ == '__main__':
    unittest.main()
