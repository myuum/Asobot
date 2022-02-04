import datetime
from os import name
from discord import Member, Option, SlashCommandGroup, User
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from . import birthday_sheet

class birthdayCog(commands.Cog):
    guild_ids = []
    birthday = SlashCommandGroup("誕生日", "誕生日関係コマンド")
    def __init__(self, bot:discord.Bot, config):
        self.guild_ids = [config.guild_id]
        self.bot = bot
        
    @birthday.command(name = "登録",guild_ids = guild_ids)
    async def birthday_register(
        self, ctx: Context,
        month: Option(int, name = "月",min_value=1, max_value=12),
        day: Option(int, name = "日",min_value=1, max_value=31),
        user: Option(discord.Member, name = "ユーザー", default = discord.Member),
    ):
        date = datetime.date(2020, month, day)
        text = ''
        if(user == discord.Member):
            member = get_member(ctx)
        else:
            member = user
        birthday_sheet.register(member.id, date)
        text = f"{member.display_name}の誕生日を{month}/{day}として登録しました。"
        print(text)
        await ctx.respond(text, ephemeral=True)

    @birthday.command(name = "検索", description = "ユーザーで検索します", guild_ids = guild_ids)
    async def birthday_sheach(self, ctx: Context,
        user: Option(discord.Member, name = "ユーザー"),
    ):
        date = birthday_sheet.user_serach(user.id)
        text = f"{user.mention}の誕生日は"
        text += "登録されてません" if date == None else f"{date.month}月{date.day}日です"
        print(text)
        await ctx.respond(text)  
    @birthday.command(name = "全取得", description = "すべてのユーザーの誕生日を取得します。", guild_ids = guild_ids)
    async def birthday_all(self, ctx: Context,):
        data = birthday_sheet.all()
        text = ""
        for id,date in data.items() :
            member = get_member(ctx, id)
            text += f"{member.display_name}:{date.month}月{date.day}日"
        await ctx.respond(text)  
    
    def today_birthday_member(self,ctx: Context):
        ids = birthday_sheet.date_serach(datetime.date.today())
        print("今日の誕生日検索")
        text = "今日は\n"
        if(ids == None): 
            print("今日が誕生日の人はいません")
            return None
        for id in ids :
            text += f"<@{id}>\n"
        text += "が誕生日です!! おめでとうございます!!"
        print(text)
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
def setup(bot, config):
    cog = birthdayCog(bot, config)
    bot.add_cog(cog)
    return cog
