from discord.ext import tasks
import asyncio
import discord
import config
from birthday import birthday_cog

guild_ids=[config.guild_id]
# 読み込むCogの名前を格納しておく。
class Asobot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cog = birthday_cog.setup(self,guild_ids)  
    #===================各イベント=====================
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
       
    
    async def today_birthday_member(self):
        await self.cog.today_birthday_member(self) 
    @tasks.loop(seconds=30)
    async def tock_loop(self):
        # botが起動するまで待つ
        await self.wait_until_ready()
        await self.job()

    async def job(self):
        print("定時起動")
        self.today_birthday_member()

def main():
    print('実行')
    token = config.token
    intents = discord.Intents.all()
    discord_bot = Asobot(intents = intents, debug_guild = config.guild_id)
    discord_bot.tock_loop.start()
    discord_bot.run(token)


def get_member(ctx, member_id = None):
    if(member_id == None):
        member = ctx.author
    else :
        member = ctx.guild.get_member(member_id)
    if(member == None):
        return None
    return member
def get_channel(ctx, channel_id = None):
    if(channel_id == None):
        return ctx.channel
    return ctx.guild.get_channel(channel_id)

if __name__ == '__main__':
    main()
