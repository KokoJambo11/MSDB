import os
import json
import logging
import aoihttp
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

# Конфигурация
RIOT_API_KEY = os.getenv('RIOT_API_KEY')
DATA_FILE = Path('players.json')

REGION_MAPPING = {
    'euw': {'cluster': 'EUW1', 'region': 'europe'},
    'na': {'cluster': 'NA1', 'region': 'americas'},
    'eune': {'cluster': 'EUN1', 'region': 'europe'},
    'kr': {'cluster': 'KR', 'region': 'asia'},
    'ru': {'cluster': 'RU', 'region': 'europe'},
    'tr': {'cluster': 'TR1', 'region': 'europe'},
    'lan': {'cluster': 'LA1', 'region': 'americas'},
    'las': {'cluster': 'LA2', 'region': 'americas'},
    'oce': {'cluster': 'OC1', 'region': 'sea'},
    'jp': {'cluster': 'JP1', 'region': 'asia'}
}

GAME_MODES = {
    400: "Normal Draft",
    420: "Ranked Solo/Duo",
    430: "Normal Blind",
    440: "Ranked Flex",
    450: "ARAM",
    700: "Clash",
    900: "URF",
    1700: "Arena"
}

async def get_player_status(server, name, tag):
    region_data = REGION_MAPPING.get(server.lower())
    if not region_data:
        return None, "Invalid server"

    account_url = f"https://{region_data['region']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{quote(name)}/{tag}"
    account_data, error = await fetch_riot_data(account_url, {"X-Riot-Token": RIOT_API_KEY})
    
    if error or not account_data.get('puuid'):
        return None, error or "Player not found"

    spectator_url = f"https://{region_data['cluster']}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{account_data['puuid']}"
    game_data, _ = await fetch_riot_data(spectator_url, {"X-Riot-Token": RIOT_API_KEY})
    
    return "🎮 В игре" if game_data else "💤 Оффлайн", None

def load_players():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading players: {str(e)}")
        return []

def save_players(players):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(players, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving players: {str(e)}")

async def fetch_riot_data(url, headers):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json(), None
                elif response.status == 404:
                    return None, "Not found"
                elif response.status == 403:
                    logging.critical("Invalid API Key!")
                    return None, "Invalid API Key"
                else:
                    return None, f"API Error: {response.status}"
        except Exception as e:
            logging.error(f"Connection error: {str(e)}")
            return None, "Connection failed"
