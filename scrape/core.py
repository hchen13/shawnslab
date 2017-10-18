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

from settings import *


def scan():
    import json
    print("正在发起API请求...")
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Cookie": "device_id=bdb99c41f693c372a30387f3b564733a; s=em1b7ydxvp; __utma=1.208621711.1507526003.1507526003.1507526003.1; __utmz=1.1507526003.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=bd10649447b05a985dfe102ce646520af55111cd; xqat=bd10649447b05a985dfe102ce646520af55111cd; xq_r_token=0ce0fb904ca069a26120631b8d5043e8c8fd1ba4; xq_token_expire=Fri%20Nov%2003%202017%2013%3A42%3A37%20GMT%2B0800%20(CST); xq_is_login=1; u=5984336726; bid=81b5763c50d6ae9b80baefd6038e282e_j8jr3py1; aliyungf_tc=AQAAAGhbWmq9zgwAChuWtiFPY+q7q3YD; Hm_lvt_1db88642e346389874251b5a1eded6e3=1507776474,1507883182,1508154298,1508316742; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1508321713"
    }
    try:
        response = requests.get(URL_ALL, headers=headers)
    except ConnectionError as e:
        print("网络连接错误: ")
        print("访问失败, 取消本次操作\n")
        return None
    print("请求成功")
    json_list = json.loads(response.content)
    if len(json_list) <= 0:
        return None
    combo = json_list[0]
    assert combo['name'] == '惠明'
    data_list = combo['list']
    print("已成功获取自{}起的{}条数据记录\n".format(data_list[0]['date'], len(data_list)))
    return data_list


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


def save(Session, x, date=None):
    print("正在储存数据...")
    session = Session()
    today = datetime.now().date() if date is None else date
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


def raw_save(val, date, Session):
    print("正在储存数据...")
    session = Session()



if __name__ == '__main__':
    Session = init_db()
    a = extract_data()
    save(a, Session)
