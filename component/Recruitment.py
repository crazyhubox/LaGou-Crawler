import csv
from re import compile as re_cmp
from typing import Mapping
from redis import Redis
from component.Get_cookies import GetCookies
from component.Ajax_requests import get_json, clo
from component.tools import J2Dict
from hashlib import sha1


class Recruitment:

    def __init__(self, position, city=None, filter_=False):
        self.position = position
        self.city = city
        self._city = J2Dict()[city]
        self._filter = filter_
        self.url = f'https://www.lagou.com/jobs/list_{position}/p-city_{self._city}?px=default#filterBox'
        self.cookieProducter = GetCookies(self.url)
        self.sha_id = self.getIdentity(self.position + self.city)

    def main(self):
        ...

    def csv_data(self,
                 redis_,
                 headers: Mapping[str, str],
                 cookies: Mapping[str, str],
                 startPage: int,
                 lastPage: int
                 ) -> None:
        start_page = startPage
        last_page = lastPage + 1
        csv_headers = headers
        cookies_ = cookies
        position = self.position
        city = self._city
        city_name = self.city
        redis = redis_
        ajax_url = self.url

        print(clo.blue(str(start_page)), clo.blue(str(last_page)))

        with open(f'results/{position}_{city_name}.csv', 'w', encoding='utf-8', newline='') as fp:
            # 如果考虑移植性的话这个path是一个问题
            writer = csv.writer(fp, csv_headers)
            writer.writerow(csv_headers)
            for i in range(start_page, last_page):
                try:  # 请求几次之后Ajax接口返回异常，cookies过期，重新获取一下
                    josb_json = get_json(
                        url=ajax_url, cookies=cookies_, page=i, position=position, city=city)
                    for _ in josb_json['content']['positionResult']['result']:
                        pass
                except:
                    cookies_ = self.cookieProducter.cookies()
                    josb_json = get_json(
                        url=ajax_url, cookies=cookies_, page=i, position=position, city=city)

                for each in self.get_Jobinfo(josb_json):
                    writer.writerow(each)

                redis.set(self.sha_id, i)
                print(('='*50), clo.green(f'[page{i}]'))

    def getIdentity(self, key: str) -> str:
        return sha1((key).encode()).hexdigest()

    def get_lastPage(self) -> Redis:
        """从redis数据中读取上次爬取到的页数,根据kw和cty生成指纹"""
        id_ = self.sha_id
        redis = Redis(host='127.0.0.1', password='130298', db=1)
        if not redis.get(id_):
            redis.set(id_, 1)
            start_page = 1
        else:
            start_page = int(redis.get(id_))
        return redis, start_page

    def get_Jobinfo(self, json: Mapping[str, str], keyword: str = None):
        """

        :param json     : 得到的json数据
        :param keyword  : 过滤关键词, defaults to None
        :yield          : 给csv写入文件的内容
        :rtype          : tuple
        """
        datas_re = re_cmp(f'{keyword}')  # 工作类型过滤关键词
        position_re = json['content']['positionResult']['result']
        filter_flag = self._filter

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


if __name__ == "__main__":
    # Recruitment('软件工程师','上海')
    test_str = '上海'
    test_str1 = 'python'

    # 8bfb939edc76165ba59f962b79bc5535b0f3a68c
    # bdd541b4402074c3e047ee01c509afe4cc605688
