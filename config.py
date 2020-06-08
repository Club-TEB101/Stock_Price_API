#encoding:utf-8
#DIALECT = 'MySQL'
USERNAME = 'teb101Club'
PASSWORD = 'teb101Club'
HOST = '127.0.0.1'
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
