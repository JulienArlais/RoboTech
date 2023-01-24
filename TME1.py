import msvcrt 
import numpy as np

class InvalidMoveException(Exception):
    def __init__(self, message):
        self.message = message
        
class TooMuchObstacleException(Exception):
    def __init__(self, message):
        self.message = message


class Environnement:
    def __init__(self, width, height): 
        # prendre width et height >= 3 
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        for i in range(width):
            for j in range(height):
                #self.grid[i][j] = '.' 
                if i==0 or j==0 or i==self.width-1 or j==self.height-1:
                    self.grid[i][j] = 'X'
                   
    def afficher(self):
        for i in range(self.width):
            for j in range(self.height):
                print(self.grid[i][j], end=' ')
            print()
    
    def obstacle(self):
        print("\n")
        nb_obstacles = int(input("Combien ya t-il d'obstacles dans la pièces ? "))
        if (nb_obstacles > (self.width-2)*(self.height-2)-1):
            raise InvalidMoveException("Le nombre d'obstacles est trop important")
        print("\n")
        i = 0
        while (i < nb_obstacles):
            x = np.random.randint(1, self.width - 1)
            y = np.random.randint(1, self.height - 1)
            if (self.grid[x][y] != 'X') and (self.grid[x][y] != 'R'):
                self.grid[x][y] = 'X'
                i+=1
        environment.afficher()
        print("\n")

class Capteur:
    def __init__(self, portee, x, y): 
        self.portee = portee
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def distance(self, x, y): 
        # donne la distance par rapport aux coordonnées (x, y), lève une exception si impossible
        dist = (int)(np.sqrt(np.square(x-self.x)+np.square(y-self.y)))
        if (dist > self.portee):
            raise InvalidMoveException("Pas assez de portée")
        else:
            return dist


class Robot:
    def __init__(self, environnement, portee): 
        # coordonnées x et y aléatoires dans [1, width-2] et [1, height-2]
        self.x = np.random.randint(1, environnement.width - 2)
        self.y = np.random.randint(1, environnement.height - 2)
        self.environnement = environnement
        self.capteur = Capteur(portee, self.x, self.y)
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
        self.capteur.setX(self.x)
        self.y = y
        self.capteur.setY(self.x)
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
            direction = bytes.decode(msvcrt.getch())
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
                

#EXEMPLE DE SIMULATION#

environment = Environnement(20, 20) 
robot=Robot(environment, 7)

environment.afficher()
environment.obstacle()


robot.direction=input("Donner une direction au robot ")
robot.reculer()

robot.placer(18,18) 

robot.auto_move()

robot.carre()

# place le robot en (1, 1) et donne sa distance entre les coordonnées (18, 18), lève une exception car le capteur n'a pas assez de portée
robot.placer(1,1) 

