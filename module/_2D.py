import tkinter as tk
from .toolbox import format, distance, create_circle


mult = 10 # multiplieur pour l'affichage graphique
dt = 0.05 

class GUI():
	def __init__(self, env, robot, objets):
		"""constructeur de l'interface graphique

		Args:
			env (Environnement): environnemment dans l'affichage
			robot (Robot): robot dans l'affichage
			objets (List[Objet]): liste des objets dans l'affichage
		"""
		self.environnement = env
		self.robot = robot
		self.objets = objets
		self.window = tk.Tk()
		self.window.title("Interface Graphique")
		self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult, height=self.environnement.height*mult)
		self.r = create_circle(self.robot.x*mult, self.robot.y*mult, self.robot.rayon*mult, self.canvas, "red")
		self.d = self.canvas.create_line(self.robot.x*mult, self.robot.y*mult, self.robot.x*mult+self.robot.getXstep(dt)*mult, self.robot.y*mult+self.robot.getYstep(dt)*mult, arrow=tk.LAST)
		for objet in self.objets:
			create_circle(objet.x*mult, objet.y*mult, objet.rayon*mult, self.canvas, "black")
		self.canvas.pack()

	def update(self):
		self.canvas.coords(self.d, self.robot.x*mult-self.robot.getXstep(dt)*mult, self.robot.y*mult-self.robot.getYstep(dt)*mult, 1.0*self.robot.x*mult, self.robot.y*mult)
		self.canvas.move(self.r, self.robot.getXstep(dt)*mult, self.robot.getYstep(dt)*mult)


