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