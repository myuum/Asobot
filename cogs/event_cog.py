from os import name
from discord import Guild, Member, Message, Option, SlashCommandGroup, command
import discord
import config.config as config
from discord.ext import commands
from discord.ext.commands.context import Context
from log import log

class Event_cog(commands.Cog):
    event = SlashCommandGroup("イベント","イベント関係のコマンド")
    def __init__(self, bot:discord.Bot):
        self.bot = bot
        
    @event.command(name = "登録", guild_ids = [config.guild_id])
    async def register(
        self, ctx: Context,
        title: Option(str,name = "タイトル"),
        count: Option(int,name = "人数"),
        data: Option(str,name = "開催日", description="mm/ddで登録してください、未定の場合は未定と書いてください"),
        time: Option(str,name = "開催時間", description="hh:mmで登録してください、未定の場合は未定と書いてください")
    ): await ctx.respond("コマンド", ephemeral=True)

def setup(bot):
    log.d('ロードEvent_cog')
    bot.add_cog(Event_cog(bot))
