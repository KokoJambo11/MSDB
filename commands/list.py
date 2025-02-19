import discord
from discord.ext import commands
from utils import load_players

class ListCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        """Показать всех игроков"""
        players = load_players()
        if not players:
            await ctx.send("📭 Список игроков пуст!")
            return
        
        player_list = "\n".join(
            f"{i+1}. {p['name']}#{p['tag']} ({p['server'].upper()})"
            for i, p in enumerate(players)
        )
        await ctx.send(f"📋 Список отслеживаемых игроков:\n{player_list}")

async def setup(bot):
    await bot.add_cog(ListCommand(bot))