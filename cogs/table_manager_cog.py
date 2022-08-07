from log import log
from discord import Bot, Member
from discord.abc import GuildChannel
from discord.ext import commands
from discord import Member
from db import table_manager

"""
サーバー全体の変更によるテーブルの管理
"""
class tableManagerCog(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        table_manager.sync_channel(self.bot.guilds[0])
        table_manager.sync_menber(self.bot.guilds[0])
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel:GuildChannel):
        log.d(f"チャンネル削除:{channel.name}")
        table_manager.delete_channel(channel = channel)

    @commands.Cog.listener()
    async def on_member_remove(self, member:Member):
        table_manager.sync_menber(member.guild)

    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        table_manager.sync_menber(member.guild)
def setup(bot):
    log.d('ロードTableManagerCog')
    bot.add_cog(tableManagerCog(bot))