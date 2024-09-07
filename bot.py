import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!')

bot.config = {
    'STAFF_ROLE_ID': os.getenv('STAFF_ROLE_ID'),
    'MUTED_ROLE_ID': os.getenv('MUTED_ROLE_ID'),
    'MOD_LOG_CHANNEL_ID': os.getenv('MOD_LOG_CHANNEL_ID')
}

for extension in ['cogs.moderation', 'cogs.events']:
    bot.load_extension(extension)

bot.run(os.getenv('DISCORD_TOKEN'))
