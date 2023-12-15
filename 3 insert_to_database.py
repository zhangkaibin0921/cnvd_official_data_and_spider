import json
import mysql.connector

json_data={}
with open('cnvd/merger.json', 'r',encoding='utf-8') as json_file:
    temp=json_file.read()
    json_data=json.loads(temp)

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='test'
)
cursor = conn.cursor()

for item in json_data['vulnerabilitys']['vulnerability']:
    print(item['number'])
    query = "insert ignore into cnvd (cn_url,cn_title,pub_date,hazard_level,cn_impact,cnvd_id,cve_id,cn_types,cn_describe,cn_reference,cn_solution,cn_patch) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    patch=''
    if 'patchName' in item:
        if 'patchDescription' in item:
            patch=item['patchName']+':'+item['patchDescription']
        else:
            patch = item['patchName']
    product=''
    if 'products' in item:
        if type(item['products']['product'])==str:
            product=item['products']['product']
        else:
            product=','.join(item['products']['product'])

    cvenumber=''
    if 'cves' in item:
        if type(item['cves']['cve'])==list:
            for i in item['cves']['cve']:
                cvenumber+=i['cveNumber']+','
            cvenumber.strip(',')
        else:
            cvenumber=item['cves']['cve']['cveNumber']

    referenceLink=''
    if 'referenceLink' in item:
        referenceLink = item['referenceLink']

    formalWay=''
    if 'formalWay' in item:
        formalWay = item['formalWay']

    serverity=''
    if 'serverity' in item:
        serverity = item['serverity']

    openTime=''
    if 'openTime' in item:
        openTime = item['openTime']

    isEvent=''
    if 'isEvent' in item:
        isEvent = item['isEvent']

    description=''
    if 'description' in item:
        description = item['description']

    title=''
    if 'title' in item:
        title = item['title']

    cursor.execute(query, (
    'http://www.cnvd.org.cn/flaw/show/'+item['number'],title, openTime, serverity, product, item['number'],
    cvenumber, isEvent, description, referenceLink, formalWay, patch))
    conn.commit()