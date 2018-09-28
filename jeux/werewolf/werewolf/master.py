from threading import Timer

from .players import Players, Roles
from .dictionary import Translator
from .communication import PublicChannel, PrivateChannel
from .votes import Votes
from .config import GameConfig
from .logs import logger

class Master:
    def __init__(self, config=GameConfig()):
        self.__players = Players()
        self.__votes = Votes() # initialisation inutile techniquement mais permet de typer la variable

        self.__game_in_progress = False

        # liste ordonnée des étapes du jeu. Certaines peuvent être supprimées suivant la distribution des rôles
        self.__steps = [(Roles.villager, self.villagers_anger),
                        (Roles.psychic, self.psychic_ritual),
                        (Roles.werewolf, self.werewolves_feast),
                        (Roles.witch, self.witch_finding),]
        # curseur sur la liste précédente indiquant l'étape en cours
        self.__step = 0

        # initialisation des canaux de communication avec des instances par défaut
        self.__village_chan = PublicChannel()
        self.__werewolves_chan = PublicChannel()
        self.__to_someone_chan = PrivateChannel()

        # initialisation du traducteur suivant la langue choisie dans la configuration
        self.__translator = Translator(config.lang)

        # chronomètres des différents rôles
        self.__village_timer = lambda: Timer(config.villagers_timer, self.villagers_votes).start()
        self.__werewolves_timer = lambda: Timer(config.werewolves_timer, self.werewolves_votes).start()
        self.__psychic_timer = lambda: Timer(config.psychic_timer, self.psychic_vision).start()
        #TODO
        #self.__witch_timer = lambda: Timer(config.witch_timer, self.witch_choice).start()

    def channels(self, villagers=None, werewolves=None, private=None):
        '''initialisation des canaux de communication'''
        if villagers:
            self.__village_chan = villagers
        if werewolves:
            self.__werewolves_chan = werewolves
        if private:
            self.__to_someone_chan = private

    def start(self):
        '''Démarrage du jeu'''
        self.__game_in_progress = True # plus personne ne peut se joindre à la partie

        # ouverture du canal de communication public des villageois en lecture seule
        self.__village_chan.open()
        self.__village_chan.read_mode()

        # détermination des rôles de chaque joueur...
        self.__players.role_distribution()

        # ... et envoi d'un message d'information à chacun d'eux
        for id in self.__players.get_all_ids():
            msg = self.__translator.do("which role {}", [self.__players.get_role(id)])
            self.__send_private(id, msg)

        # on informe chaque loup-garou de l'identité de ses congénères
        for id in self.__players.get_werewolves_ids():
            msg = self.__translator.do("other werewolves {}", [", ".join(self.__players.get_werewolves_ids_but(id))])
            self.__send_private(id, msg)

        # détermination des tours de jeu suivant les rôles existant (en enlevant les étapes des rôles inexistants
        for step in self.__steps:
            if not self.__players.seek_role(step[0]):
                self.__steps.remove(step)

        # démarrage du jeu
        self.__village_chan.send(self.__translator.do("game introduction"))
        self.__to_next_step()

    ####################################################################################################################
    ############################################  LES ETAPES DE JEU ####################################################
    ####################################################################################################################

    def villagers_anger(self):
        #ouverture des discussions pour tous
        self.__village_chan.write_mode()

        #annonce de la dernière victime et de son rôle
        victim = self.__players.last_dead
        role = self.__players.get_role(victim)
        self.__village_chan.send(self.__translator.do("dead notice {} {}", [victim, role]))

        #cas particulier: si la voyante est morte il faut supprimer son étape
        if role == Roles.psychic:
            self.__steps.remove((Roles.psychic, self.psychic_ritual))

        #demande des votes
        self.__village_chan.send(self.__translator.do("who burns"))
        self.__votes = Votes()
        #on lance le chrono
        self.__village_timer()

        return True

    def villagers_votes(self):
        # fermeture des discussions et comptage des votes
        self.__village_chan.read_mode()
        self.__votes.counting()
        loser = self.__votes.the_winner_is()

        if not loser:
            # dans le cas où personne n'a été désigné, on doit relancer les votes
            self.__village_chan.send(self.__translator.do("no culprit"))
            # On réinitialise les votes et on relance les discussions
            self.__votes = Votes()
            self.__village_chan.write_mode()
            self.__village_timer()
            return None
        else:
            self.villagers_calmed_down()

    def villagers_calmed_down(self):
        # On passe la victime des votes à l'état "mort" et on informe les joueurs de qui elle est et de son rôle
        loser = self.__votes.the_winner_is()
        self.__players.turn_to_dead(loser)
        role = self.__players.get_role(loser)
        self.__village_chan.send(self.__translator.do("who loose {} {}", [loser, role]))

        # Si la voyante est morte il faut supprimer son étape
        if role == Roles.psychic:
            self.__steps.remove((Roles.psychic, self.psychic_ritual))

        # Si un camps à gagné on passe à la conclusion
        if self.__players.game_is_over():
            self.end_game()
        else:
            self.__to_next_step()
        return True

    def psychic_ritual(self):
        # demande à la voyante la personne qu'elle compte identifier
        self.__send_private(self.__players.get_psychic_id(), self.__translator.do("vision request"))
        # On lance le chrono
        self.__psychic_timer()
        return True

    def psychic_vision(self):
        # on récupère la demande de la voyante
        vision = self.__players.psychic_vision()

        if not vision:
            # si elle n'a pas encore désigné quelqu'un on recommence
            self.__send_private(self.__players.get_psychic_id(), self.__translator.do("do a choice"))
            self.__psychic_timer()
            return None
        else:
            # sinon on lui dit
            self.__send_private(self.__players.get_psychic_id(),
                                self.__translator.do("vision answer {}", [vision]))
        self.__to_next_step()
        return True

    def werewolves_feast(self):
        # ouverture des discussions des loup-garous et demande du vote
        self.__werewolves_chan.send(self.__translator.do("which prey"))
        self.__votes = Votes()
        self.__werewolves_chan.write_mode()
        # on lance le chrono
        self.__werewolves_timer()
        return True

    def werewolves_votes(self):
        # fermeture des discussions et comptage des votes
        self.__werewolves_chan.read_mode()
        self.__votes.counting()
        loser = self.__votes.the_winner_is()

        if not loser:
            # dans le cas où aucune proie n'a été désignée, on doit recommencer
            self.__werewolves_chan.send(self.__translator.do("no prey"))
            # On réinitialise les votes et on relance les discussions
            self.__votes = Votes()
            self.__werewolves_chan.write_mode()
            self.__werewolves_timer()
            return None
        else:
            self.werewolves_sated()

    def werewolves_sated(self):
        # On passe la victime de la nuit à l'état "mort" et on rappelle aux loups-garous de qui elle est
        loser = self.__votes.the_winner_is()
        self.__players.turn_to_dead(loser)

        self.__werewolves_chan.send(self.__translator.do("prey {}", [loser]))

        #next_turn
        self.__to_next_step()
        return True

    #TODO
    def witch_finding(self):
        self.__to_next_step()
        return True
    #TODO

    def witch_choice(self):
        return True

    #TODO
    def witch_interference(self):
        return True


    def end_game(self):
        '''Conclusion du jeu'''
        if self.__players.winner == Roles.villager:
            self.__village_chan.send(self.__translator.do("villagers win"))
        else:
            self.__village_chan.send(self.__translator.do("villagers loose"))
        return True

    ####################################################################################################################
    ##############################################  LES COMMANDES  #####################################################
    ####################################################################################################################

    #TODO: toutes les cmd retournent un tuple (boolean, str) qui indique si la commande a fonctionné et si non pourquoi

    def cmd_play(self, id):
        # check que le jeu n'a pas encore démarré
        if self.__game_in_progress:
            return False, self.__translator.do("game in progress")
        # check que le joueur n'est pas déjà inscrit
        if not self.__players.add_player(id):
            return False, self.__translator.do("present yet")
        return True, ""

    #TODO
    def cmd_cure(self, sender):
        return True

    #TODO
    def cmd_poison(self, sender, target):
        return True

    #TODO
    def cmd_done(self, sender):
        return True

    def cmd_reveal(self, sender, target):
        # check que "sender" n'est pas mort
        if not self.__players.is_alive(sender):
            return False, self.__translator.do("you are dead")
        #check qu'on est au bon tour
        if self.__current_step() != Roles.psychic:
            return False, self.__translator.do("not your turn")
        #check que "sender" est bien la voyante
        if sender != self.__players.get_psychic_id():
            return False, self.__translator.do("not a psychic")
        # check que le joueur ne se désigne pas lui-même
        if sender == target:
            return False, self.__translator.do("against oneself")
        # check que la cible n'est pas morte
        if not self.__players.is_alive(target):
            return False, self.__translator.do("already dead")
        # enregistrement du choix
        self.__players.psychic_choice(target)
        return True, ""

    @logger
    def cmd_vote(self, sender, target):
        # check qu'on est au bon tour
        if self.__current_step() not in [Roles.villager, Roles.werewolf]:
            return False, self.__translator.do("not your turn")
        # check qu'on est au bon tour (dans le cas particulier des loups-garous)
        if self.__current_step() == Roles.werewolf and not self.__players.is_a_werewolf(sender):
            return False, self.__translator.do("not a werewolf")
        # check que le joueur ne se désigne pas lui-même
        if sender == target:
            return False, self.__translator.do("against oneself")
        # check que la cible n'est pas déjà morte
        if not self.__players.is_alive(target):
            return False, self.__translator.do("already dead")
        # check que le joueur n'a pas déjà voté (TODO: annulation du vote)
        if not self.__votes.vote(sender, target):
            return False, self.__translator.do("already votes")

        return True, ""

    #TODO
    def cmd_unvote(self, sender):
        return True

    ####################################################################################################################
    #####################################  FONCTIONS PUBLIQUES POUR LES TESTS ##########################################
    ####################################################################################################################
    '''
    Pour pouvoir faire des simulations de jeu pour tester mon appli j'ai du faire des fonctions publiques qui révèlent
    les rôles. Techniquement, c'est une faille.
    '''

    def who_s_alive(self):
        return self.__players.players_living()

    def who_s_a_wolf(self):
        return self.__players.werewolves_living()

    def who_s_not_a_wolf(self):
        return self.__players.villagers_living()

    ####################################################################################################################
    ############################################  FONCTIONS INTERNES ###################################################
    ####################################################################################################################

    def __send_private(self, dest, msg):
        self.__to_someone_chan.open(dest)
        self.__to_someone_chan.send(dest, msg)
        self.__to_someone_chan.close(dest)

    def __current_step(self):
        return self.__steps[self.__step][0]

    def __to_next_step(self):
        if self.__step == len(self.__steps) - 1:
            self.__step = 0
        else:
            self.__step += 1

        _, step_method = self.__steps[self.__step]

        step_method()

