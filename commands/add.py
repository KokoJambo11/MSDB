import discord
from discord.ext import commands
from utils import load_players, save_players

class AddCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, server: str, *args):
        """Добавить игрока: !add <сервер> <имя> <тег>"""
        if len(args) < 2:
            await ctx.send("❌ Формат: !add <сервер> <имя> <тег>\nПример: `!add euw Solo Player 1234`")
            return
        
        name = ' '.join(args[:-1])
        tag = args[-1]
        
        players = load_players()
        new_player = {
            'server': server.lower(),
            'name': name,
            'tag': tag
        }
        
        if new_player in players:
            await ctx.send("⚠️ Этот игрок уже в списке!")
            return
        
        players.append(new_player)
        save_players(players)
        await ctx.send(f"✅ Игрок **{name}#{tag}** ({server.upper()}) добавлен!")

async def setup(bot):
    await bot.add_cog(AddCommand(bot))