import imp
from tkinter.messagebox import NO
import dataset
from discord import Guild
from discord.abc import GuildChannel
from log import log
from typing import Optional
from dataset import Table

db = dataset.connect('sqlite:///db/asobiba.sqlite')#データベース名.db拡張子で設定

def sync_menber(guild:Guild):
    t_user = __load_t_user()
    data = {d['id'] for d in t_user.find(order_by='id')}
    join_member_ids = {m.id for m in guild.members}
    leave_member_ids = data - join_member_ids
    members = [{"id": id, "is_dropout": False} for id in join_member_ids]
    members.extend([{"id": id, "is_dropout": True} for id in leave_member_ids])
    t_user.upsert_many(members,['id'])

def sync_channel(guild:Guild):
    log.d("チャンネル同期")
    t_channel = __load_t_channel()
    data = {d['id'] for d in t_channel.find(order_by='id')}
    join_member_ids = {m.id for m in guild.members}
    leave_member_ids = data - join_member_ids
    for id in leave_member_ids:
        t_channel.delete(id = id)

def delete_channel(channel:GuildChannel):
    t_channel = __load_t_channel()
    if(t_channel.find_one(id = channel.id) != None):
        t_channel.delete(id = id)

def __load_t_user() -> Optional[Table] :
    return db.create_table('t_user',primary_id='id',primary_type=db.types.bigint)

def __load_t_channel()-> Optional[Table]:
    return db.create_table('t_channel',primary_id='id',primary_type=db.types.bigint)
