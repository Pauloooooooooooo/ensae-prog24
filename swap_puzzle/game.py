import random
from solver import Solver 

class Game():
    """ 
    Création d'une classe Game qui permet, avec la donnée de la difficulté du jeu, de créer une grille et de la  résoudre,
    en faisant varier la taille et le nombre de barrières
    """

    def __init__(self, difficulty):
        """
        difficulty : int between 1 and 3 ==> {1 : easy; 2 : medium; 3 : hard}
        """
        self.difficulty = difficulty

    def shuffle(taille):
        """ 
        Créer une grille de manière aléatoire connaissant la taille que l'on veut lui donner
        """
        nb = [i for i in range(1,taille**2 + 1)]
        random.shuffle(nb)
        grid = [nb[i:i+taille] for i in range(0,taille**2, taille)]
        return grid

    def create_solver(self):
        """ 
        Générer un objet type Solver connaissant la difficulté que l'on souhaite, pour jouer sur la taille de la grille 
        et l'ajout ou non de barrières
        """
        s = Solver(self.difficulty + 2, self.difficulty + 2, [])
        s.state = Game.shuffle(s.m)
        if self.difficulty != 1:
            s.barriers = s.create_barrier(self.difficulty)
        return s

    def resolve(self):
        s = self.create_solver()
        return s.state, s.Astar_improved()
    



    


