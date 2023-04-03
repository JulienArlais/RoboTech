import tkinter as tk
from .toolbox import format, distance, create_circle
from .constante import dt
from .constante import mult


class GUI():
    def __init__(self, env, robot):
        """constructeur de l'interface graphique
        Args:
            env (Environnement): environnement dans l'affichage
            robot (Robot): robot dans l'affichage
            objets (List[Objet]): liste des objets dans l'affichage
        """
        self.environnement = env
        scale = self.environnement.scale
        self.robot = robot
        self.window = tk.Tk()
        self.window.title("Interface Graphique")
        self.canvas = tk.Canvas(self.window, width=self.environnement.width*mult*scale, height=self.environnement.height*mult*scale)
        self.r = create_circle(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.rayon*mult*scale, self.canvas, "#FD6C9E")
        self.r_led1 = create_circle(self.robot.x*mult*scale - self.robot.rayon*mult*scale/2, self.robot.y*mult*scale, self.robot.rayon*mult*scale/4, self.canvas, "black")
        self.r_led2 = create_circle(self.robot.x*mult*scale + self.robot.rayon*mult*scale/2, self.robot.y*mult*scale, self.robot.rayon*mult*scale/4, self.canvas, "black")
        self.d = self.canvas.create_line(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.x*mult*scale+self.robot.getXstep(dt)*mult*scale, self.robot.y*mult*scale+self.robot.getYstep(dt)*mult*scale, arrow=tk.LAST)
        for objet in self.environnement.objets:
            create_circle(objet.x*mult*scale, objet.y*mult*scale, objet.rayon*mult*scale, self.canvas, "#FFA500")
        
        #prise en compte de l'emeteur qui sera de couleur verte

        for emt in self.environnement.éméteur:
            create_circle(emt.x*mult*scale, emt.y*mult*scale, emt.rayon*mult*scale, self.canvas, "green")


        self.canvas.pack()

    def update(self):
        scale = self.environnement.scale
        create_circle(self.robot.x*mult*scale, self.robot.y*mult*scale, 1, self.canvas, "red")
        self.canvas.delete(self.r)
        self.r = create_circle(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.rayon*mult*scale, self.canvas, "#FD6C9E")
        self.canvas.delete(self.r_led1)
        self.r_led1 = create_circle(self.robot.x*mult*scale - self.robot.rayon*mult*scale/2, self.robot.y*mult*scale, self.robot.rayon*mult*scale/4, self.canvas, "red" if self.robot.led1 else "black")
        self.canvas.delete(self.r_led2)
        self.r_led2 = create_circle(self.robot.x*mult*scale + self.robot.rayon*mult*scale/2, self.robot.y*mult*scale, self.robot.rayon*mult*scale/4, self.canvas, "blue" if self.robot.led2 else "black")
        self.canvas.delete(self.d)

        #prise en compte du tracage:
        if self.robot.abaisser==True: #Condition du tracer de ligne
            self.d = self.canvas.create_line(self.robot.x*mult*scale, self.robot.y*mult*scale, self.robot.x*mult*scale+self.robot.getXstep(dt)*mult*scale, self.robot.y*mult*scale+self.robot.getYstep(dt)*mult*scale, arrow=tk.LAST)
