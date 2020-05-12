import random

starters_good_list = [
    "Hell yeah bro, ",
    "You're crushing it dude. ",
    "420 blaze it, ",
    "Yeeeee buddy, ",
    "My guy, ",
    "Sick bro! ",
    "SKKKRAT SKKKRAT! ",
    "Hold my spitter, bro... ",
    "Like, dude! ",
    "Wheel, snipe, celly boys. "
]

starters_neutral_list = ["Suh dude, ", "Bro, ",
                         "Bud, ", "HEY GUYS, Dicebro here. ", "Three things are gunna happen: I hit you, you hit the ground, and ", "skriii brappp bwooraappp! "]

starters_bad_list = ["Shit bro, ",
                     "Sheeeeeeeeeeeeeet. " "Damn bro, ", "My guy... ", "Give your balls a tug. ", "Jinkies!", "Jeepers!", "Zoinks!", "Ruh-Roh!"]

you_rolled_list = ["rolled a", "laid down a",
                   "tossed a", "flipped a", "flipped a"]

crit_fail = ["Everybody's dying :(", "NO DON'T",
             "f in the chat", "Ya fucked er, bud."]

crit_success = ["YOOOOOOOOOOOOOOO",
                "BROOOOO BRO. YEH. BRO.", "COME ON AND SLAM!", "That's a lot of damage!"]

just_chatting = ["Gonna crush some sandos after prackie."]

sfx = [[""]]


def starters(kind: str):
    if kind == "good":
        return random.choice(starters_good_list)
    elif kind == "neutral":
        return random.choice(starters_neutral_list)
    elif kind == "bad":
        return random.choice(starters_bad_list)


def you_rolled(username: str):
    return username + " " + random.choice(you_rolled_list)
