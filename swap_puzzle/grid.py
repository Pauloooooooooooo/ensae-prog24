"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random
import matplotlib.pyplot as plt 
import copy

#import pygame as pg 
BLOCK_SIZE=200
BLACK=(0,0,0)
WHITE=(255,255,255)
directions=[(-1,0),(1,0),(0,1),(0,-1)]
class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as git push.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j] != i*self.n + (j+1):
                    return False
        return True

    def swap(self, cell1, cell2):
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        i1, j1 = cell1
        i2, j2 = cell2
        assert (i1 == i2 and abs(j1-j2) == 1) or (j1 == j2 and abs(i1-i2) == 1)
        self.state[i1][j1], self.state[i2][j2] = self.state[i2][j2], self.state[i1][j1]  

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        for e in cell_pair_list:
            c1, c2 = e 
            self.swap(c1,c2)

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid

    def trac(self):
        for i in range(self.n):
            for j in range(self.m):
                plt.plot([i, i+1], [j, j], color='black')
                plt.plot([i, i], [j, j+1], color='black')

        for k in range(self.m):
            plt.plot([k, k+1], [self.n, self.m], color='black')

        for k in range(self.n):
            plt.plot([self.m, self.m], [k, k+1], color='black')


        for i in range(self.n):
            for j in range(self.m):
                plt.text(i + 0.5, j + 0.5, str(self.state[j][i]),color='black', ha='center', va='center', fontsize=12)

        plt.xlim(0, self.m)
        plt.ylim(0, self.n)
        plt.gca().invert_yaxis()
        plt.axis('off')

        plt.show()

    def hashable_state(self):
        """
        On obtient un état mutable d'une grille pour les noeuds du graphe
        """
        return tuple([tuple(inner_list) for inner_list in self.state])

    def create_barrier(self, diff):
        """ 
        Créer une barrière consiste pour une grille à retenir une liste de swaps qui seront interdits dans le jeu et donc
        enlevés des mouvements possibles
        """
        sommets = []
        barriers = []
        if self.m == 1 or self.n == 1:  #on vérifie que les grilles ne soient pas qu'une ligne ou une colonne, auquel cas le jeu 
            return barriers             #serait bloqué avec l'ajout d'une barrière
        for i in range(diff * 2):
            x, y = random.randint(1,self.m), random.randint(1,self.n)
            if not((x,y) in sommets):           #on choisit la case à laquelle on adjoint une barrière
                sommets.append((x,y))
                d = random.randint(0,3)         #on tire au hasard la direction qui sera bloquée (gauche, droite, haut, bas)
                if self.legal_move((x,y),directions[d]) :
                    xb, yb = Solver.sumtuple((x,y),directions[d])
                    sommets.append((xb,yb))
                    barriers.append(((x,y),(xb,yb)))
                    barriers.append(((xb,yb),(x,y)))
        return barriers

    def griddisplay(self):
        """
        Crée un affichage de la grille avec Pygame et permet à l'utilisateur d'interagir pour déplacer les cases.
        """
        pg.init()
        self.display = pg.display.set_mode((self.n * BLOCK_SIZE, self.m * BLOCK_SIZE))
        self.display.fill(WHITE)
        pg.display.set_caption("Swap Puzzle")
        font = pg.font.Font(None, 25)
        active_cell = None  
        while True:
            for event in pg.event.get():                  # On décide de quitter la fenêtre graphique
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:          # on obtient les coordonnées de la case cliquée
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    colonne = mouse_x // BLOCK_SIZE
                    ligne = mouse_y // BLOCK_SIZE
                    if 0 <= ligne < self.m and 0 <= colonne < self.n:
                        if active_cell is None:
                            active_cell = (ligne, colonne)                                                  # Si aucune case n'est sélectionnée, on sélectionne celle-ci
                        else:           
                            self.swapdisplay(active_cell, (ligne, colonne))
                            active_cell= None                                                         # on rénitialise la cellule active
            self.display.fill(WHITE)                                                                # on redéssine la grille avec les numéros 
            for i in range(self.m):
                for j in range(self.n):
                    left = j * BLOCK_SIZE
                    top = i * BLOCK_SIZE
                    pg.draw.rect(self.display, BLACK, pg.Rect(left, top, BLOCK_SIZE, BLOCK_SIZE), 5)
                    mid_top = top + (BLOCK_SIZE) / 2
                    mid_left = left + (BLOCK_SIZE) / 2
                    text = font.render(str(self.state[i][j]), True, BLACK)
                    self.display.blit(text, (mid_left - text.get_width() // 2, mid_top - text.get_height() // 2))
            pg.display.flip()

    
    def swapdisplay(self, coord_case1, coord_case2):
        font = pg.font.Font(None, 36) 
        message = font.render('Swap non légal !', True, (255, 255, 255))
        i1, j1 = coord_case1
        i2, j2 = coord_case2
        self.state[i1][j1], self.state[i2][j2] = self.state[i2][j2], self.state[i1][j1]
        if ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)):
            self.display.fill(WHITE)                                # on redéssine la grille ue fois l'échange fait
            font = pg.font.Font(None, 25)
            for i in range(self.m):
                for j in range(self.n):
                    left = j * BLOCK_SIZE
                    top = i * BLOCK_SIZE
                    pg.draw.rect(self.display, BLACK, pg.Rect(left, top, BLOCK_SIZE, BLOCK_SIZE), 5)
                    mid_top = top + (BLOCK_SIZE) / 2
                    mid_left = left + (BLOCK_SIZE) / 2
                    text = font.render(str(self.state[i][j]), True, BLACK)
                    self.display.blit(text, (mid_top, mid_left))
            pg.display.flip()
        else :
            self.display.blit(message,(100,100))


      






