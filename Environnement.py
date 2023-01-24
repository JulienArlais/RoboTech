import msvcrt 
import numpy as np

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
        self.afficher()
        print("\n")