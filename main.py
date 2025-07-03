import discord
import json
from api import GetPlayerBalance, GetAllItemPrices, GetContributionsLeaderboard, GetMoneyLeaderboard
from discord import app_commands

#region Variables
with open ("config.json") as js:
    config=json.load(js)

TOKEN=config["TOKEN"]
PREFIX="'"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
#endregion

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=786255946535796759))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your mom"))
@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]
    print(args)
    if args[0] == "test" :
        await message.channel.send("hi")

#region Balance
@tree.command(
    name="balance",
    description="Outputs a desired player's balance on Vache SMP",
    guild=discord.Object(id=786255946535796759)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
#endregion

#region Items
@tree.command(
    name="items",
    description="Outputs all items prices on Vache SMP",
    guild=discord.Object(id=786255946535796759)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
#endregion

#region LD
@tree.command(
    name="lb",
    description="Outputs the top 10 players by weekly contributions on Vache SMP",
    guild=discord.Object(id=786255946535796759)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
#endregion

#region Rich_Players
@tree.command(
    name="lb",
    description="Outputs the top 10 richest players on Vache SMP",
    guild=discord.Object(id=786255946535796759)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
#endregion

client.run(TOKEN)
