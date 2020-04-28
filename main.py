# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import json
import re

# from spellList import spellList

spell_dict = {}
with open("spellList.json") as json_file:
    spell_dict = json.load(json_file)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

starters_good = [
    "Hell yeah bro, ",
    "You're crushing it dude. ",
    "420 blaze it, ",
    "Yeeeee buddy, ",
]

starters_neutral = ["Suh dude, ", "Bro, ", "Bud, "]

starters_bad = ["Shit bro, ", "Sheeeeeeeeeeeeeet. " "Damn bro, ", "My guy... "]

cast_commands = ["cast", "Cast", "CAST"]


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    m_array = message.content.split()
    yougot = message.author.name + " rolled a **"
    if m_array[0] == "roll":
        if m_array[1].isdigit():
            num = int(m_array[1])
            dice_array = roll(num)
            dice_max = max(dice_array)
            if dice_max < 6:
                response = (
                    random.choice(starters_bad)
                    + yougot
                    + ", ".join(str(x) for x in dice_array)
                    + "**"
                )
            elif dice_max > 14:
                response = (
                    random.choice(starters_good)
                    + yougot
                    + ", ".join(str(x) for x in dice_array)
                    + "**"
                )
            else:
                response = (
                    random.choice(starters_neutral)
                    + yougot
                    + ", ".join(str(x) for x in dice_array)
                    + "**"
                )

            await message.channel.send(response)
    elif m_array[0] in cast_commands:
        spell_name = message.content[5:]
        spell_name = "".join(e for e in spell_name if e.isalnum()).lower()
        print(spell_name)
        spell = spell_dict[spell_name]
        print(spell)
        await message.channel.send(
            message.author.name + " is casting " + spell["name"] + "!"
        )
        desc_array = spell["desc"].split("</p>")
        for i in desc_array:
            response = i[3:]
            if response != "":
                await message.channel.send("*" + response + "*")
        await message.channel.send("******")
        m = re.search(r"(\d+)?d(\d+)([\+\-]\d+)?", spell["desc"])
        print(m.group())
        print(m.span())
        if m:
            damage = m.group()
            damage_array = damage.split("d")
            dice_array = roll(int(damage_array[0]), int(damage_array[1]))
            await message.channel.send(
                "pew pew pew! Rolling "
                + damage
                + ": `["
                + ", ".join(str(x) for x in dice_array)
                + "]` = **"
                + str(sum(dice_array))
                + "**"
            )


def roll(number, dice=20):
    dice_array = []
    for i in range(number):
        dice_array.append(random.randint(1, dice))
    return dice_array


# SUCK MY ASS on crit fail
# NO DON'T on crit fail


client.run(TOKEN)
