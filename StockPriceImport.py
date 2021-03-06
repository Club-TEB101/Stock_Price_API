#!/usr/bin/env python
# coding: utf-8

# In[7]:


import json
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from pandas import json_normalize
from datetime import datetime
import os
from sqlalchemy import exc

engine = create_engine("mysql+pymysql://teb101Club:teb101Club@127.0.0.1:3306/twstock??charset=utf8mb4", max_overflow=5)

connection = engine.connect

year=datetime.today().date().year
month=datetime.today().date().month

if month >9:
    jsonpath= str(year)+'/'+str(year)+str(month)
else:
    jsonpath= str(year)+'/'+str(year)+'0'+str(month)


filelist=os.listdir(jsonpath)
    
#print(len(filelist))

data=[]
for _file in filelist:
    if 'ng' not in _file:
        filename=path+'/'+_file
        with open(filename, 'r') as f:
            data.append(json.load(f))
            
df=json_normalize(data)
df=df.rename(index=str, columns={'code':'sid'})

df[["date"]] = df[["date"]].astype('datetime64[ns]')
df[["capacity"]] = df[["capacity"]].astype('int')
df[["transaction"]] = df[["transaction"]].astype('int')
df.tail()


# In[2]:


df.info()
#print(df.describe())


# # 處理有交易紀錄的缺值

# In[3]:


df['open'].fillna(df['turnover']/df['capacity'],inplace=True)
df['high'].fillna(df['turnover']/df['capacity'],inplace=True)
df['low'].fillna(df['turnover']/df['capacity'],inplace=True)
df['close'].fillna(df['turnover']/df['capacity'],inplace=True)
df[df['open'].isna()]
#nalist = df[df['open'].isna()].index
#print(nalist)


# # 處理有開市，但沒有紀錄 (移除該欄位)

# In[4]:


df=df.dropna()
df= df.reset_index(drop=True)
print(df[df['open'].isna()])


# # 設定輸出到mySQL的資料型態

# In[5]:


#from sqlalchemy.exc import SQLAlchemyError, IntegrityError
def sqlcol(dfparam):    
    dtypedict = {}
    for i,j in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(j):
            dtypedict.update({i: sqlalchemy.types.NVARCHAR(length=4)})

        if "datetime" in str(j):
            dtypedict.update({i: sqlalchemy.types.DateTime()})

        if "float" in str(j):
            dtypedict.update({i: sqlalchemy.types.Float(precision=2, asdecimal=True)})

        if "int" in str(j):
            dtypedict.update({i: sqlalchemy.types.INT()})
            
        if "int64" in str(j):
            dtypedict.update({i: sqlalchemy.types.BIGINT()})
            
    return dtypedict

outputdict = sqlcol(df)
print(outputdict)
df.tail()


# # import to mySQL

# In[6]:


try:
    df.to_sql('transactions', engine, schema='twstock',if_exists='append',index= False, dtype=outputdict, chunksize = 1000)
    print('import mySQL Done')

except exc.IntegrityError:
    print('IntegrityError')
    pass

