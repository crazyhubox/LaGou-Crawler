import csv
import asyncio
from aiohttp import ClientSession
from component.tools import J2Dict

from typing import Dict, Mapping, Tuple
from urllib.parse import quote
from parsel import Selector
from re import compile as re_cmp
from yarl import URL
from color import Colored
from time import time


def now(): return time()


def timer(func):
    start = now()

    def newfunc(*ars, **kw):
        res = func(*ars, **kw)
        print(clo.yellow(f'time:{now()-start}'))
        return res
    return newfunc


clo = Colored()


class AioSplash:
    def __init__(self, position: str, city: str):
        self.COOKIES = {}
        self.position = position
        self.city = city
        self.run(self.position, self.city)

    async def fetch_html(self, session: ClientSession, page, position, city):
        headers = {
            'authority': 'www.lagou.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-anit-forge-code': '0',
            'x-requested-with': 'XMLHttpRequest',
            'x-anit-forge-token': 'None',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.lagou.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%AE%9E%E4%B9%A0/p-city_3?px=default&gj=%E5%9C%A8%E6%A0%A1/%E5%BA%94%E5%B1%8A',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        params = (
            ('px', 'default'),
            ('city', city),
            ('needAddtionalResult', 'false'),
        )

        data = {
            'first': 'true',
            'pn': f"{page}",
            'kd': position
        }
        url = 'https://www.lagou.com/jobs/positionAjax.json'
        pages_url = f'https://www.lagou.com/jobs/list_{position}/p-city_{J2Dict()[city]}?px=default#filterBox'

        try:
            async with session.post(url, headers=headers, params=params, data=data, cookies=self.COOKIES) as response:
                re_dict = await response.json()
                re_dict['content']['positionResult']['result'][2]['positionName']

        except:
            cookie, _ = await self.get_cookies(session, url_=pages_url)
            self.COOKIES = cookie
            async with session.post(url, headers=headers, params=params, data=data, cookies=cookie) as response:
                re_dict = await response.json()
                re_dict['content']['positionResult']['result'][2]['positionName']

        for each in self.get_Jobinfo(re_dict):
            yield each

    async def get_cookies(self, session, url_: str, iftotal=False):
        lua_ = '''
        function main(splash)
            local treat = require("treat")
            splash.images_enabled = false
            splash:go("''' + url_ + """")
            return {
                html = splash:html(),
                cookies = splash:get_cookies()
            }
        end
        """
        print(clo.green('正在获取cookies和totalPages'))
        url = 'http://0.0.0.0:8050/execute?lua_source={}'.format(quote(lua_))
        async with session.get(URL(url, encoded=False)) as res_:
            datas = await res_.json()
            if iftotal:
                html = datas['html']
                total = self.get_total(html)
                print(clo.green(str(total)))
                return {each['name']: each['value'] for each in datas['cookies']}, total

            return {each['name']: each['value'] for each in datas['cookies']}, None

    def get_total(self, html: str) -> int:
        find = Selector(text=html)
        pages = find.css('.item_con_pager span::text')
        return int(pages[-2].get().strip()) if pages else 2

    def get_Jobinfo(self, json: Mapping[str, str], keyword: str = None) -> Tuple:
        """

        :param json     : 得到的json数据
        :param keyword  : 过滤关键词, defaults to None
        :yield          : 给csv写入文件的内容
        :rtype          : tuple
        """
        datas_re = re_cmp(f'{keyword}')  # 工作类型过滤关键词
        position_re = json['content']['positionResult']['result']
        filter_flag = False

        for each in position_re:
            name = each['positionName']
            salary = each['salary']
            types = [each['firstType'], each['secondType'], each['thirdType']]

            if filter_flag:
                if list(filter(datas_re.search, types)):  # 使用正则表达式判断工作类型里面有没有数据关键词
                    companyFullName = each['companyFullName']
                    companyLabelList = each['companyLabelList']
                    companySize = each['companySize']
                    businessZones = each['businessZones']

                    subwayline = each['subwayline']
                    stationname = each['stationname']
                    linestaion = each['linestaion']

                    url = f"https://www.lagou.com/jobs/{each['positionId']}.html"
                    yield (name, salary, types, companyFullName, companyLabelList, companySize, businessZones, subwayline, stationname, linestaion, url)
                else:  # 说明这个工作类型没有包含数据关键词
                    continue

            else:
                companyFullName = each['companyFullName']
                companyLabelList = each['companyLabelList']
                companySize = each['companySize']
                businessZones = each['businessZones']

                subwayline = each['subwayline']
                stationname = each['stationname']
                linestaion = each['linestaion']

                url = f"https://www.lagou.com/jobs/{each['positionId']}.html"
                yield (name, salary, types, companyFullName, companyLabelList, companySize, businessZones, subwayline, stationname, linestaion, url)

    @timer
    def run(self, position, city):
        csv_headers = [
            'name',
            'salary',
            'types',
            'companyFullName',
            'companyLabelList',
            'companySize',
            'businessZones',
            'subwayline',
            'stationname',
            'linestaion',
            'url'
        ]

        async def Spider2Csv(position, city, fileWriter):
            pages_url = f'https://www.lagou.com/jobs/list_{position}/p-city_{J2Dict()[city]}?px=default#filterBox'
            async with ClientSession() as session:
                cookies, total = await self.get_cookies(session=session, url_=pages_url, iftotal=True)
                self.COOKIES = cookies
                for i in range(1, total+1):
                    async for each in self.fetch_html(session=session, page=i, position=position, city=city):
                        fileWriter.writerow(each)
                    print(clo.red(f'第[page{i}]'))

        async def main():
            with open(f'results/{position}_{city}.csv', 'w', encoding='utf-8', newline='') as fp:
                # 如果考虑移植性的话这个path是一个问题
                writer = csv.writer(fp, csv_headers)
                writer.writerow(csv_headers)
                await Spider2Csv(position=position, city=city, fileWriter=writer)
                print(clo.green('写入完成'))

        asyncio.run(main())


if __name__ == "__main__":
    AioSplash('go', '北京')
