"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random
import matplotlib.pyplot as plt 

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
        for e, f in self.state, self.initial_state:
            if e != f:
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

    def convert(self):
        """ Permet de convertir une grille en tuple de sorte à ce que les noeuds de notre graphe soient hashable"""
        l=[]
        for i in range(self.n):
            l.append(self.state[i])
        return tuple(l)
    
    def creation_graphe(self):

        """ Permet à partir d'une position donnée de créer un une liste de noeuds de tout les états possibles
        de sorte à pouvoir créer le graph à l'aide des méthodes implémentées dans la méthode graphe """

        """ On crée également un dico de sorte à faciliter la création des edges plus tard """

        noeuds=[self.state]
        l=[self.state.convert()]
        dico={}
        while noeuds:
            tmp=noeuds.pop(0)
            if tmp.is_sorted():
                return l,dico
            else:
                for i in range(self.n):
                    for j in range(self.m):
                        tmp1=tmp.swap((i,j),(i,j+1))
                        tmp2=tmp.swap((i, j),(i+1,j))
                        dico[tmp.convert()].append(tmp1.convert())
                        dico[tmp.convert()].append(tmp2.convert())
                        if tmp1 not in noeuds:
                            noeuds.append(tmp1)
                            l.append(tmp1.convert())
                            tmp1.creation_graphe()
                        if tmp2 not in noeuds:
                            noeuds.append(tmp2)
                            tmp2.creation_graphe()
                            l.append(tmp2.convert())
            return l,dico







