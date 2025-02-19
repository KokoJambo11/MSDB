import discord
from discord.ext import commands, tasks
from utils import (
    load_players, RIOT_API_KEY, REGION_MAPPING,
    fetch_riot_data, get_player_status
)
import asyncio

class MatchTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_statuses = {}
        self.tracker.start()

    def cog_unload(self):
        self.tracker.cancel()

    @tasks.loop(minutes=2)
    async def tracker(self):
        try:
            players = load_players()
            for player in players:
                current_status, _ = await get_player_status(
                    player['server'],
                    player['name'],
                    player['tag']
                )
                
                prev_status = self.last_statuses.get(f"{player['name']}#{player['tag']}")
                
                # Если статус изменился с "в игре" на другой
                if prev_status and "в игре" in prev_status and "в игре" not in current_status:
                    await self.send_match_report(player)
                
                self.last_statuses[f"{player['name']}#{player['tag']}"] = current_status
        except Exception as e:
            print(f"Tracker error: {str(e)}")

    async def send_match_report(self, player):
        """Отправляет отчет о последнем матче"""
        try:
            # Получаем PUUID игрока
            region_data = REGION_MAPPING[player['server']]
            account_url = f"https://{region_data['region']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player['name']}/{player['tag']}"
            account_data, _ = await fetch_riot_data(account_url, {"X-Riot-Token": RIOT_API_KEY})
            
            # Получаем последний матч
            match_url = f"https://{region_data['region']}.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_data['puuid']}/ids?start=0&count=1"
            match_ids, _ = await fetch_riot_data(match_url, {"X-Riot-Token": RIOT_API_KEY})
            
            if not match_ids:
                return
                
            # Получаем детали матча
            match_info_url = f"https://{region_data['region']}.api.riotgames.com/lol/match/v5/matches/{match_ids[0]}"
            match_data, _ = await fetch_riot_data(match_info_url, {"X-Riot-Token": RIOT_API_KEY})
            
            # Находим данные игрока в матче
            participant = next(
                p for p in match_data['info']['participants'] 
                if p['puuid'] == account_data['puuid']
            )
            
            # Формируем embed
            embed = discord.Embed(
                title=f"Результаты матча {player['name']}#{player['tag']}",
                color=0x00ff00 if participant['win'] else 0xff0000
            )
            
            embed.add_field(name="Чемпион", value=participant['championName'], inline=True)
            embed.add_field(name="K/D/A", 
                value=f"{participant['kills']}/{participant['deaths']}/{participant['assists']}", 
                inline=True)
            embed.add_field(name="Золото", value=participant['goldEarned'], inline=True)
            
            items = "\n".join([
                f"• {participant[f'item{i}']}" 
                for i in range(6) 
                if participant[f'item{i}'] > 0
            ])
            embed.add_field(name="Предметы", value=items or "Нет предметов", inline=False)
            
            # Отправляем в канал
            channel = self.bot.get_channel(int(os.getenv('CHANNEL_ID')))
            await channel.send(embed=embed)
            
        except Exception as e:
            print(f"Match report error: {str(e)}")

    @tracker.before_loop
    async def before_tracker(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MatchTracker(bot))