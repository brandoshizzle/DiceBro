# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import json
import re
import pickle

# my junk
import commands
from speech import starters, you_rolled, crit_fail, crit_success

# from spellList import spellList

spell_dict = {}
with open("spellList.json") as json_file:
    spell_dict = json.load(json_file)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

user_data = {}

# Load data (deserialize)
if os.path.exists("data.pickle"):
    with open("data.pickle", "rb") as handle:
        user_data = pickle.load(handle)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content.lower()
    if content.startswith("dicebro"):
        content = content[7:].strip()
    m_array = content.split()
    username = message.author.name
    if m_array[0] == "roll" or len(m_array) == 1:

        if len(m_array) > 1:
            dice = get_dice(content)
            secondIsNum = m_array[1].isdigit()
        else:
            dice = False
            secondIsNum = True

        if dice or secondIsNum:
            if dice:
                num, sides, mod = split_dice(dice)
                dice_array = roll(num, sides)
            else:
                if len(m_array) > 1:
                    dice_array = roll(int(m_array[1]))
                    mod = 0
                else:
                    if m_array[0] == "roll":
                        dice_array = roll(1)
                        mod = 0
                    elif get_dice(content):
                        dice = get_dice(content)
                        num, sides, mod = split_dice(dice)
                        dice_array = roll(num, sides)
                    else:
                        return False
            dice_max = max(dice_array)
            if dice_max == 20:
                await message.channel.send(random.choice(crit_success))
                response = you_rolled(username) + print_dice(dice_array, mod)
            elif min(dice_array) == 1:
                await message.channel.send(random.choice(crit_fail))
                response = you_rolled(username) + print_dice(dice_array, mod)
            elif dice_max < 8:
                response = (
                    starters("bad") + you_rolled(username) + print_dice(dice_array, mod)
                )
            elif dice_max > 14:
                response = (
                    starters("good")
                    + you_rolled(username)
                    + print_dice(dice_array, mod)
                )
            else:
                response = (
                    starters("neutral")
                    + you_rolled(username)
                    + print_dice(dice_array, mod)
                )

            await message.channel.send(response)
    # CAST SPELLS
    elif any(phrase in content for phrase in commands.cast):
        spell_index = content.find("cast") + 4
        spell_name = content[spell_index:]
        spell_name = "".join(e for e in spell_name if e.isalnum()).lower()
        print(spell_name)
        spell = spell_dict[spell_name]
        await message.channel.send(
            message.author.name + " casted " + spell["name"] + "!"
        )
        desc_array = spell["desc"].split("</p>")
        for i in desc_array:
            response = i[3:]
            if response != "":
                await message.channel.send("*" + response + "*")
        await message.channel.send("******")
        damage = get_dice(spell["desc"])
        if damage:
            num, sides, mod = split_dice(damage)
            dice_array = roll(num, sides)
            await message.channel.send(
                "pew pew pew! Rolling "
                + damage
                + ": || "
                + print_dice(dice_array, mod)
                + "||"
            )
    # Set AC per user
    elif m_array[0] == "ac":
        update_user_data(username, "AC", int(m_array[1]))
        await message.channel.send("AC for " + username + " set at " + m_array[1])
    # Make a defense roll
    elif any(phrase in content for phrase in commands.defense_roll):
        if username in user_data:
            if "AC" in user_data[username]:
                the_roll = roll(1, 20)
                defense_total = the_roll[0] + user_data[username]["AC"]
                await message.channel.send(
                    "You got this bro! "
                    + username
                    + " tries to avoid with a `"
                    + str(the_roll)
                    + "` + "
                    + str(user_data[username]["AC"])
                    + " = **"
                    + str(defense_total)
                    + "**"
                )
            else:
                await message.channel.send(
                    "Yo " + username + ", you forgot to set your AC. Type ex. 'AC 14'"
                )
        else:
            await message.channel.send(
                "Yo " + username + ", you forgot to set your AC. Type ex. 'AC 14'"
            )


def update_user_data(user, key, value):
    if user not in user_data:
        user_data[user] = {}
    user_data[user][key] = value
    store_user_data()


def roll(number, dice=20):
    dice_array = []
    for i in range(number):
        dice_array.append(random.randint(1, dice))
    return dice_array


def get_dice(str):
    m = re.search(r"(\d+)?d(\d+)([\+\-]\d+)?", str.lower())
    if m:
        return m.group()
    else:
        return False


def get_dice_location(str):
    m = re.search(r"(\d+)?d(\d+)([\+\-]\d+)?", str)
    if m:
        return m.span()
    else:
        return False


def split_dice(str):
    split = str.lower().split("d")
    if "+" in split[1]:
        split.append(split[1].split("+")[1])
        split[1] = split[1].split("+")[0]
    elif "-" in split[1]:
        split.append(split[1].split("-")[1])
        split[1] = "-" + split[1].split("-")[0]
    else:
        split.append(0)
    return int(split[0]), int(split[1]), int(split[2])


def print_dice(dice_array, mod):
    if mod > 0:
        mod_sign = "+ " + str(mod)
    elif mod < 0:
        mod_sign = "- " + str(mod)[1:]
    else:
        mod_sign = ""

    the_string = (
        " `["
        + ", ".join(str(x) for x in dice_array)
        + "]` "
        + mod_sign
        + " = **"
        + str(sum(dice_array) + mod)
        + "**"
    )
    return the_string


# SUCK MY ASS on crit fail
# NO DON'T for defense roll


def store_user_data():
    # Store data (serialize)
    with open("data.pickle", "wb") as handle:
        pickle.dump(user_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


client.run(TOKEN)
