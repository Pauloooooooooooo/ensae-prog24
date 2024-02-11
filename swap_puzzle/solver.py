from grid import Grid

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,m,n,ini):
        Grid.__init__(self,m,n,ini)
        
    def search(self, elt):
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
        for i in range(1, self.n*self.m +1):
            l,c = self.search(i)
            lf = (i-1)//self.n 
            if i%self.n == 0:
                cf = self.n - 1
            else:
                cf = i%self.n - 1
            while cf != c:
                if cf < c:
                    self.swap((l,c),(l,c-1))
                    S.append(((l,c),(l,c-1)))
                    c = c-1
                else:
                    self.swap((l,c),(l,c+1))
                    S.append(((l,c),(l,c+1)))
                    c += 1
            while lf != l:
                if lf < l:
                    self.swap((l,c),(l-1,c))
                    S.append(((l,c),(l-1,c)))
                    l = l-1
                else:
                    self.swap((l,c),(l+1,c))
                    S.append(((l,c),(l+1,c)))
                    l += 1
        return S, self.is_sorted()


    def legal_move(self,x,y):
        i1,j1 = x
        i2,j2 =y
        return 0<=i1<self.grid.m and 0<=j1<self.grid.n and 0<=i2<self.grid.m and 0<=j2<self.grid.n and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1))
    
    @staticmethod
    def sumtuple(x,y):
        return (x[0]+y[0],x[1]+y[1])

    @staticmethod
    def find_place(mat,elt):
        for i, rows in enumerate(mat):
            if elt in rows:
                return i, rows.index(elt)

        return None
    
    @staticmethod
    def move_needed(state1,state2):
        """
        Giving 2 grid that differs from one swap, find the swap they have in common
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
        raise Exception(f"The 2 grids differs from more than 1 swap {state1} and {state2}")

    
    def possible_moves(self):
        """
        Return all possible_moves from a state
        
        To each state we have (4*2 + 2*(m-2)*3 + 2*(n-2)*3 + 4*(m-2)(n-2))/2 swaps possibles 
        Output : [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')),.....]
        """
        possible_moves = []
        
        for i in range(0,self.grid.m):
            for j in range(0,self.grid.n):
                x = (i,j)
                #print(x)
                move_close_to_x = [Solver.sumtuple(x,y) for y in directions]
                #print(move_close_to_x)
                for t in move_close_to_x:
                    if self.legal_move(x,t) and (t,x) not in possible_moves:
                        #print(f"On append {(x,t)}")
                        possible_moves.append((x,t))
        return possible_moves

    def build_graph(self):
        """
        On construit un graphe où les noeuds représentent des états de la grille et il exitse une arête si les deux états
        son reliés par un swap legal
        
        Sortie : Objet Graph
        """
        g = Graph()
        possibles_moves = self.possible_moves()
        memory = copy.deepcopy(self.grid.state) #Remember the state for putting back the state of the grid at the end of the function

        for swap1,swap2 in possibles_moves :
            non_mutable_state = self.grid.hashable_state()
            for cell1,cell2 in possibles_moves:
                self.grid.swap(cell1,cell2)
                non_mutable_new_state = self.grid.hashable_state()
                if (non_mutable_state,non_mutable_new_state) not in g.edges or (non_mutable_new_state,non_mutable_state) not in g.edges: 
                        g.add_edge(non_mutable_state,non_mutable_new_state)
                self.grid.swap(cell1,cell2) #put back the changement

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
        state_path = g.bfs(src,dst)
        #print(f"state_path = {state_path}") 
        if state_path == None :
            return None
        #we have the list of the different state we need to follow to order the grid
        #but we want the sequence of swaps, so we are gonna extrat the list of the swap neccessary
        path = []
        for i in range(0,len(state_path)-1):
            state1,state2 = state_path[i],state_path[i+1]
            move_needed = Solver.move_needed(state1,state2)
            path.append(move_needed)
        return path

