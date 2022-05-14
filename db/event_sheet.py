import datetime
import math
import dataset
from discord import Message
from log import log

db = dataset.connect('sqlite:///db/asobiba.sqlite')#データベース名.db拡張子で設定
def register(message:Message, gm_id:int, date:datetime.datetime, scenario_name:str,):
    t_event = __load_t_event()

def __load_t_event():
    return db.create_table('mystery_event')
