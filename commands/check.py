# commands/check.py
import discord
from discord.ext import commands
from utils import load_players, get_player_status, GAME_MODES

class CheckCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx):
        """Проверить статусы всех игроков с режимами игры"""
        players = load_players()
        if not players:
            await ctx.send("📭 Список игроков пуст!")
            return
        
        message = await ctx.send("⏳ Проверяю статусы...")
        results = []
        
        for player in players:
            status, error, game_mode = await get_player_status(
                player['server'],
                player['name'],
                player['tag']
            )
            
            line = f"• **{player['name']}#{player['tag']}** ({player['server'].upper()})\n"
            
            if error:
                line += f"❌ Ошибка: {error}"
            else:
                mode_emoji = self._get_mode_emoji(game_mode)
                line += f"{mode_emoji} {status}"
                if game_mode:
                    line += f" ({game_mode})"
            
            results.append(line)
        
        await message.edit(content="\n".join(results))

    def _get_mode_emoji(self, mode):
        emoji_map = {
            "ARAM": "🎯",
            "Ranked Solo/Duo": "⚔️",
            "Ranked Flex": "🛡️",
            "URF": "🌀",
            "Clash": "🏆",
            "Normal": "🎮"
        }
        return emoji_map.get(mode, "🎲")

async def setup(bot):
    await bot.add_cog(CheckCommand(bot))
