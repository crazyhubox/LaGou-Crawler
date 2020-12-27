from component.Recruitment import Recruitment, J2Dict, clo
from concurrent.futures import ThreadPoolExecutor, wait
from component.tools import Demands

from time import time
now = lambda:time()
def timer(func):
    start = now()
    def newfunc(*ars,**kw):
        res = func(*ars,**kw)
        print(clo.yellow(f'time:{now()-start}'))
        return res
    return newfunc

class SyncParse(Recruitment):
    def __init__(self, position, city=None, filter_=False):
        super().__init__(position, city)
        self.main()

    def main(self):
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




def task(position_: str, city_: str) -> None:
    SyncParse(position=position_, city=city_)


@timer
def main():
    demands = Demands('./Demands.json')
    need_size = demands['demands_size']
    ds = demands['demands']
    print(clo.green('需求列表读取成功'))
    with ThreadPoolExecutor(max_workers=need_size) as t:
        all_tasks = [t.submit(task, *(each['position'], each['city']))
                     for each in ds]
        wait(all_tasks)
        print('finished')

if __name__ == "__main__":
    # a,b = SyncParse('保险实习','广州').get_lastPage()
    # print(a,b)
    
    main()
    # 多线程的错误捕获?