game_dictionary = {
    "werewolf": {"fr": "loup-garou",
                 "en": "werewolf",},
    "werewolves": {"fr": "loups-garous",
                   "en": "werewolves",},
    "villager": {"fr": "villageois",
                 "en": "villager",},
    "villagers": {"fr": "villageois",
                  "en": "villagers",},
    "witch": {"fr": "sorcière",
              "en": "witch",},
    "psychic": {"fr": "voyante",
                "en": "psychic",},
    "game introduction": {"fr": "La nuit tombe sur votre petit village et vous allez vous couchez après une dure journée de labeurs",
                          "en": "",},#TODO
    "dead notice {} {}": {"fr": "{} a été tué cette nuit! Son rôle était: {}",
                       "en": "{} has been killed this night! He was the {}",},
    "who burns": {"fr": "Qui d'après-vous est un loup-garou?",
                  "en": "Who is a werewolf?",},
    "no culprit": {"fr": "Pas de coupable désigné!",
                   "en": "No designated culprit!",},
    "no prey": {"fr": "Vous n'avez pas assez faim pour vous mettre d'accord?",
                "en": "No hungry enough?",},
    "who loose {} {}": {"fr": "Les votes ont désignés {} qui était un ... {}!",
                        "en": "The vote designated {} who was a ... {}",},
    "villagers win": {"fr": "Les villageois sont victorieux!",
                      "en": "Villagers win!"},
    "villagers loose": {"fr": "Les villageois ont perdu!",
                        "en": "Villagers loose!"},
    "which prey": {"fr": "Qui voulez-vous manger?",
                   "en": "Who will be your prey?",},
    "prey {}": {"fr": "Vous mangez {}.",
                "en": "You eat {}",},
    "game in progress": {"fr": "Jeu en cours",
                         "en": "Game in progress",},
    "present yet": {"fr": "Vous êtes déjà inscrit",
                    "en": "You're already in tne game",},
    "not your turn": {"fr": "Ce n'est pas votre tour de jeu",
                      "en": "It's not your turn",},
    "not a werewolf": {"fr": "Vous n'êtes pas un loup-garou",
                       "en": "You're not a werewolf", },
    "against oneself": {"fr": "C'est vous!",
                        "en": "It's you!", },
    "already dead": {"fr": "Celui-ci est déjà mort",
                     "en": "This one is already dead", },
    "already votes": {"fr": "Vous avez déjà voté!",
                      "en": "You have already vote!", },
    "which role {}": {"fr": "Votre rôle: {}",
                      "en": "You are a {}", },
    "other werewolves {}": {"fr": "Les autres loups-garous sont {}",
                            "en": "The other werewolves are {}", },
    "day and": {"fr": "La nuit commence à tomber.",
                "en": "Night is fallinf", },
    "vision request": {"fr": "De quelle personne souhaitez-vous connaître l'identité?",
                       "en": "Who do you want to identify?", },
    "vision answer {}": {"fr": "Son rôle est {}",
                         "en": "Is a {}", },
    "you are dead": {"fr": "Vous êtes mort!",
                     "en": "You are dead!", },
    "not a psychic": {"fr": "Vous n'êtes pas la voyante",
                      "en": "You are not the psychic", },
    "do a choice": {"fr": "Faites un choix",
                    "en": "Do a choice",},
    "": {"fr": "",
         "en": "", },
}

class Translator:
    def __init__(self, lang):
        self.__lang = lang

    def do(self, msg, args=[]):
        # Il faut éventuellement traduire les arguments complétant le message
        new_args = []
        for arg in args:
            if arg in game_dictionary:
                new_args.append(game_dictionary[arg][self.__lang])
            else:
                new_args.append(arg)

        if msg in game_dictionary:
            tmsg = game_dictionary[msg][self.__lang].format(*new_args)
        else:
            tmsg = msg.format(*new_args)
        return tmsg
