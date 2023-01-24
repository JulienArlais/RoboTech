from Environnement import Environnement
import numpy as np
import getch 
from Exceptions import *


class Robot:
    def __init__(self, environnement): 
        # coordonnées x et y aléatoires dans [1, width-1[ et [1, height-1[
        self.x = np.random.randint(1, environnement.width - 1)
        self.y = np.random.randint(1, environnement.height - 1)
        self.environnement = environnement
        self.direction = "haut" # Le robot est dirigé vers le haut par défaut 
        self.environnement.grid[self.x][self.y] = "R"

    def placer(self, x, y): 
        # place le robot aux coordonnées (x,y) si c'est possible sinon lève une exception
        # prend x dans [1,width-2], et y dans [1, height-2]
        if (self.environnement.grid[x][y] == "X"):
            raise InvalidMoveException("Obstacle détecté")
            return
        self.environnement.grid[self.x][self.y] = "."
        self.x = x
        self.y = y
        self.environnement.grid[self.x][self.y] = "R"
        self.environnement.afficher()
        print("\n")          

    def tourner(self,cote):
        # permet au robot de tourner sur soi-même de 90 degrés vers la droite ou la gauche
        if cote == "droite":
            if self.direction == "haut":
                    self.direction = "droite"
            elif self.direction == "droite":
                    self.direction = "bas"
            elif self.direction == "bas":
                    self.direction = "gauche"
            elif self.direction == "gauche":
                    self.direction = "haut"
        elif cote == "gauche":
            if self.direction == "haut":
                    self.direction = "gauche"
            elif self.direction == "gauche":
                    self.direction = "bas"
            elif self.direction == "bas":
                    self.direction = "droite"
            elif self.direction == "droite":
                    self.direction = "haut"
        else:
            print("Direction non valide")

    def reculer(self):
        # permet au robot de reculer d'une case en fonction du dernier deplacement
        if self.direction == "haut":
            self.bas()
        elif self.direction == "bas":
            self.haut()
        elif self.direction == "gauche":
            self.droite()
        elif self.direction == "droite":
            self.gauche()
        else:
            print("Direction non valide")  
    
    def bas(self):
        # permet au robot de bouger d'une case vers le bas si possible sinon lève une exception
        if(self.environnement.grid[self.x+1][self.y] == "X"):
            raise InvalidMoveException("Obstacle détecté vers le bas")
        self.environnement.grid[self.x][self.y] = "."  # marque le déplacement précédent
        self.x += 1
        self.environnement.grid[self.x][self.y] = "R"  # met à jour la position actuelle du robot
        self.direction = "bas" # met à jour la direction
        self.environnement.afficher()
        print("\n")

    def haut(self):
        # permet au robot de bouger d'une case vers le haut si possible sinon lève une exception
        if(self.environnement.grid[self.x-1][self.y] == "X"):
            raise InvalidMoveException("Obstacle détecté vers le haut")
        self.environnement.grid[self.x][self.y] = "."  # marque le déplacement précédent
        self.x -= 1
        self.environnement.grid[self.x][self.y] = "R"  # met à jour la position actuelle du robot
        self.direction = "haut" # met à jour la direction
        self.environnement.afficher()
        print("\n")

    def gauche(self):
        # permet au robot de bouger d'une case vers la gauche si possible sinon lève une exception
        if (self.environnement.grid[self.x][self.y-1] == "X"):
            raise InvalidMoveException("Obstacle détecté vers la gauche")
        self.environnement.grid[self.x][self.y] = "."  # marque le déplacement précédent
        self.y -= 1
        self.environnement.grid[self.x][self.y] = "R"  # met à jour la position actuelle du robot
        self.direction = "gauche" # met à jour la direction
        self.environnement.afficher()
        print("\n")

    def droite(self):
        # permet au robot de bouger d'une case vers la droite si possible sinon lève une exception
        if (self.environnement.grid[self.x][self.y+1] == "X"):
            raise InvalidMoveException("Obstacle détecté vers la droite")
        self.environnement.grid[self.x][self.y] = "."  # marque le déplacement précédent
        self.y += 1
        self.environnement.grid[self.x][self.y] = "R"  # met à jour la position actuelle du robot
        self.direction = "droite" # met à jour la direction
        self.environnement.afficher()
        print("\n")        
    
    def auto_move(self):
        # fonction de déplacement en continue du robot 
        while True:
            direction = getch.getch()
            try:
                if direction == "z":
                    self.haut()
                elif direction == "s":
                    self.bas()
                elif direction == "q":
                    self.gauche()
                elif direction == "d":
                    self.droite()
                elif direction=="r":
                    self.reculer()
                elif direction=="c":
                    break
                else:
                    print("Direction non valide, veuillez réessayer")
            except InvalidMoveException as e:
                print(e)
                pass

    def carre(self):
        # trace un carré avec le robot, arrête le robot si un obstacle est sur le chemin
        dst=input("Entrez la distance du carré que vous voulez: ")
        distance=(int)(dst)
        try:
            for i in range(distance):
                self.droite()
            for i in range(distance):
                self.bas()
            for i in range(distance):
                self.gauche()
            for i in range(distance):
                self.haut()
        except InvalidMoveException:
            print("Obstacle détecté, replacez le robot")




