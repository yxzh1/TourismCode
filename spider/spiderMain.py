import requests
from lxml import etree
import re
import json
import csv
import os
import pandas as pd
import time
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','travel.settings')
django.setup()
from app.models import TravelInfo

class spider(object):
    def __init__(self):
        self.url = 'https://piao.qunar.com/ticket/list.json?keyword=%s&page=%s'
        self.detailUrl = 'https://piao.qunar.com/ticket/detail_%s.html'
        self.commentUrl = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=%s&pageSize=10&index=1'
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie':'''SECKEY_ABVK=b8IEmp75ejdwwDS1iK8GDzyH8xYTozHqQCcPpdTNsZM%3D; BMAP_SECKEY=R78tGbCTliH_UKforEFG6bkPu3YN2-OoHSZPBXBiN0pdWrDSzpYdzYjZ3u3gP2Xe26KVixeMVFejwgBR9CJ-w7ILBXooFVP75TGFGpEAJ2ShojKZ1DBu8BsGZ9WeUnWe3y1pszhfHjE-Dh2UTbV5NjBvXp99zmMbDBqLHoLYoKoxwRBDKt2wxwfwbUOuJ7ei; QN1=00006300306c49a231301a3f; QN300=s%3Dbaidu; QN99=3425; QunarGlobal=10.67.197.57_-315863c_184a309bb38_-1d6c|1669185576668; fid=d2274349-f1bd-4865-9f33-2d14799ef8d2; ctt_june=1654604625968##iK3wVKjOVuPwawPwasPwaRDwaSvNXK2nEKfhVKPAas2NEKXmERgmX2jwESt%3DiK3siK3saKjOVKDmWKjnas2nWhPwaUvt; QN57=16735024544680.884216181267804; QN271AC=register_pc; QN269=EC1BA1D02D0E11EEAE97FA163E6051F0; QN205=s%3Dbaidu; QN48=tc_c37b032d4fcdcb6e_1899bb77459_488a; ariaDefaultTheme=null; QN601=8fc403fedc30423ad9bf80560e31c026; quinn=52cff7791fb2241bffb9f293396244b1195afeecb5ca4eae483d850d7b0c028d6a231e97613a2bcc4cf790cdd99dc6b7; HN1=v1c4cacceff43bcaf2c3221e6ac091b5fa; HN2=qukzullckqssz; QN243=9; QN63=%E5%8C%97%E4%BA%AC; ctf_june=1683616182042##iK3wWSPOWwPwawPwa%3DERaKaNEPWTXSg%3DaS2wWRvOW2ETX%3DjAaK0TaSkDa23NiK3siK3saKjNaRg%2BVKa%2BWSDmWuPwaUvt; cs_june=a2251d3540fc6e52d313a0280598ebce169fbeccf97b7783ac905a4cd61ca7917ddda68253ca261c13b71af11083b5969380af884f02ad66396ed55ce1f811ecb17c80df7eee7c02a9c1a6a5b97c11791cb994da421857cea53abba039d353d55a737ae180251ef5be23400b098dd8ca; QN271SL=3a947e0d87871ace6f5cf42f3ab6f46d; QN271RC=3a947e0d87871ace6f5cf42f3ab6f46d; _q=U.txsewnz1317; csrfToken=ntVx9eipihjmotqX9cYxuUlPokMkflGH; _s=s_BOMLYBFWFGV6OGKDQ5EGVTNLOU; _t=28289096; _v=F5QaIBiw16AiX4iIGFExpwiRaDxqr8WSlHIVZy73KI9vhAiqNUnMGIMqYgRN9robdTZ1sxYtdjvQZIM8jnZNPBYz3XkwP24OsGNtzWDarvX-FgJmDsA3errgxcQgj7JAllpWEF-nxbE9JIwry4oBbKKpN4iiHg3-6tU1HXKKfgH0; QN43=""; QN42=%E5%8E%BB%E5%93%AA%E5%84%BF%E7%94%A8%E6%88%B7; _i=DFiEuDr3m5674XSwtqKxYvshUjOw; QNSPU=2052539421%2C3320442612%2C127362640%2C721810477; QN277=s%3Dbaidu; QN71="MzYuMTU3LjIxOC4yODrljJfkuqw6MQ=="; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN44=txsewnz1317; Hm_lvt_15577700f8ecddb1a927813c81166ade=1690779361,1690784008,1690784225,1690870921; QN67=14161%2C38170%2C507738%2C11824; _vi=0zEBz6vF6RFW9iIJtqBEHMULvH2-a3EmxBfE0lNvXYZfH_ZWeGGPW-YNZ7CIKqX43wypOfmsfiMaLq3GHJNA1NT-FFU9FEgLAdROUXHYQjYaJelz2bZzYQ7-lGI7TcCCdjOIEg4TTCFDlkF6QLmAdwtzAzOUCk65wafo8gxg1D31; QN58=1690875915134%7C1690878484573%7C17; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1690878485; QN271=0d364fd9-b5f4-4284-8d8a-db52f8727785; QN267=01574179237029f6b76; __qt=v1%7CVTJGc2RHVmtYMTh2V3lEaHR5cmtIQ29xNUU0N2NpN3ZnNW1EVVNXb25MaG1iNVlnd3pqUXR4azcrUE1LWjF1MVB5eWVjZjUrRklyUEE4MEkrOTA4T3BwOEVwNG9OZ1Evemk1L21RRW9ncjNBYS85Z09oYzBndkxmR21DSlVwS25qbnhzRERKS2RXVTlUU09CYktnVllVRHhZdHNtMlJQZHJDSC9ZenMzMDZzPQ%3D%3D%7C1690878726303%7CVTJGc2RHVmtYMS9FNEh1UUxNakEyeU4xSVhLb2M0M0VnVGNOUTBhS2ZKaTFWQU9MV3FVU3JXN0FTYVBJak1vbjhOcHdoM0VDSUNKbWJRM0tEdVVINlE9PQ%3D%3D%7CVTJGc2RHVmtYMSt2S0lZRlhPOTF6YmhGbnJzSXdCQ2FpRkNrYVhucU1ZTjZEL1Azb210aWZZbGJQM0V3bFVKNTZlcnlRbkxoRnErWmlFSGpBV05pYnlPUmdDeVA0RDIydWk2NndhNVl3bGpZNDJJK3RUYXgxaTI3U3dIcTNjUUFwRVhrSjBXbUhReklWTjMzdXVBZUkrejlISE1CVzFka2h2SHR2QkMxUXpWd3UyQWg5cTJUd2R2NzRoaUVEOTgvQ3FWNTdRSkkwWWs2SVRRYnk2eHJIeVV6REFQQUI2NWp2cXZDdjlsS3FxWDhabWM1NVBwYWdBRWRpZ3JhaHMzLzZseXZIRWF6aW0yMW5DeFpCT1kvak14K3lRK2dmRDR0a1VIbElPM3lsOVZZc0k2a09PdG9MSWZoZzBjK2Q2eWo2TktWbjBiaW9qVEExZmpkNFVDdjNDUDVPYlQxcGZRQXoyRnFXMDJ2UVc0eXdneklLRWprUzFGdlc2U2VodmJPdkI5NjdaU3h2NUM4aXdvSnc4VEllZDNYc2Vhb3VyUnN1N3FvV1dhd3BQdy9ETDFEYzZ2OGRZc0dUYTVTcEljc0YyQXVWb0ZXTUNEWG9DclBPVFd4T3Y0U095VmxqYXVxcXR4S2l4NTh4ZzdNRm5yV1l0azNueThqU0hFcVA5S2w2aDRYcURBQ3VRaWJSdi9MaHkxZFc3RUY0cEhoZmIwa2I1bjZLMDFTaWtqc0h6YW9HamlYS3RiNktsaWZrN1d1NHZYQkVRS3ZYVGU3MzZsbGl3b0VXQ3hJWUFJV3F0MkdRbCt3NTZVREZOdVJnU1NWNWFvMXZtR09SMXQ0M282cGluMEorVmxtT3k2UGIxbHpXL1c5OFFhNmdhWmZiODNrWCtDQnVLc0tpQkp4bE83SXhCL05xRzkraktoR1o1QWQrT0F4TWFvck8xeFNCa01RRWRUK1ZWc1IvVXJhYklmelVnWWFYc2ZFWWxiaVlVOExCSkZqV0VhMjNQNWFpVmFu;'''
    }

    def init(self):
        if not os.path.exists('tempData.csv'):
            with open('tempData.csv', 'w', encoding='utf8', newline='') as csvfile:
                wirter = csv.writer(csvfile)
                wirter.writerow([
                    'title',
                    'level',
                    'province',
                    'star',
                    'detailAddress',
                    'shortIntro',
                    'detailUrl',
                    'score',
                    'price',
                    'commentsTotal',
                    'detailIntro',
                    'img_list',
                    'comments',
                    'cover',
                    'discount',
                    'saleCount'
                ])

    def send_request(self,url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            return None

    def save_to_csv(self,row):
        with open('tempData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

    def save_to_sql(self):
        with open('tempData.csv','r',encoding='utf8') as csvfile:
            readerCsv = csv.reader(csvfile)
            next(readerCsv)
            for travel in readerCsv:
                try:
                    TravelInfo.objects.create(
                        title=travel[0],
                        level=travel[1],
                        province=travel[2],
                        star=travel[3],
                        detailAddress=travel[4],
                        shortIntro=travel[5],
                        detailUrl=travel[6],
                        score=travel[7],
                        price=travel[8],
                        commentsLen=travel[9],
                        detailIntro=travel[10],
                        img_list=travel[11],
                        comments=travel[12],
                        cover=travel[13],
                        discount=travel[14],
                        saleCount=travel[15]
                    )
                except:
                    continue

            print('已成功插入数据库')


    def spiderMain(self,resp,province):
        respJSON = resp.json()['data']['sightList']
        for index,travel in enumerate(respJSON):
            print('正在爬取该页第%s数据' % str(index + 1))
            time.sleep(2)
            detailAddress = travel['address']
            discount = travel['discount']
            shortIntro = travel['intro']
            price = travel['qunarPrice']
            saleCount = travel['saleCount']
            try:
                level = travel['star'] + '景区'
            except:
                level = '未评价'
            title = travel['sightName']
            cover = travel['sightImgURL']
            sightId = travel['sightId']
            # ================================= 详情爬取
            detailUrl = self.detailUrl % sightId
            respDetailXpath = etree.HTML(self.send_request(detailUrl).text)
            score = respDetailXpath.xpath('//span[@id="mp-description-commentscore"]/span/text()')
            if not score:
                score = 0
                star = 0
            else:
                score = score[0]
                star = int(float(score)*10)
            commentsTotal = respDetailXpath.xpath('//span[@class="mp-description-commentCount"]/a/text()')[0].replace('条评论','')
            detailIntro = respDetailXpath.xpath('//div[@class="mp-charact-intro"]//p/text()')[0]
            img_list = respDetailXpath.xpath('//div[@class="mp-description-image"]/img/@src')[:6]
            # ================================= 评论爬取
            commentSightId = respDetailXpath.xpath('//div[@class="mp-tickets-new"]/@data-sightid')[0]
            commentsUrl = self.commentUrl % commentSightId
            comments = []
            try:
                commentsList = self.send_request(commentsUrl).json()['data']['commentList']
                for c in commentsList:
                    if c['content'] != '用户未点评，系统默认好评。':
                        author = c['author']
                        content = c['content']
                        date = c['date']
                        score = c['score']
                        comments.append({
                            'author': author,
                            'content': content,
                            'date': date,
                            'score': score
                        })
            except:
                comments = []

            resultData = []
            resultData.append(title)
            resultData.append(level)
            resultData.append(province)
            resultData.append(star)
            resultData.append(detailAddress)
            resultData.append(shortIntro)
            resultData.append(detailUrl)
            resultData.append(score)
            resultData.append(price)
            resultData.append(commentsTotal)
            resultData.append(detailIntro)
            resultData.append(json.dumps(img_list))
            resultData.append(json.dumps(comments))
            resultData.append(cover)
            resultData.append(discount)
            resultData.append(saleCount)
            self.save_to_csv(resultData)


    def start(self):     # 爬虫程序
        with open('./city.csv','r',encoding='utf8') as readerFile:
            readerCsv = csv.reader(readerFile)
            next(readerCsv)
            for cityData in readerCsv:
                for page in range(1,2):    # 页数
                    try:
                        url = self.url % (cityData[0], page)
                        print('正在爬取 %s 该城市的旅游数据正在第 %s 页 路径为: %s' % (
                            cityData[0],
                            page,
                            url
                        ))

                        response = self.send_request(url)
                        self.spiderMain(response, cityData[0])
                        time.sleep(3)
                    except:
                        continue


if __name__ == '__main__':
    spiderObj = spider()
    # spiderObj.init()
    spiderObj.start()    # 采集数据
    spiderObj.save_to_sql()  # 将数据写入MySQL数据库


# 原始代码
# if __name__ == '__main__':
#     spiderObj = spider()
#     spiderObj.save_to_sql()