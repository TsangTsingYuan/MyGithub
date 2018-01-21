import  pymongo
from pymongo import MongoClient

#连接默认主机和端口
#client = MongoClient()
#连接mongodb数据库 明确指定主机和端口
#client = MongoClient('localhost', 27017)
#使用MongoDB URI格式
client = MongoClient('mongodb://localhost:27017/')
#指定数据库名称 不存在会自动创建
db = client.stock
