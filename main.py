import config.config as config
import discord
from bot import Asobot
from log import log
intents = discord.Intents.all()
discord_bot = Asobot(
    intents = intents)

def main():
    log.d('実行')
    token = config.token
    discord_bot.tock_loop.start()
    discord_bot.run(token)

if __name__ == '__main__':
    main()