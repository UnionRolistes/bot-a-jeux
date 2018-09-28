import random

from jeux.werewolf.werewolf import master, communication, config

conf = config.GameConfig()
conf.villagers_timer = 0.1
conf.werewolves_timer = 0.1
conf.witch_timer = 0.1
conf.psychic_timer = 0.1

master = master.Master(conf)

def pick_someone(villagers):
    secure_random = random.SystemRandom()
    return secure_random.choice(villagers)

def village_vote():
    living_players = master.who_s_alive()

    for player in living_players:
        target = pick_someone(living_players)
        master.cmd_vote(player, target)

def werewolves_vote():
    living_werewolves = master.who_s_a_wolf()
    living_villagers = master.who_s_not_a_wolf()

    for werewolf in living_werewolves:
        target = pick_someone(living_villagers)
        master.cmd_vote(werewolf, target)

def psychic_choice(player):
    living_players = master.who_s_alive()
    target = pick_someone(living_players)
    print("=> {}".format(target))
    ok, _ = master.cmd_reveal(player, target)
    if not ok:
        psychic_choice(player)

def private_msg(dest, msg):
    print("To {}: {}".format(dest, msg))
    if msg.find("connaître l'identité") != -1:
        psychic_choice(dest)



villagers_chan = communication.PublicChannel(open=lambda: None,
                                             read=lambda: None,
                                             write=village_vote,
                                             close=lambda: print(""),
                                             send=lambda msg: print("To villagers: {}".format(msg)))
werewolves_chan = communication.PublicChannel(open=lambda: None,
                                             read=lambda: None,
                                             write=werewolves_vote,
                                             close=lambda: None,
                                             send=lambda msg: print("To werewolves: {}".format(msg)))
private_chan = communication.PrivateChannel(open=lambda dest: None,
                                            close=lambda dest: None,
                                            send=private_msg)

master.channels(villagers=villagers_chan, werewolves=werewolves_chan, private=private_chan)

players = ["Golgoth","Pietro","Sov","Caracole","Erg","Talweg","Firost","Tourse",
           "Steppe","Arval","Darbon","Horst","Karst","Oroshi","Alme","Aoi","Larco",
           "Léarch","Callirhoé","Boscavo","Coriolis","Sveziest","Barbak"]

for player in players:
    master.cmd_play(player)

master.start()