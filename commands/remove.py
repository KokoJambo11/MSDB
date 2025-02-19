import discord
from discord.ext import commands
from utils import load_players, save_players

class RemoveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remove(self, ctx, number: int):
        """Удалить игрока: !remove <номер>"""
        players = load_players()
        if 1 <= number <= len(players):
            removed = players.pop(number-1)
            save_players(players)
            await ctx.send(f"✅ Игрок {removed['name']}#{removed['tag']} удалён!")
        else:
            await ctx.send("❌ Неверный номер игрока!")

async def setup(bot):
    await bot.add_cog(RemoveCommand(bot))