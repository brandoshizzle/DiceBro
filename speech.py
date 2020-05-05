import random

starters_good_list = [
    "Hell yeah bro, ",
    "You're crushing it dude. ",
    "420 blaze it, ",
    "Yeeeee buddy, ",
    "My guy, ",
    "Sick bro! ",
]

starters_neutral_list = ["Suh dude, ", "Bro, ", "Bud, "]

starters_bad_list = ["Shit bro, ", "Sheeeeeeeeeeeeeet. " "Damn bro, ", "My guy... "]

you_rolled_list = ["rolled a", "laid down a", "tossed a", "flipped a", "flipped a"]

crit_fail = ["Everybody's dying :(", "NO DON'T", "f in the chat"]

crit_success = ["YOOOOOOOOOOOOOOO", "BROOOOO BRO. YEH. BRO."]


def starters(kind: str):
    if kind == "good":
        return random.choice(starters_good_list)
    elif kind == "neutral":
        return random.choice(starters_neutral_list)
    elif kind == "bad":
        return random.choice(starters_bad_list)


def you_rolled(username: str):
    return username + " " + random.choice(you_rolled_list)
