import datetime
from discord import Member, Option, SlashCommandGroup, User
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from . import birthday_sheet

class birthdayCog(commands.Cog):
    guild_ids = []
    birthday = SlashCommandGroup("誕生日", "誕生日関係コマンド")
    def __init__(self, bot:discord.Bot, guild_ids):
        self.guild_ids = guild_ids
        self.bot = bot
        
    @birthday.command(name = "登録",guild_ids = guild_ids)
    async def birthday_register(
        self, ctx: Context,
        month: Option(int, "月",min_value=1, max_value=12),
        day: Option(int, "日",min_value=1, max_value=31),
        user: Option(discord.Member, "誰", default = discord.Member),
    ):
        date = datetime.date(2020, month, day)
        text = ''
        if(user == discord.Member):
            member = get_member(ctx)
        else:
            member = user
        birthday_sheet.register(member.id, date)
        text = f"{member.name}の誕生日を{month}/{day}として登録しました。"
        await ctx.respond(text, ephemeral=True)

    @birthday.command(name = "検索", description = "ユーザーで検索します", guild_ids = guild_ids)
    async def birthday_sheach(self, ctx: Context,
        user: Option(discord.Member, "ユーザー"),
    ):
        date = birthday_sheet.user_serach(user.id)
        text = f"{user.mention}の誕生日は"
        text += "登録されてません" if date == None else f"{date.month}月{date.day}日です"
        await ctx.respond(text)  
    
    async def today_birthday_member(self,ctx: Context):
        ids = birthday_sheet.date_serach(datetime.date.today())
        text = "今日の誕生日は\n"
        if(ids == None): return
        for id in ids :
            member = get_member(self,id) 
            if(type(member) is User ):
                print(member.name)
                text += f"{member.mention}\n"
            else: continue
        await ctx.respond(text)  
                
            

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
def setup(bot, guild_ids):
    cog = birthdayCog(bot, guild_ids)
    bot.add_cog(cog)
    return cog
