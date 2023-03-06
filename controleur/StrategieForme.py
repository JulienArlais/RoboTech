from module.constante import dt
import numpy as np
from module.toolbox import distance

class StrategieForme():
	def __init__(self, liste):
		"""Constructeur de la stratégie Forme

		Args:
			liste : liste de stratégies
		"""
		self.liste = liste
		self.indlist = 0
		
	def update(self):
		if self.liste[self.indlist].stop():
			self.indlist += 1
			if self.stop():
				return
		self.liste[self.indlist].update()
		
	def stop(self):
		return self.indlist >= len(self.liste)

	def run(self):
		while not self.stop():
			self.update()
