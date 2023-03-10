import tkinter as tk
from .toolbox import format, distance, create_circle
from .constante import dt
from .constante import mult 



class GUI():
	def __init__(self, env, robot, objets):
		"""constructeur de l'interface graphique

		Args:
			env (Environnement): environnemment dans l'affichage
			robot (Robot): robot dans l'affichage
			objets (List[Objet]): liste des objets dans l'affichage
		"""
		self.environnement = env
		scale = self.environnement.scale
		self.robot = robot
		self.objets = objets
		self.window = tk.Tk()
		self.window.title("Interface Graphique")
		self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult*scale, height=self.environnement.height*mult*scale)
		self.r = create_circle(self.robot.x*mult**scale, self.robot.y*mult**scale, self.robot.rayon*mult*env.scale, self.canvas, "red")
		self.d = self.canvas.create_line(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.x*mult*scale+self.robot.getXstep(dt)*mult*scale, self.robot.y*mult*scale+self.robot.getYstep(dt)*mult*scale, arrow=tk.LAST)
		for objet in self.objets:
			create_circle(objet.x*mult*scale, objet.y*mult*scale, objet.rayon*mult*scale, self.canvas, "black")
		self.canvas.pack()

	def update(self):
		scale = self.environnement.scale
		create_circle(self.robot.x*mult*scale, self.robot.y*mult*scale, 1, self.canvas, "black")
		self.canvas.delete(self.r)
		self.r = create_circle(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.rayon*mult*scale, self.canvas, "red")
		self.canvas.delete(self.d)
		self.d = self.canvas.create_line(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.x*mult*scale+self.robot.getXstep(dt)*mult*scale, self.robot.y*mult*scale+self.robot.getYstep(dt)*mult*scale, arrow=tk.LAST)
		
