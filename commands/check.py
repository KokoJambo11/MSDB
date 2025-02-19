import discord
from discord.ext import commands
from utils import load_players, get_player_status

class CheckCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx):
        """Проверить всех игроков"""
        players = load_players()
        if not players:
            await ctx.send("📭 Список игроков пуст!")
            return
        
        message = await ctx.send("⏳ Проверяю статусы...")
        results = []
        
        for player in players:
            status, error = await get_player_status(
                player['server'],
                player['name'],
                player['tag']
            )
            
            if error:
                results.append(f"❌ {player['name']}#{player['tag']}: {error}")
            else:
                results.append(f"• {player['name']}#{player['tag']} ({player['server'].upper()}): {status}")
        
        await message.edit(content="\n".join(results))

async def setup(bot):
    await bot.add_cog(CheckCommand(bot))