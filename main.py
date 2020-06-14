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
from speech import starters, you_rolled, crit_fail, crit_success, faq

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
    # Check for starting with roll
    if m_array[0] == "roll":
        # If only 1 word, then assume 1d20
        if len(m_array) == 1:
            content = "1d20"
        # If 2 words, then next is # of dice
        elif len(m_array) == 2 and m_array[1].isdigit():
            content = str(m_array[1]) + "d20"

        # Get the dice from the original string or our provided string
        dice = get_dice(content)

        if dice:
            # Save roll as last roll
            update_user_data(username, "last_roll", dice)
            response = await rigama_roll(dice, message)
            # Send response
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
            update_user_data(username, "last_roll", damage)
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
    # Redo the last roll
    elif content == "and again" or content == "and again!":
        # const ayy = client.emojis.find(emoji => emoji.name === "ayy")
        if username in user_data:
            if "last_roll" in user_data[username]:
                response = await rigama_roll(user_data[username]["last_roll"], message)
                # Send response
                await message.channel.send(
                    username + "'s last roll was " + user_data[username]["last_roll"]
                )
                await message.channel.send(response)
            else:
                await message.channel.send("Gotta roll something first bro!")
        else:
            await message.channel.send("Gotta roll something first bro!")
    # Ask for help/faq
    elif any(phrase in m_array[0] for phrase in commands.faq):
        await message.channel.send(random.choice(faq))


def update_user_data(user, key, value):
    if user not in user_data:
        user_data[user] = {}
    user_data[user][key] = value
    store_user_data()


async def rigama_roll(dice, message):
    # Parse the dice string into number of dice, number of sides, and modifier
    num, sides, mod = split_dice(dice)
    # Roll dice and return an array of the results
    dice_array = roll(num, sides)
    # Determine the maximum value
    dice_max = max(dice_array)

    username = message.author.name

    # Determine message to send!
    # Crit success message
    if dice_max == 20 and sides == 20:
        await message.channel.send(random.choice(crit_success))
        response = you_rolled(username) + print_dice(dice_array, mod)
    # Crit fail message
    elif min(dice_array) == 1 and sides == 20:
        await message.channel.send(random.choice(crit_fail))
        response = you_rolled(username) + print_dice(dice_array, mod)
    # Crit damage message
    elif dice_max == sides and sides < 20:
        await message.channel.send("That's a lot of damage!")
        response = you_rolled(username) + print_dice(dice_array, mod)
    # Bad roll message
    elif dice_max < sides * 0.3:
        response = starters("bad") + you_rolled(username) + print_dice(dice_array, mod)
    # Good roll message
    elif dice_max > sides * 0.85:
        response = starters("good") + you_rolled(username) + print_dice(dice_array, mod)
    # Neutral roll message
    else:
        response = (
            starters("neutral") + you_rolled(username) + print_dice(dice_array, mod)
        )
    return response


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
