import config
import discord
from bot import Asobot
intents = discord.Intents.all()
discord_bot = Asobot(
    intents = intents, 
    debug_guild = config.guild_id
    )

def main():
    print('実行')
    token = config.token
    discord_bot.tock_loop.start()
    discord_bot.run(token)

if __name__ == '__main__':
    main()