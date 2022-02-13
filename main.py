from discord.ext.commands.context import Context
from cogs.birthday_cog import recycle
import config.config as config
import discord
from bot import Asobot
intents = discord.Intents.all()
discord_bot = Asobot(
    intents = intents)

def main():
    print('実行')
    token = config.token
    discord_bot.tock_loop.start()
    discord_bot.run(token)

if __name__ == '__main__':
    main()