from datetime import datetime

import requests
from bs4 import BeautifulSoup
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scrape.settings import *


def extract_data():
    print("当前时间: {}\t正在提取净值...".format(datetime.now()))
    headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    try:
        response = requests.get(URL_SHAWN_COMBO, headers=headers)
    except ConnectionError as e:
        print("网络连接错误: {}".format(e))
        print("提取失败, 取消本次操作\n")
        return None
    content = response.content
    page = BeautifulSoup(content, "lxml")
    try:
        elem = page.select(
                "#cube-info > div.cube-blockmain > div > div.cube-profits.fn-clear > div:nth-of-type(3) > div.per")[0]
        value = elem.text
        print("提取完成, 此时净值为{}\n".format(value))
    except IndexError as e:
        print("净值元素在页面中不存在, 跳过...\n")
        value = None
    return float(value) if value else None


Base = declarative_base()


class NetValue(Base):
    __tablename__ = 'netvalue'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    record_time = Column(DateTime, default=datetime.now)
    date = Column(Date)

    def __repr__(self):
        date = self.record_time.date()
        return "{} 净值: {}".format(self.date, self.value)


def init_db():
    print("正在初始化数据库...")
    url = '{dialect}+{driver}://{username}:{password}@{host}/{db}?charset=utf8'.format(
        dialect='mysql',
        driver='mysqldb',
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        db=DB_NAME)
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    print('数据库初始化完成\n')
    return Session


def save(x, Session):
    print("正在储存数据...")
    session = Session()
    today = datetime.now().date()
    result = session.query(NetValue).filter(NetValue.date == today).first()
    if result is None:
        print("正在储存{}新数据: {}".format(today, x))
        nv = NetValue(value=x, date=today)
        session.add(nv)
    else:
        print("正在更新{}原有数据: {} - {}".format(today, result.value, x))
        result.value = x
        result.record_time = datetime.now()
    session.commit()
    print('储存成功!\n')


if __name__ == '__main__':
    Session = init_db()
    a = extract_data()
    save(a, Session)
