'''
Afin de pouvoir rendre la communication le plus générique possible deux classes ont été créées. Cependant l'idée de
départ étant de faire un bot Discord on trouve une certaine logique:
- la classe de communication publique prévoit non seulement l'ouverture/fermeture de canal et l'envoi de message, mais
  aussi les permissions de lecture/écriture.
- la classe pour la communication privée elle est faite pour n'envoyer des messages qu'à une personne. La même instance
  peut cependant être réutilisée pour envoyer un message à une autre personne une fois la précédente contactée, c'est
  pour cette raison qu'elle propose de configurer une ouverture et fermeture conversation.

Chaque action est configurée avec une fonction définie par l'utilisateur. Evidemment une fonction peut ne rien faire!

'''

class PublicChannel:
    '''
    description des fonctions données par l'utilisateur (signatures, utilités):
    - open (() -> None): ouvre le canal de discussion public
    - close (() -> None): ferme le canal
    - read (() -> None): met le canal en lecture seule
    - write (() -> None): met le canal en lecture et écriture
    - send ((msg: str) -> None): envoie un message (msg) sur le canal public
    '''

    def __init__(self, open=None, read=None, write=None, close=None, send=None):
        if open:
            self.__opening_func = open
        else:
            self.__opening_func = lambda: print("**channel opened**")
        if close:
            self.__closing_func = close
        else:
            self.__closing_func = lambda: print("**channel closed**")
        if read:
            self.__read_mode_func = read
        else:
            self.__read_mode_func = lambda: print("**channel in reading mode**")
        if write:
            self.__write_mode_func = write
        else:
            self.__write_mode_func = lambda: print("**channel in writing mode**")
        if send:
            self.__sending_func = send
        else:
            self.__sending_func = lambda msg: print("To channel: {}".format(msg))

    def open(self):
        self.__opening_func()

    def close(self):
        self.__closing_func()

    def read_mode(self):
        self.__read_mode_func()

    def write_mode(self):
        self.__write_mode_func()

    def send(self, msg):
        self.__sending_func(msg)

class PrivateChannel:
    '''
    description des fonctions données par l'utilisateur (signatures, utilités):
    - open ((dest: str) -> None): ouvre le canal de discussion avec un destinaire correspondant à l'id donné (dest)
    - close ((dest: str) -> None): ferme le canal de discussion avec un destinaire correspondant à l'id donné (dest)
    - send ((dest: str, msg: str) -> None): envoie un message (msg) au destinaire correspondant à l'id donné (dest)
    '''

    def __init__(self, open=None, close=None, send=None):
        if open:
            self.__opening_func = open
        else:
            self.__opening_func = lambda dest: print("**{} channel opened**".format(dest))
        if close:
            self.__closing_func = close
        else:
            self.__closing_func = lambda dest: print("**{} channel closed**".format(dest))
        if send:
            self.__sending_func = send
        else:
            self.__sending_func = lambda dest, msg: print("To {}: {}".format(msg, dest))

    def open(self, dest):
        self.__opening_func(dest)

    def close(self, dest):
        self.__closing_func(dest)

    def send(self, dest, msg):
        self.__sending_func(dest, msg)
