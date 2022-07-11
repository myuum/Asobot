from discord.ext.commands.context import Context
from typing import Optional, Union
from discord import Member, User

def get_member(ctx:Context, member_id = None)-> Union[User,Member,None]:
    if(member_id == None):
        member = ctx.author
    else :
        member = ctx.guild.get_member(member_id)
    if(type(member) in (User, Member)):
        return member 
    else:
        return None
def get_channel(ctx, channel_id = None):
    if(channel_id == None):
        return ctx.channel
    return ctx.guild.get_channel(channel_id)