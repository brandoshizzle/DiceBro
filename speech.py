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
]

starters_neutral_list = [
    "Suh dude, ",
    "Bro, ",
    "Bud, ",
    "HEY GUYS, Dicebro here. ",
    "Three things are gunna happen: I hit you, you hit the ground, and ",
]

starters_bad_list = [
    "Shit bro, ",
    "Sheeeeeeeeeeeeeet. " "Damn bro, ",
    "My guy... ",
    "Give your balls a tug. ",
]

you_rolled_list = ["rolled a", "laid down a", "tossed a", "flipped a", "flipped a"]

crit_fail = ["Everybody's dying :(", "NO DON'T", "f in the chat"]

crit_success = ["YOOOOOOOOOOOOOOO", "BROOOOO BRO. YEH. BRO.", "That's a lot of damage!"]

faq = [
    "Haha gl bro",
    "FAQ? More like faq you am I right?",
    "gg my guy",
    "I hope you like reading python my dude. https://github.com/brandoshizzle/DiceBro",
]


def starters(kind: str):
    if kind == "good":
        return random.choice(starters_good_list)
    elif kind == "neutral":
        return random.choice(starters_neutral_list)
    elif kind == "bad":
        return random.choice(starters_bad_list)


def you_rolled(username: str):
    return username + " " + random.choice(you_rolled_list)
