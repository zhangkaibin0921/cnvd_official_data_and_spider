#需要手动更换cookie，单线程，sleep(3)。否则会被封锁ip
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
from time import sleep
import mysql.connector

headers = {
    'Host': 'www.cnvd.org.cn',
    'Cookie': '__jsluid_s=46493e058490a07b63faaa0c00f0e8e9; JSESSIONID=B02A720D957A837C0ED1C655AE20E90D; __jsl_clearance_s=1702634754.095|0|iqik9GgZGEomL5ijLqZBJjI4aBM%3D',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Priority': 'u=0, i',
    'Connection': 'close'
}


conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='test'
)
cursor = conn.cursor()

def getdetail(cnvd_id):
    url="https://www.cnvd.org.cn/flaw/show/"+cnvd_id
    session = requests.Session()
    session.cookies.clear()

    print(url)
    response = session.get(url, headers=headers)
    sleep(3)
    page_text = response.text
    html = etree.HTML(page_text)
    #print(page_text)

    if page_text.startswith('<script>document.cookie'):
        print("cookie失效了")
        return False

    item = {}
    # URL
    item["cn_url"] = url
    # 获取漏洞标题
    item["cn_title"] = html.xpath(
        "//div[@class='blkContainerPblk']/div[@class='blkContainerSblk']/h1/text()")
    if item["cn_title"]:
        item["cn_title"] = html.xpath("//div[@class='blkContainerPblk']/div[@class='blkContainerSblk']/h1/text()")[
            0].strip()
    else:
        item["cn_title"] = ''

    # 获取漏洞公开日期
    # item["date"] = html.xpath("//td[text()='公开日期']/following-sibling::td[1]/text()")
    item["pub_date"] = html.xpath(
        "//div[@class='tableDiv']/table[@class='gg_detail']//tr[2]/td[2]/text()")
    if item["pub_date"]:
        item["pub_date"] = "".join(
            [i.strip() for i in item["pub_date"]])
    #    item["pub_date"] = self.convertstringtodate(item["pub_date"])
    else:
        item["pub_date"] = ''
    #    item["pub_date"] = self.convertstringtodate(item["pub_date"])

    # 获取漏洞危害级别
    item["hazard_level"] = html.xpath(
        "//td[text()='危害级别']/following-sibling::td[1]/text()")
    if item["hazard_level"]:
        item["hazard_level"] = "".join(
            [i.replace("(", "").replace(")", "").strip() for i in item["hazard_level"]])
    else:
        item["hazard_level"] = ''

    # 获取漏洞影响的产品
    item["cn_impact"] = html.xpath(
        "//td[text()='影响产品']/following-sibling::td[1]/text()")
    if item["cn_impact"]:
        item["cn_impact"] = ",".join(
            [i.strip() for i in item["cn_impact"]])
        item["cn_impact"] =item["cn_impact"].strip(',')
    else:
        item["cn_impact"] = ''

    # 获取cnvd id
    item["cnvd_id"] = html.xpath(
        "//td[text()='CNVD-ID']/following-sibling::td[1]/text()")
    if item["cnvd_id"]:
        item["cnvd_id"] = "".join(
            [i.strip() for i in item["cnvd_id"]])
    else:
        item["cnvd_id"] = ''

    # 获取cve id
    item["cve_id"] = html.xpath(
        "//td[text()='CVE ID']/following-sibling::td[1]//text()")
    if item["cve_id"]:
        item["cve_id"] = ",".join(
            [i.strip() for i in item["cve_id"]])
    else:
        item["cve_id"] = ''

    # 获取漏洞类型
    item["cn_types"] = html.xpath(
        "//td[text()='漏洞类型']/following-sibling::td[1]//text()")
    if item["cn_types"]:
        item["cn_types"] = "".join(
            [i.strip() for i in item["cn_types"]])
    else:
        item["cn_types"] = ''

    # 获取漏洞描述
    item["cn_describe"] = html.xpath(
        "//td[text()='漏洞描述']/following-sibling::td[1]//text()")
    if item["cn_describe"]:
        item["cn_describe"] = "".join(
            [i.strip() for i in item["cn_describe"]]).replace("\u200b", "")
    else:
        item["cn_describe"] = ''

    # 获取漏洞的参考链接
    item["cn_reference"] = html.xpath(
        "//td[text()='参考链接']/following-sibling::td[1]/a/@href")
    if item["cn_reference"]:
        item["cn_reference"] = item["cn_reference"][0].replace('\r', '')
    else:
        item["cn_reference"] = ''

    # 获取漏洞的解决方案
    item["cn_solution"] = html.xpath(
        "//td[text()='漏洞解决方案']/following-sibling::td[1]//text()")
    if item["cn_solution"]:
        item["cn_solution"] = "".join(
            [i.strip() for i in item["cn_solution"]])
    else:
        item["cn_solution"] = ''

    # 获取漏洞厂商补丁
    item["cn_patch"] = html.xpath(
        "//td[text()='厂商补丁']/following-sibling::td[1]/a")
    if item["cn_patch"]:
        for i in item["cn_patch"]:
            list = []
            try:
                list.append(i.xpath("./text()")[0])
                list.append("http://www.cnvd.org.cn" + i.xpath("./@href")[0])
                item["cn_patch"] = list[0] + ':' + list[1]
            except IndexError:
                item["cn_patch"] = ''
    else:
        item["cn_patch"] = ''


    if item["cnvd_id"]=='':
        item["cnvd_id"] ="AKEE"+str(random.randint(0, 100000000))


    print(item)

    query = "insert ignore into cnvd (cn_url,cn_title,pub_date,hazard_level,cn_impact,cnvd_id,cve_id,cn_types,cn_describe,cn_reference,cn_solution,cn_patch) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query, (item['cn_url'],item['cn_title'],item['pub_date'],item['hazard_level'],item['cn_impact'],item['cnvd_id'],item['cve_id'],item['cn_types'],item['cn_describe'],item['cn_reference'],item['cn_solution'],item['cn_patch']))
    conn.commit()
    return True

# 创建 ThreadPoolExecutor 对象
executor = ThreadPoolExecutor(max_workers=1)


cnvd_list=[]
with open('need.txt','r',encoding='utf-8') as file:
    temp=file.read()
    cnvd_list=eval(temp)

print(cnvd_list)
#cnvd_list=['CNVD-2021-14449']


for i in cnvd_list:
    res=getdetail(i)
    #future=executor.submit(getdetail, i)
    if not res:#future.result():
        print(i+"**************")
        with open('need.txt', 'w', encoding='utf-8') as file:
            file.write(str(cnvd_list))
        break

# 关闭线程池
executor.shutdown()
