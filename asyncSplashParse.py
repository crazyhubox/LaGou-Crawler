from component.aio_splash import clo,AioSplash
from concurrent.futures import ThreadPoolExecutor,wait
from component.tools import Demands


class AsyncSplashParse(AioSplash):
    
    def __init__(self,position:str,city:str):
        super().__init__(position=position,city=city)



def task(position:str,city:str)->None:
    AsyncSplashParse(position=position,city=city)


def main():
    path = '/Users/crazyhubox/Desktop/Recruitment/Demands.json'
    demands = Demands(path=path)
    need_size = demands['demands_size']
    ds = demands['demands']
    print(clo.green('需求列表读取成功'))
    with ThreadPoolExecutor(max_workers=need_size) as t:
        all_tasks = [t.submit(task, *(each['position'], each['city']))
                     for each in ds]
        wait(all_tasks)
        print('finished')

if __name__ == "__main__":
    main()

    # TODO 在flask当中post一个json列表，读取列表开启爬虫
    # TODO 爬取日志保存为文件
    
    # 日志格式:
        # [时间-职位-地点]********************************
        # 内容

    # json格式:Demands格式\
        
        
        
        