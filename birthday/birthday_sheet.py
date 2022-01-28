import datetime
import dataset
db = dataset.connect('sqlite:///db/asobiba.sqlite')#データベース名.db拡張子で設定

def register(user_id, date):
    birthday = __load_table()
    print(f"id: {user_id}, 日付:{date}")
    birthday.upsert({"id": user_id, "birthday": date}, ["id"])

def user_serach(user_id):
    birthday = __load_table()
    data = birthday.find_one(id = user_id)
    if(data == None): return None
    return data['birthday']

def date_serach(date:datetime.date):
    birthday_t = __load_table()
    data = birthday_t.find()
    if(data == None): return
    ids = []
    for d in data:
        print(d)
        date2 = d['birthday']
        if(date.month == date2.month and date.day == date2.day):
            ids.append(d['id'])
    return ids if len(ids) != 0 else None

def __load_table():
    return db.create_table('birthday',primary_id='id',primary_type=db.types.bigint)

if __name__ == '__main__':
    date=datetime.date.today()
    ids = date_serach(date)
    for id in ids :
        print(id)

