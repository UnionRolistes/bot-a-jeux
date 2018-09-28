class Votes:
    '''
    Classe permettant la gestion d'un vote:
     - qui a voté,
     - pour qui,
     - y-a-t'il un vainqueur?
     - qui a été désigné?
    '''

    def __init__(self):
        # catalogue des votants: id du votant -> id de la personne choisie
        self.__votes = {}
        # comptes des voix par personnes: id -> nombre de voix
        self.__counts = {}
        # gagnant(s). C'est une liste car il peut y avoir des ex aequo
        self.__winner = []

    def vote(self, voter, voted):
        '''
        Retourne True si le vote de "voter" pour "voted" a été pris en compte, False si
        "voter a déjà voté". Les deux arguments sont les id des joueurs
        '''
        if voter in self.__votes:
            return False

        self.__votes[voter] = voted

        if voted not in self.__counts:
            self.__counts[voted] = 0
        self.__counts[voted] += 1

        return True

    def counting(self):
        '''Fait les comptes des votes'''
        max = 0
        for id, score in self.__counts.items():
            if score > max:
                self.__winner = [id]
                max = score
            elif score == max:
                self.__winner.append(id)

    def the_winner_is(self):
        '''
        DOIT être précédé d'un appel à counting()
        Retourne None s'il y a un ex aequo
        Retourne l'id du joueur désignée par les votes sion
        '''
        if not self.__winner:
            return None
        if len(self.__winner) > 1:
            return None
        return self.__winner[0]

