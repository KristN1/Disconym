import discord
import os
from discord.ext import commands
from db_actions import Database
from discord_slash import SlashCommand

intents = discord.Intents.default()
intents.members = True

def get_prefix(client, message):
    if message.guild == None:
        return "!"
    else:
        return Database.find_prefix(message.guild.id)

client = commands.Bot(command_prefix= (get_prefix), intents=intents, case_insensitive=True)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

client.remove_command('help')

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        client.load_extension(f"commands.{filename[:-3]}")

for filename in os.listdir("./functions"):
    if filename.endswith(".py"):
        client.load_extension(f"functions.{filename[:-3]}")

with open("token.txt","r") as f:
    token = f.read()

client.run(token)