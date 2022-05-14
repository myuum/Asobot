from ast import Try
import datetime
from discord import Guild, Member, Message, Option, SlashCommandGroup
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from db import birthday_sheet
from view import birthbay_view
import config.config as config
from log import log

class birthdayCog(commands.Cog):
    birthday = SlashCommandGroup("誕生日", "誕生日関係コマンド")
    def __init__(self, bot:discord.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_remove(self, member:Member):
        birthday_sheet.sync_menber(member.guild)

    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        birthday_sheet.sync_menber(member.guild)

    @commands.Cog.listener()
    async def on_message(self,message:Message):
        if message.content == "メンバー同期":
            birthday_sheet.sync_menber(message.guild)
            await message.delete()    
        if (message.content.startswith('$list_sync')):
            await message.delete()
            list = message.content.split()
            if(len(list) == 0 or not list[1].isdecimal()): 
                await message.channel.send("再読み込みしたいメッセージIDを入れてください")
                return
            try:
                message = message.channel.get_partial_message(int(list[1]))
                await birthbay_view.recycle(message.guild, message)
            except discord.NotFound :
                await message.channel.send("メッセージが見つかりません")
            except discord.Forbidden :
                await message.channel.send("このbotのメッセージを指定してださい")
            except : message.channel.send("不明なエラーです")
            
            
    @birthday.command(name = "登録", description = "ユーザーを入力しない場合自分が登録されます。チャットは汚しません。",guild_ids = [config.guild_id])
    async def birthday_register(
        self, ctx: Context,
        month: Option(int,name = "月",description ="0は削除",min_value=0, max_value=12),
        day: Option(int,name = "日",description ="0は削除",min_value=0, max_value=31),
        user: Option(discord.Member,name = "ユーザー", default = discord.Member),
    ):
        date = datetime.date(2020, month, day) if(month != 0 and day != 0) else None
        if(user == discord.Member):
            member = get_member(ctx)
        else:
            member = user
        text = f"{member.display_name}の誕生日を"
        birthday_sheet.register(member.id, date)
        text = f"{month}/{day}として登録しました。"if(month != 0 and day != 0) else "削除しました"
        log.i(text)
        await ctx.respond(text, ephemeral=True)

    @birthday.command(name = "検索", description = "ユーザーで検索します", guild_ids = [config.guild_id])
    async def birthday_sheach(self, ctx: Context,
        user: Option(discord.Member, "ユーザー"),
    ):
        date = birthday_sheet.user_serach(user.id)
        text = f"{user.mention}の誕生日は"
        text += "登録されてません" if date == None else f"{date.month}月{date.day}日です"
        log.i(text)
        await ctx.respond(text)  
        
    @birthday.command(name = "リスト表示", description = "登録された誕生日の一覧をリストで表示させます", guild_ids = [config.guild_id])
    async def birthday_all(self, ctx: Context): 
        await ctx.respond("誕生日の一覧を表示します")  
        await birthbay_view.create(ctx.guild,ctx.channel)

def today_birthday_member():
    today = datetime.date.today()
    ids = birthday_sheet.date_serach(today)
    log.i("今日の誕生日検索")
    text = ""
    if(today.month == 2 and today.day == 16):
        text = f"今日はサーバー設立{today.year -2021}周年です:tada:\n"
    if(ids == None): 
        log.i("今日が誕生日の人はいません")
        return text
    text += "今日は\n"
    for id in ids :
        text += f"<@{id}>\n"
    text += "が誕生日です！！\n誕生日おめでとうございます:tada:"
    log.i(text)
    return text  

def get_member(ctx:Context, member_id = None):
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
async def recycle(guild:Guild,message:Message):
    await birthbay_view.recycle(guild,message)

def setup(bot):
    log.d('ロードbirthdayCog')
    bot.add_cog(birthdayCog(bot))
