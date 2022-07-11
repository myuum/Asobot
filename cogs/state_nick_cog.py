import imp
from itertools import tee
from log import log
import config.config as config
from discord import Member, Option, SlashCommandGroup, VoiceChannel, VoiceState
from discord.abc import GuildChannel
import discord
from discord.ext.commands.context import Context
from discord.ext import commands
from discord_utility import get_member
from db import state_nick_sheet

class stateNickCog(commands.Cog):
    state_nick = SlashCommandGroup("ニックネーム", "通話の状態に応じてそれぞれのニックネームを設定できます。")
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    @commands.has_permissions(change_nickname=True)
    @commands.Cog.listener()
    async def on_voice_state_update(self, member:Member, before:VoiceState, after:VoiceState):
        log.d(f"ボイスステート変更:{member.display_name} セルフミュート:{after.self_mute} サーバーミュート:{after.mute}")
        nick = state_nick_sheet.user_state_nick(member.id, after)
        log.d(f"ニックネーム:{nick}")
        if(nick == None): return
        await member.edit(nick=nick)

    @state_nick.command(name = "登録", description = "通話の状態に応じてそれぞれのニックネームを設定します。",guild_ids = [config.guild_id])
    async def state_nick_register(
        self, ctx: Context,
        normal: Option(str,name = "通常時",default = ""),
        mute: Option(str,name = "ミュート時",default = "")
    ):
        user = get_member(ctx)
        state_nick_sheet.nick_register(user.id, normal, mute)
        text = f"通常時: {normal}\nミュート時: {mute}\nとしてニックネームを登録しました。"
        await ctx.respond(text, ephemeral=True)
    
    @state_nick.command(name = "無効チャンネル設定", description = "ニックネームの変更を行わないチャンネルを設定します。",guild_ids = [config.guild_id])
    async def set_disabled_channel(
        self, ctx: Context,
        ch: Option(VoiceChannel, name = "音声チャンネル")
    ):
        state_nick_sheet.set_active_nick_channel(ch.id, False)
        text = f"{ch.name}のニックネーム変更機能を無効にしました。"
        await ctx.respond(text, ephemeral=True)

    @state_nick.command(name = "有効チャンネル設定", description = "ニックネームの変更をするチャンネルを設定します。",guild_ids = [config.guild_id])
    async def set_enable_channel(
        self, ctx: Context,
        ch: Option(VoiceChannel, name = "音声チャンネル")
    ):
        state_nick_sheet.set_active_nick_channel(ch.id, True)
        text = f"{ch.name}のニックネーム変更機能を有効にしました。"
        await ctx.respond(text, ephemeral=True)
def setup(bot):
    log.d('ロードstateNickCog')
    bot.add_cog(stateNickCog(bot))
