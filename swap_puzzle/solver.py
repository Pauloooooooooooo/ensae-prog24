from grid import Grid
from graph import Graph
import heapq
import random
import copy
from itertools import permutations
import numpy as np

directions=[(-1,0),(1,0),(0,1),(0,-1)]
class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,m,n,ini):
        """
        On a décidé de considérer la classe Solver comme une classe enfant de la classe Grid.
        Ainsi, à chaque variable de type Solver, sera automatiquement associée une grille.
        """
        Grid.__init__(self,m,n,ini)
        self.barriers = []

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
            grid = Solver(m, n, initial_state)
        return grid

    def final(self):
        return Grid(self.m,self.n)

    def search(self, elt):
        """
        Fonction qui recherche dans la grille les coordonnées de l'élément cherché

        Args:
            elt : int
        """
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == elt:
                    return (i,j)

    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution
        #  returned.
        S = []
        for i in range(1, self.n*self.m +1):    #on replace les nombres à leurs places dans l'ordre croissant du 1 au n*m ème
            l,c = self.search(i)                #on cherche tout d'abord la place de l'élément i dans la grille
            lf = (i-1)//self.n                  #on calcule la place finale que i doit obtenir
            if i%self.n == 0:
                cf = self.n - 1
            else:
                cf = i%self.n - 1
            while cf != c:                      #on commence par replacer i dans sa colonne finale (on commence par les colonnes afin 
                if cf < c:                      # de ne pas déplacer un élément qui serait déjà à sa place)
                    self.swap((l,c),(l,c-1))
                    S.append(((l,c),(l,c-1)))
                    c = c-1
                else:
                    self.swap((l,c),(l,c+1))
                    S.append(((l,c),(l,c+1)))
                    c += 1
            while lf != l:                      #Puis, on attribue à i sa ligne finale
                if lf < l:
                    self.swap((l,c),(l-1,c))
                    S.append(((l,c),(l-1,c)))
                    l = l-1
                else:
                    self.swap((l,c),(l+1,c))
                    S.append(((l,c),(l+1,c)))
                    l += 1
        return S, self.is_sorted()              #On renvoie la liste des swaps effectués et on vérifie par la même occasion que la grille est bien triée

        """
        Q.3 : 
        La complexité de la fonction get_solution est en O([n*m]**2)
        Estimation du nombre de swaps ==> A chaque tour de boucle (boucle for), pour un élément i fixé, on effectue abs(cf[i] - c[i]) + abs(lf[i] - l[i]) swaps,
        en notant cf[i] et lf[i] (resp c[i] et l[i]) la colonne et la ligne finales de i (la colonne et la ligne initiales de i).
        Ainsi, nb_tot_swaps = SOMME(i : 1 -> n*m) [abs(cf[i]-c[i]) + abs(lf[i] - l[i])]
        """

        """_
        On peut se convaincre grâce à des exemples simples que la longueur de chemins obtenue n'est pas optimale.
        """
    def tuple_to_list(t):
        return list(list(e) for e in t)

    def legal_move(self,x,y):
        i1,j1 = x
        i2,j2 =y
        return 0<=i1<self.m and 0<=j1<self.n and 0<=i2<self.m and 0<=j2<self.n and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1))
    
    @staticmethod
    def sumtuple(x,y):
        return (x[0]+y[0],x[1]+y[1])
    
    @staticmethod
    def move_needed(state1,state2):
        """
        A partir de 2 grilles qui différent d'un swap, on retrouve ce swap.
        """
        l1 = [list(elt) for elt in state1]
        l2 = [list(elt) for elt in state2]
        g1 = Solver(len(state1),len(state1[0]),l1)
        g2 = Solver(len(state2),len(state2[0]),l2)
        possible_moves = g1.possible_moves()
        for cell1,cell2 in possible_moves:
            g1.swap(cell1,cell2)
            if np.array_equal(g1.state,g2.state):
                return (cell1,cell2)
            g1.swap(cell1,cell2)
        raise Exception(f"Les deux grilles diffèrent de plus qu'un swap {state1} et {state2}")

    
    def possible_moves(self):
        """
        On va récupèrer tout les mouvement possibles à partir d'une grille.
        
        On sait qu'a chaque étape, on a au total (4*2 + 2*(m-2)*3 + 2*(n-2)*3 + 4*(m-2)(n-2))/2 swaps possibles 
        Sortie : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')),.....]
        """
        possible_moves = []
        for i in range(0,self.m):
            for j in range(0,self.n):
                x = (i,j)
                move_close_to_x = [Solver.sumtuple(x,y) for y in directions]
            
                for t in move_close_to_x:
                    if (self.legal_move(x,t)) and ((t,x) not in possible_moves) and ((x,t) not in self.barriers) and ((t,x) not in self.barriers):
                        possible_moves.append((x,t))
        return possible_moves

    def generate_possible_states(self):
        """
        Generates all possible states of the grid.

        Returns:
        --------
        states: set
            A set containing all possible states of the grid.
        """
        states = set()  # Initialize an empty set to store unique grid states
        cells = [(i, j) for i in range(self.m) for j in range(self.n)]  # Get all cell positions
        permutations_cells = permutations(cells) # Generate all permutations of cell positions
        # For each permutation, create a grid state and add it to the set of states
        for perm in permutations_cells:
            new_state = [[0 for _ in range(self.n)] for _ in range(self.m)]  # Initialize a new grid state
            for index, (i, j) in enumerate(perm):  # Assign numbers to cells based on the permutation
                new_state[i][j] = index + 1
            states.add(tuple(map(tuple, new_state)))  # Add the new state to the set of states
        return states
    
    def build_graph(self):
        g = Graph()
        all_states = self.generate_possible_states()
        for state in all_states:
            l = Solver.tuple_to_list(state)
            s = Solver(len(l),len(l[0]),l)
            previous = s.hashable_state()
            moves = s.possible_moves()
            for c1, c2 in moves:
                s.swap(c1,c2)
                g.add_edge(previous,s.hashable_state())
                s.swap(c1,c2)
        return g

    def get_solution_graph(self):
        """
        On trouve le chemin le plus court dans le graphe construit précedemment
        On récupére la liste des swaps effectués 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        g = self.build_graph()
        src = self.hashable_state()
        goal = Grid(self.m,self.n)
        dst = goal.hashable_state()
        etats_successifs = g.bfs(src,dst)
        if etats_successifs == None :
            return None
        #On a obtenu la liste des états succesifs de la grille 
        #On va maintenant récupérer la séquence de swaps qui ont été faits à partir de cette liste
        chemin = []
        for i in range(0,len(etats_successifs)-1):
            state1,state2 = etats_successifs[i],etats_successifs[i+1]
            move_needed = Solver.move_needed(state1,state2)
            chemin.append(move_needed)
        return chemin 

    def distance(self):
        dist=0
        l1 = [list(elt) for elt in self.state]
        l2 = [list(elt) for elt in self.final().state]
        for i in range(len(l1)):
            for j in range(len(l1[0])):
                if l1[i][j]!=l2[i][j]:
                    dist+=1
        return dist

    def manhattan_distance(self):
        d = 0
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] != self.final().state[i][j]:
                    final_i, final_j = divmod(self.state[i][j] - 1,len(self.state[0]))
                    d += abs(i - final_i) + abs(j - final_j)
        return d

    def Astar(self):
        curr=self
        chemin=[]
        cheminb =  []
        vus=[curr.hashable_state()]
        while  curr.is_sorted() == False:
            h=[]
            cpt = 0 #numéro d'ajout pour éviter les problèmes d'égalité et de comparaison entre Grille dans l'utilisation de heapq
            for elt in curr.possible_moves():
                cpt += 1
                L = [[curr.state[i][j] for j in range(len(curr.state[0]))] for i in range(len(curr.state))]
                neighbor = Solver(curr.m, curr.n, L)
                #neighbor = Solver(curr.m, curr.n, curr.state[:][:])
                neighbor.swap(elt[0],elt[1])
                if not (neighbor.hashable_state() in vus):
                    heapq.heappush(h,(neighbor.distance(),cpt,neighbor,elt))    #il compare non pas seulement le premier, mais aussi le deuxieme elem qui est un Solver 
                #print(h), print(neighbor.state)
            new=heapq.heappop(h)
            print(new[2].state)
            vus.append(new[2].hashable_state())
            chemin.append(new[3])
            curr=new[2]
        return chemin, curr.state

    def Astar_improved(self):
        curr=self
        chemin=[]
        cheminb =  []
        vus=[curr.hashable_state()]
        while  curr.is_sorted() == False:
            h=[]
            cpt = 0 #numéro d'ajout pour éviter les problèmes d'égalité et de comparaison entre Grille dans l'utilisation de heapq
            for elt in curr.possible_moves():
                cpt += 1
                L = [[curr.state[i][j] for j in range(len(curr.state[0]))] for i in range(len(curr.state))]
                neighbor = Solver(curr.m, curr.n, L)
                #neighbor = Solver(curr.m, curr.n, curr.state[:][:])
                neighbor.swap(elt[0],elt[1])
                if not (neighbor.hashable_state() in vus):
                    heapq.heappush(h,(neighbor.manhattan_distance(),cpt,neighbor,elt))    #il compare non pas seulement le premier, mais aussi le deuxieme elem qui est un Solver 
                #print(h), print(neighbor.state)
            new=heapq.heappop(h)
            #print(new[2].state)
            vus.append(new[2].hashable_state())
            chemin.append(new[3])
            curr=new[2]
        return chemin, curr.state



"""
    def create_graph(self):
      
        On crée un graphe où les noeuds représentent des états de la grille et il exitse une arête si les deux états
        son reliés par un swap legal
        
        Sortie : Objet Graph
      
        g = Graph()
        possibles_moves = self.generate_possible_states()
        memory = copy.deepcopy(self.state) #On retient l'état de la grille de sorte à le remettre à la fin de la fonction

        for swap1,swap2 in possibles_moves :
            non_mutable_state = self.hashable_state()
            for cell1,cell2 in possibles_moves:
                self.swap(cell1,cell2)
                non_mutable_new_state = self.hashable_state()
                if (non_mutable_state,non_mutable_new_state) not in g.edges or (non_mutable_new_state,non_mutable_state) not in g.edges: 
                        g.add_edge(non_mutable_state,non_mutable_new_state)
                self.swap(cell1,cell2) #on refait le changement

            self.swap(swap1,swap2)
            non_mutable_state = self.hashable_state()
 
        self.state = memory
        return g 
"""


                





