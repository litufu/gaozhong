import pandas as pd
from database import GaoZhong,Base
from session import session
import sqlite3

conn = sqlite3.connect("gaozhong.sqlite")



def add():
    df = pd.read_csv('qq.csv')
    for qq in df['qq']:
        newqq = str(qq)
        users = session.query(User).filter(User.qq == newqq).all()
        if len(users) == 0:
            user = User(name="", qq=newqq, send=False)
            session.add(user)
    session.commit()


def delete():
    users = session.query(GaoZhong).all()
    for user in users:
        session.delete(user)
    session.commit()


def update():
    users = session.query(User).all()
    users.reverse()

    for user in users:
        if user.qq == "7420838":
            break
        user.send = False
    session.commit()


if __name__ == '__main__':
    # delete()
    df = pd.read_sql_query("select * from gaozhong;", conn)
    df.to_csv('gaozhong.csv')
    print(df[:5])