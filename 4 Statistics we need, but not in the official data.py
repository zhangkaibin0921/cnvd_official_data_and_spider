
import mysql.connector

res = []  # 在已有的cnvd数据库中没有的一些cnvd_id编号
res1 = []  # 在已有的cnvd数据库中有，但是影响产品字段为空的一些cnvd_id编号
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='test'
)

cursor = conn.cursor()
query = "select cnvd_id from vule_detail_cnvd where cnvd_id is not null and cve_id is null"
cursor.execute(query)
result = cursor.fetchall()

for row in result:
    cnvd_id = str(row[0])
    #print(cnvd_id)
    query = "select cnvd_id from `cnvd` where cnvd_id= %s"
    cursor.execute(query, (cnvd_id,))
    r = cursor.fetchall()
    if len(r) == 0:
        res.append(cnvd_id)
        continue

    query = "select cnvd_id from `cnvd` where  cnvd_id=%s and cn_impact=''"
    cursor.execute(query,(cnvd_id,))
    r = cursor.fetchall()
    if len(r) != 0:
        res1.append(cnvd_id)

print(len(res))

print(len(res1))

with open('need.txt','w',encoding='utf-8') as file:
    file.write(str(res))