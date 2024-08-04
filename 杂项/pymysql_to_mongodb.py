# 把mysql数据库中的数据导入mongodb中
import pymysql
import pymongo

con = pymysql.connect(host='localhost', port=3306, user='', password='', db='')
# 获取游标
cur = con.cursor(cursor=pymysql.cursor)
# 这里以查询student表为例
try:
  cur.execute('select * from student')
  client = pymongo.MongoClient(host='localhost', port=27017)
  # 获取数据库
  db = client['']  #或者db=client.xx,相当于数据库中的use xx;
  for row in cur.fetchall():
    row['birthday'] = str(row['birthday']) #因为mongodb没有datetime类型，因此必须先转为字符串才能导入mongodb,否则可省略此步
    db.student.insert_one(row)
except Exception as e:
  print(e)
finally:
  con.close()
  client.close()