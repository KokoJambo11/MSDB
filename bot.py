import discord
from discord.ext import commands
import os
import logging
from utils import DATA_FILE, save_players
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

async def load_commands():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                logging.info(f"Loaded command: {filename}")
            except Exception as e:
                logging.error(f"Failed to load {filename}: {str(e)}")

@bot.event
async def on_ready():
    logging.info(f"Бот {bot.user.name} запущен!")
    if not DATA_FILE.exists():
        save_players([])
    await load_commands()

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))