import datetime
import math
import dataset
from discord import Guild
from tabulate import tabulate

db = dataset.connect('sqlite:///db/asobiba.sqlite')#データベース名.db拡張子で設定

def register(user_id, date):
    birthday = __load_table()
    print(f"id: {user_id}, 日付:{date}")
    birthday.upsert({"id": user_id, "birthday": date,"is_dropout":False}, ["id"])

def user_serach(user_id):
    birthday = __load_table()
    data = birthday.find_one(id = user_id)
    if(data == None): return None
    return data['birthday']

def date_serach(date:datetime.date):
    birthday_t = __load_table()
    data = birthday_t.find(is_dropout = False)
    if(data == None): return
    ids = []
    for d in data:
        print(d)
        date2 = d['birthday']
        if(date.month == date2.month and date.day == date2.day):
            ids.append(d['id'])
    return ids if len(ids) != 0 else None

def all():
    birthday_t = __load_table()
    data = birthday_t.find(is_dropout = False, order_by='id')
    return to_list(data)
def get_page(page:int,limit:int):
    birthday_t = __load_table()
    data = birthday_t.find(is_dropout = False, order_by='birthday',_limit = limit,_offset = limit * page)
    return to_list(data)
def page_count(limit:int): 
    birthday_t = __load_table()
    count = birthday_t.count(is_dropout = False)
    return math.ceil(count / limit)

def sync_menber(guild:Guild):
    birthday_t = __load_table()
    data = birthday_t.find(order_by='id')   
    for d in data:
        id = d['id']
        menber = guild.get_member(id)
        birthday_t.upsert({"id": id, "is_dropout": (menber == None)}, ["id"])



def to_list(data):
    datelist = []
    for d in data:
        id = d['id']
        date = d['birthday']
        datelist.append((id,f"{date.month}月{date.day}日"))
    return datelist

def __load_table():
    return db.create_table('birthday',primary_id='id',primary_type=db.types.bigint)

if __name__ == '__main__':
    print(f"{page_count(4)}")
    data = tabulate(get_page(0,3),headers=['ユーザー名', '誕生日'], tablefmt='fancy_grid')
    print(data)

