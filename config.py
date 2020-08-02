#encoding:utf-8
#DIALECT = 'MySQL'
USERNAME = 'xxxx'
PASSWORD = 'xxxxx'
HOST = '120.97.27.113'
PORT = '3306'
DATABASE = 'twstock'



DB_URI='mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(username = USERNAME,
password = PASSWORD,
host = HOST,
port = PORT,
db = DATABASE)

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI=DB_URI
