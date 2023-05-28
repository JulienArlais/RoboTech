import unittest
from module.modele.element_simulation import Robot, Environnement
from module.vue.affichage_2D import GUI


class TestGUI(unittest.TestCase):
	def setUp(self):
		self.e = Environnement(80, 80, 1)
		self.r = Robot(5, 6, 0, 3, 2, 1)
		self.gui = GUI(self.e, self.r)

	def test_gui(self):
		self.assertIsInstance(self.gui.environnement, Environnement)
		self.assertIsInstance(self.gui.robot, Robot)

if __name__ == '__main__':
	unittest.main()
