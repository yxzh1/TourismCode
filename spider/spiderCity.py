import requests
from lxml import etree
import csv
import os

def init():
    if not os.path.exists('city.csv'):
        with open('city.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'city',
                'cityLink'
            ])

def wirterRow(row):
        with open('city.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_html(url):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie':'QN1=00006300306c49a231301a3f; QN300=s%3Dbaidu; QN99=3425; QunarGlobal=10.67.197.57_-315863c_184a309bb38_-1d6c|1669185576668; fid=d2274349-f1bd-4865-9f33-2d14799ef8d2; ctt_june=1654604625968##iK3wVKjOVuPwawPwasPwaRDwaSvNXK2nEKfhVKPAas2NEKXmERgmX2jwESt%3DiK3siK3saKjOVKDmWKjnas2nWhPwaUvt; QN57=16735024544680.884216181267804; QN271AC=register_pc; QN269=EC1BA1D02D0E11EEAE97FA163E6051F0; QN205=s%3Dbaidu; QN48=tc_c37b032d4fcdcb6e_1899bb77459_488a; ariaDefaultTheme=null; QN601=8fc403fedc30423ad9bf80560e31c026; quinn=52cff7791fb2241bffb9f293396244b1195afeecb5ca4eae483d850d7b0c028d6a231e97613a2bcc4cf790cdd99dc6b7; HN1=v1c4cacceff43bcaf2c3221e6ac091b5fa; HN2=qukzullckqssz; QN243=9; QN63=%E5%8C%97%E4%BA%AC; ctf_june=1683616182042##iK3wWSPOWwPwawPwa%3DERaKaNEPWTXSg%3DaS2wWRvOW2ETX%3DjAaK0TaSkDa23NiK3siK3saKjNaRg%2BVKa%2BWSDmWuPwaUvt; cs_june=a2251d3540fc6e52d313a0280598ebce169fbeccf97b7783ac905a4cd61ca7917ddda68253ca261c13b71af11083b5969380af884f02ad66396ed55ce1f811ecb17c80df7eee7c02a9c1a6a5b97c11791cb994da421857cea53abba039d353d55a737ae180251ef5be23400b098dd8ca; QN271SL=3a947e0d87871ace6f5cf42f3ab6f46d; QN271RC=3a947e0d87871ace6f5cf42f3ab6f46d; _q=U.txsewnz1317; csrfToken=ntVx9eipihjmotqX9cYxuUlPokMkflGH; _s=s_BOMLYBFWFGV6OGKDQ5EGVTNLOU; _t=28289096; _v=F5QaIBiw16AiX4iIGFExpwiRaDxqr8WSlHIVZy73KI9vhAiqNUnMGIMqYgRN9robdTZ1sxYtdjvQZIM8jnZNPBYz3XkwP24OsGNtzWDarvX-FgJmDsA3errgxcQgj7JAllpWEF-nxbE9JIwry4oBbKKpN4iiHg3-6tU1HXKKfgH0; QN43=""; QN42=%E5%8E%BB%E5%93%AA%E5%84%BF%E7%94%A8%E6%88%B7; _i=DFiEuDr3m5674XSwtqKxYvshUjOw; QNSPU=2052539421%2C3320442612%2C127362640%2C721810477; QN277=s%3Dbaidu; QN71="MzYuMTU3LjIxOC4yODrljJfkuqw6MQ=="; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; QN44=txsewnz1317; QN67=38170%2C507738%2C11824; Hm_lvt_15577700f8ecddb1a927813c81166ade=1690779361,1690784008,1690784225,1690870921; _vi=-k2AsGRKl8xEYYNxNyO4cVpTyqU0MRywS3aFzPMk1xU86S8RXFt5VEjW5-558kNFKPwUK-YuouGTcnnU9R8gIqPsftC_QO1WxhUuLWGhwzoDfNfNlJ8iAgvwM1xlAP8wYnKsSR2e4PpUrLr1WzQS5xj4TTixsTty74uli_TMs8lP; QN58=1690875915134%7C1690876060197%7C12; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1690876061; QN271=50e3e9ff-99ab-41de-9b81-79b73691639b; JSESSIONID=A797207C02559CA92998EDB64DB63821; QN267=01574179237f0e556bd; __qt=v1%7CVTJGc2RHVmtYMTlaTE8rRXVESTdwNTVPN3F5N0ovNi9iZUxxdmhxUW5wOUo3OWFyQ3BUSGhIN3VGenNRMFBDRy9zSGFaZ2VpSkpwVXhYTzlyckpTVUN5anFlajZYQWZzOU1TK1JCOXlBVE1IdTZUTi9BU1ltaFY0ZFFLOUpCczdLRTRyYzdFM0VjWHhrdXBlajBzRTNpemJjdnErWHJmNWFGNmxFSXpJdU5RPQ%3D%3D%7C1690876265736%7CVTJGc2RHVmtYMTlQSU43VW94SzhTYU1RcGI5ZDhteHM2bXVVSVZ4cnI4RFZwRTZNSExZMS9pMDJOUE0zQS9rRjhpbUJsQzEyVnZYcFR4anVIeHJxS0E9PQ%3D%3D%7CVTJGc2RHVmtYMTlBeXZ0dG56UlRuRU9HVG5rSVhwcXl0cEU2SkcvclJwaGVkRjhoUXZzeS9VaW5HaCtCWmxEd0hBemJCQW5ENHl5SFJXdVJwaVdkWVJ3c2NUK1NCWDRkMHJRM2MycytsWi9MZ0gwSk5YckJ1T3A3dHZnZngrT3B0ekg1ZHErcnVXZHl0SVFRcnJDVmJabFVsdjUzaklPR016TUFrWFRNbm5jc3RsSVJTenRiSHV6WEpsMWYzcFZFUjFCMU1OMDI3NEN1RnM4RkM1Y3JDeUQ0SWVDMUVuT2dnKzlMR3JBQS93Vm5yd0YwTzJWWjlCWlFmSTV3cXlZVEJUTUxxYXg5RUo4MzRWQnZmcDl4UnhKZC9MckJxSndZcUlHMDRlbnF6OGZST2t0aGwwYk1UOUorTitNWGdGaitRNUJ6d3BmN0JwZGVCV0FjSVZnWmNyWWgzYkRpcCtnQkZnT3VNZkd4UG95SW95ajN4bzJMSWpTUmR0RTR5UkZIdkZkVjBnTDBITTBxcTh1K1Erbk1vS0IwdzhTUi9Nako3VDYzTHl2aCtnT0U0NjBOUVJyZXRaUVJmckQrWnl0ODd1WWhjdVdFaGRRZzQxSjh6ZHJjWkJkWEQ0M0dUb3JrbTBad3BmVGlndTY5TnN6Q25lMGxqV05WdjdocEtMMHlnSlNQbVVTOStXUks1aFNaREpGN1ZmSk5IMk5NVEtDVFcwNnlMbmVuNitUODQxTkFTWUlMNEpwY0d1Q1A3UlBocTIzRnNDZzl1OGpjc2pDc1BjU1ZOSCsxTFNsZ1p1T2toeTJLZDh2SXlRVi8zVEx3bWtTM3BhUi8rOFhNN1JVbEl3MUdNbUd6dzYzVWZ6K3BleW1Ca1RVbTdLeDBhck1mQUJleFM0VWQ0TjlzZk1WN3hrRmdZMGJrSU1JalpMNW96ZDBQbDhxN2M5MW5iUnkxUVV1eHgyVERKak9WM2tZWE1taXl4ZHdBenhKa1lKQ0x5by9lYk5yemo4RGo3dmRn'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response
    else:
        return None

def parse_html(response):
    root = etree.HTML(response.text)
    cityList = root.xpath('//div[@class="mp-city-content"]//li[@class="mp-city-item"]/a')
    for city in cityList:
        cityName = city.text
        cityLink = 'https://piao.qunar.com/ticket/list.htm?keyword=%s' % cityName
        wirterRow([
            cityName,
            cityLink
        ])

if __name__ == '__main__':
    url = 'https://piao.qunar.com/daytrip/list.htm'
    init()
    response = get_html(url)
    parse_html(response)