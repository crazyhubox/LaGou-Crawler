from component.Ajax_requests import get_json, cookies_splash
from component.Recruitment import Recruitment,clo
from component.tools import J2Dict
from typing import Mapping
import csv

class SplashParse(Recruitment):
    
    # def __init__(self, position, city=None, filter_=False):
    #     self.position = position
    #     self.city = city
    #     self._city = J2Dict()[city]
    #     self._filter = filter_
    #     self.sha_id = self.getIdentity(self.position + self.city)
        
    
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
                    cookies_ = self.Cookies
                    josb_json = get_json(
                        url=ajax_url, cookies=cookies_, page=i, position=position, city=city)

                for each in self.get_Jobinfo(josb_json):
                    writer.writerow(each)

                redis.set(self.sha_id, i)
                print(('='*50), clo.green(f'[page{i}]'))
    
    
    def mian(self):
        cookies_, pagetotal = self.cookieProducter.getCookiesTotalPage()
        if not cookies_:
            raise ValueError('No cookies get')
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
        rdb, start_page = self.get_lastPage()
        self.csv_data(
            redis_=rdb,
            cookies=cookies_,
            headers=csv_headers,
            startPage=start_page,
            lastPage=pagetotal
        )
    
    
    @property    
    def Cookies(self):
        return cookies_splash()
    
    
    
if __name__ == "__main__":
    SplashParse('hadoop','上海').mian()