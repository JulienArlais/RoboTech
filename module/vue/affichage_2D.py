import tkinter as tk
import numpy as np
from ..toolbox import create_circle
from ..constante import mult

class GUI():
	def __init__(self, env, robot):
		"""constructeur de l'interface graphique
		Args:
			env (Environnement): environnemment dans l'affichage
			robot (Robot): robot dans l'affichage
		"""
		self.environnement = env
		scale = self.environnement.scale
		self.robot = robot

		self.window = tk.Tk()
		self.window.title("Interface Graphique")
		self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult*scale, height=self.environnement.height*mult*scale)
		x, y = self.robot.x*mult*scale, self.robot.y*mult*scale
		self.r = create_circle(x, y, self.robot.rayon*mult*scale, self.canvas, "red")
		self.d = self.canvas.create_line(x, y, x+self.robot.getXstep()*mult*scale, y+self.robot.getYstep()*mult*scale, arrow=tk.LAST, width=2)
		for objet in self.environnement.objets:
			create_circle(objet.x*mult*scale, objet.y*mult*scale, objet.rayon*mult*scale, self.canvas, "black")
		self.canvas.pack()

	def update(self):
		scale = self.environnement.scale
		x, y = self.robot.x*mult*scale, self.robot.y*mult*scale
		create_circle(x, y, 1, self.canvas, "black")
		self.canvas.delete(self.r)
		self.r = create_circle(x, y, self.robot.rayon*mult*scale, self.canvas, "red")
		self.canvas.delete(self.d)
		self.d = self.canvas.create_line(x, y, x+self.robot.getXstep()*mult*scale, y+self.robot.getYstep()*mult*scale, arrow=tk.LAST)