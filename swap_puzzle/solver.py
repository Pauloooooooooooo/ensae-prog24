from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.
    """
    def __init__(self,m,n):
        Grid.__init__(self,m,n,initial_state = [])
        
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution
        #  returned.
        S = []
        for i in range(1, g.n*g.m +1):
            l,c = self.search(g,i)
            lf, cf = g.d[i]
            while lf != l:
                if lf < l:
                    g.swap((l,c),(l-1,c))
                    S.append(((l,c),(l-1,c)))
                    l = l-1
                else:
                    g.swap((l,c),(l+1,c))
                    S.append(((l,c),(l+1,c)))
                    l += 1
            while cf != c:
                if cf < c:
                    g.swap((l,c),(l,c-1))
                    S.append(((l,c),(l,c-1)))
                    c = c-1
                else:
                    g.swap((l,c),(l,c+1))
                    S.append(((l,c),(l,c+1)))
                    c += 1
        return S

    def search(g,elt):
        for i in range(len(g.state)):
            for j in range(len(g.state[i])):
                if g.state[i][j] == elt:
                    return (i,j)

