
from __future__ import barry_as_FLUFL
from datetime import datetime
from discord.ext import tasks,commands
import discord
import config
from birthday import birthday_cog

guild_ids=[config.guild_id]
# 読み込むCogの名前を格納しておく。
class Asobot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('cog設定')
        self.cog = birthday_cog.setup(self,config)
        print('cog完了')  
    #===================各イベント=====================
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    @commands.has_permissions(change_nickname=True)
    async def on_voice_state_update(self,member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
        print(f"ボイスステート変更:{member.display_name}")
        if(member.id != 390449375039717376): return
        if(before.self_mute == after.self_mute): return
        nick = "ミュート" if after.self_mute else ""
        await member.edit(nick=nick)
    
    async def today_birthday_member(self):
        text = self.cog.today_birthday_member(self) 
        guild = self.get_guild(int(config.guild_id))
        if(guild == None):
            print("サーバーが存在しません。")
            return
        ch = guild.get_channel(int(config.text_ch_id))
        if(ch == None): 
             print("チャンネルがが存在しません。")
             return
        await ch.send(text)


    @tasks.loop(seconds=30)
    async def tock_loop(self):
        # botが起動するまで待つ
        await self.wait_until_ready()
        await self.job()

    async def job(self):
        now = datetime.now().strftime('%H:%M')
        if (now == '00:00'):
            await self.today_birthday_member()

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
