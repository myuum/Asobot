from typing import Optional
import dataset
from discord import VoiceState
from log import log

db = dataset.connect('sqlite:///db/asobiba.sqlite')#データベース名.db拡張子で設定

def nick_register(user_id:int,normal_nick:Optional[str], mute_nike:Optional[str]):
    db = __load_t_user()
    log.i(f"ニックネーム登録　id: {user_id}, 通常:{normal_nick}, ミュート時:{mute_nike}")
    db.upsert({"id": user_id, "normal_nick": normal_nick,"mute_nick":mute_nike,"nick_active":True}, ["id"])

def set_active_nick(user_id:int, nick_active:bool):
    db = __load_t_user()
    active_text = "ON"if(nick_active)else"OFF"
    log.i(f"id: {user_id}ニックネーム切換え{active_text}")
    db.upsert({"id": user_id, "nick_active":nick_active}, ["id"])

def set_active_nick_channel(channel_id:int, nick_active:bool):
    db = __load_t_channel()
    active_text = "ON"if(nick_active)else"OFF"
    log.i(f"id: {channel_id}有効チャンネル切換え{active_text}")
    db.upsert({"id": channel_id, "nick_active":nick_active}, ["id"])

def user_state_nick(user_id: int, state:VoiceState) -> Optional[str]:
    t_user = __load_t_user()
    t_channel = __load_t_channel()
    channel_id = state.channel.id if state.channel != None else 0
    if(t_channel.find_one(id = channel_id, nick_active = False) != None): 
        log.d("有効化されていないチャンネルでボイスステートが変更されました。")
        return None
    data = t_user.find_one(id = user_id, nick_active = True)
    if(data == None):
        log.d("有効化されていないユーザーかデータがありません。")
        return None
    key = "mute_nick" if channel_id != 0 and (state.self_mute or state.mute)  else "normal_nick"
    return data[key]

def __load_t_user() -> Optional[dataset.Table] :
    return db.create_table('t_user',primary_id='id',primary_type=db.types.bigint)

def __load_t_channel()-> Optional[dataset.Table]:
    return db.create_table('t_channel',primary_id='id',primary_type=db.types.bigint)


