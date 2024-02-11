from grid import Grid

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

    def legal_move(self,x,y):
        i1,j1 = x
        i2,j2 =y
        return 0<=i1<self.grid.m and 0<=j1<self.grid.n and 0<=i2<self.grid.m and 0<=j2<self.grid.n and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1))
    
    @staticmethod
    def sumtuple(x,y):
        return (x[0]+y[0],x[1]+y[1])

  
    
    @staticmethod
    def move_needed(state1,state2):
        """
        A partir de 2 grilles qui différent d'un swap, on retrouve ce swap.
        """
        state1l = [list(elt) for elt in state1]
        state2l = [list(elt) for elt in state2]
        g1 = Grid(len(state1),len(state1[0]),state1l)
        g2 = Grid(len(state2),len(state2[0]),state2l)
        solv = Solver(g1)
        possible_moves = solv.possible_moves()
        for cell1,cell2 in possible_moves:
            g1.swap(cell1,cell2)
            if np.array_equal(g1.state,g2.state):
                return (cell1,cell2)
            g1.swap(cell1,cell2)
        raise Exception(f"Les deux grilles diffèreent de pllus qu'un swap {state1} et {state2}")

    
    def possible_moves(self):
        """
        On va récupèrer tout les mouvement possibles à partir d'une grille.
        
        On sait qu'a chaque étape, on a au total (4*2 + 2*(m-2)*3 + 2*(n-2)*3 + 4*(m-2)(n-2))/2 swaps possibles 
        Sortie : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')),.....]
        """
        possible_moves = []
        
        for i in range(0,self.grid.m):
            for j in range(0,self.grid.n):
                x = (i,j)
                move_close_to_x = [Solver.sumtuple(x,y) for y in directions]
            
                for t in move_close_to_x:
                    if self.legal_move(x,t) and (t,x) not in possible_moves:
                        possible_moves.append((x,t))
        return possible_moves

    def create_graph(self):
        """
        On crée un graphe où les noeuds représentent des états de la grille et il exitse une arête si les deux états
        son reliés par un swap legal
        
        Sortie : Objet Graph
        """
        g = Graph()
        possibles_moves = self.possible_moves()
        memory = copy.deepcopy(self.grid.state) #On retient l'état de la grille de sorte à le remettre à la fin de la fonction

        for swap1,swap2 in possibles_moves :
            non_mutable_state = self.grid.hashable_state()
            for cell1,cell2 in possibles_moves:
                self.grid.swap(cell1,cell2)
                non_mutable_new_state = self.grid.hashable_state()
                if (non_mutable_state,non_mutable_new_state) not in g.edges or (non_mutable_new_state,non_mutable_state) not in g.edges: 
                        g.add_edge(non_mutable_state,non_mutable_new_state)
                self.grid.swap(cell1,cell2) #on refait le changement

            self.grid.swap(swap1,swap2)
            non_mutable_state = self.grid.hashable_state()
        
        self.grid.state = memory
        return g 

    def get_solution_graphe(self):
        """
        On trouve le chemin le plus court dans le graphe construit précedemment
        On récupére la liste des swaps effectués 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        g = self.build_graph()
        src = self.grid.hashable_state()
        goal = Grid(self.grid.m,self.grid.n)
        dst = goal.hashable_state()
        etats_successifs = g.bfs(src,dst)
        if etats_successifs == None :
            return None
        #On a obtenu la liste des états succesifs de la grille 
        #On va maintenant récupérer la séquence de swaps qui ont été faits à partir de cette liste
        chemin = []
        for i in range(0,len(etats_successifs)-1):
            state1,state2 = etats_succesifs[i],etats_successifs[i+1]
            move_needed = Solver.move_needed(state1,state2)
            chemin.append(move_needed)
        return chemin 



