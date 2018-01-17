import os

URL_XUEQIU = 'https://xueqiu.com'
URL_SHAWN_COMBO = "https://xueqiu.com/P/ZH946285"
URL_ALL = "https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol=ZH946285"

try:
    DB_USER = os.environ['SHAWN_DB_USER']
    DB_PASS = os.environ['SHAWN_DB_PASS']
    DB_HOST = os.environ['SHAWN_DB_HOST']
    DB_NAME = os.environ['SHAWN_DB_NAME']
except KeyError as e:
    print("请在环境变量中设置数据库信息: ", e)
    exit()
