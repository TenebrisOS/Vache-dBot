import discord
import json
from datetime import datetime
import itertools
from api import (
    GetPlayerBalance,
    GetAllItemPrices,
    GetContributionsLeaderboard,
    GetMoneyLeaderboard,
)
from discord import app_commands, Object, Interaction, Embed

#region CONFIG 
with open("config.json") as js:
    config = json.load(js)

TOKEN = config["TOKEN"]
PREFIX = "'"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=786255946535796759))
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="your mom"
        )
    )

#endregion

# @client.event
# async def on_message(message: discord.Message):
#     if message.author.bot or not str(message.content).startswith(PREFIX):
#         return

#region BALANCE COMMAND
@tree.command(
    name="balance",
    description="Outputs a desired player's balance on Vache SMP",
    guild=discord.Object(id=786255946535796759),
)
async def balance(interaction: Interaction, player: str):
    bal = GetPlayerBalance(player)
    embed = discord.Embed(
        title=f"💰 {player}'s Balance",
        colour=discord.Colour.teal(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Balance", value=f"`{bal}` coins", inline=False)
    embed.set_footer(text="Vache SMP")
    await interaction.response.send_message(embed=embed)
#endregion

#region ITEMS PAGINATION
ITEMS_PER_PAGE = 9

def build_embeds(items: dict[str, dict[str, int]]) -> list[discord.Embed]:
    sorted_items = sorted(items.items())
    embeds = []
    page = 0
    while sorted_items:
        page_items, sorted_items = (
            sorted_items[:ITEMS_PER_PAGE],
            sorted_items[ITEMS_PER_PAGE:],
        )
        embed = discord.Embed(
            title=f"📦 ITEM PRICES • Page {page + 1}",
            colour=discord.Colour.green(),
        )
        for name, price in page_items:
            nice = name.replace("_", " ").title()
            embed.add_field(
                name=nice,
                value=f"SELL: `{price['sell']}`\nBUY : `{price['buy']}`",
                inline=True,
            )
        embeds.append(embed)
        page += 1
    total = len(embeds)
    for e in embeds:
        e.set_footer(text=f"Page {embeds.index(e) + 1} / {total}")
    return embeds

class PricePaginator(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__(timeout=180)
        self.embeds = embeds
        self.page = 0
        self.total = len(embeds)
        self.prev_btn.disabled = True
        if self.total == 1:
            self.next_btn.disabled = True

    @discord.ui.button(
        label="◀️ Prev", style=discord.ButtonStyle.secondary, row=0
    )
    async def prev_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.page -= 1
        self._update()
        await interaction.response.edit_message(
            embed=self.embeds[self.page], view=self
        )

    @discord.ui.button(
        label="Next ▶️", style=discord.ButtonStyle.secondary, row=0
    )
    async def next_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.page += 1
        self._update()
        await interaction.response.edit_message(
            embed=self.embeds[self.page], view=self
        )

    def _update(self):
        self.prev_btn.disabled = self.page == 0
        self.next_btn.disabled = self.page >= self.total - 1

@tree.command(
    name="items",
    description="Outputs all items prices on Vache SMP",
    guild=discord.Object(id=786255946535796759),
)
async def items(interaction: Interaction):
    await interaction.response.defer()
    embeds = build_embeds(GetAllItemPrices())
    view = PricePaginator(embeds)
    await interaction.followup.send(embed=embeds[0], view=view)
#endregion

#region CONTRIBUTIONS LEADERBOARD
def make_leaderboard_embed(
    players: dict[str, dict[str, int]], title: str, icon: str
) -> discord.Embed:
    sorted_players = sorted(
        players.items(), key=lambda kv: (kv[1]["rank"], -kv[1]["score"])
    )
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}
    lines = []
    for name, data in itertools.islice(sorted_players, 10):
        badge = medal.get(data["rank"], f"`#{data['rank']}`")
        lines.append(f"{badge}  **{name}**  —  `{data['score']}`")
    embed = discord.Embed(
        title=f"{icon} {title}",
        description="\n".join(lines),
        colour=discord.Colour.gold(),
        timestamp=datetime.utcnow(),
    )
    embed.set_footer(text="Updated")
    return embed

@tree.command(
    name="lead",
    description="Outputs the top 10 players by weekly contributions on Vache SMP",
    guild=discord.Object(id=786255946535796759),
)
async def leaderboard(interaction: Interaction):
    players = GetContributionsLeaderboard()
    embed = make_leaderboard_embed(players, "Weekly Top 10 Contributors", "🏆")
    await interaction.response.send_message(embed=embed)
#endregion

#region RICH PLAYERS LEADERBOARD
@tree.command(
    name="lb_rich",
    description="Outputs the top 10 richest players on Vache SMP",
    guild=discord.Object(id=786255946535796759),
)
async def rich_leaderboard(interaction: Interaction):
    players = GetMoneyLeaderboard() 
    embed = make_leaderboard_embed(players, "Richest Players", "💰")
    await interaction.response.send_message(embed=embed)
#endregion

client.run(TOKEN)