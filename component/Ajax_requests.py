from typing import Dict, Mapping
import requests
from color import Colored
from urllib.request import quote
clo = Colored()


def get_json(url, cookies: Mapping[str, str], page:str, position: str, city: str = None) -> Dict[str,str]:
    """这个文件接收cookies和页数，请求Ajax数据
    Args:
        cookies (dict): cookies
        page (int): 页数

    Returns:
        dict: 从json格式的字符串用response的json方法直接转成字典，就不用使用json库了
    """
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
        # ('city', city.encode('unicode_escape').decode()),
        ('city', city),
        ('needAddtionalResult', 'false'),
    )

    data = {
        'first': 'true',
        'pn': f"{page}",
        'kd': position
    }

    response = requests.post('https://www.lagou.com/jobs/positionAjax.json',
                             headers=headers, params=params, data=data, cookies=cookies)
    print(
        f'https://www.lagou.com/jobs/positionAjax.json[page{page} {clo.green(str(response.status_code))}]')

    return response.json()


# def cookies_splash(position,city):
def cookies_splash():
    # lua_  = """
    # function main(splash)
    #     local treat = require("treat")
    #     splash:go("https://www.lagou.com/jobs/list_{}/p-city_{}?px=default#filterBox")""".format(position,city)+"""
    #     return {
    #         html = splash:html(),
    #         cookies = splash:get_cookies(),
    #     }
    # end
    # """
    # lua_  = """
    # function main(splash)
    #     local treat = require("treat")
    #     splash:go("https://httpbin.org/ip")
    #     return {
    #         html = splash:html(),
    #         cookies = splash:get_cookies(),
    #     }
    # end
    # """
    lua_ = """
    function main(splash)
        local treat = require("treat")
        splash:go("https://www.lagou.com/jobs/list_%E4%B8%8A%E6%B5%B7?labelWords=&fromSearch=true&suginput=")
        return {
            splash:get_cookies()
        }
    end
    """
    url = 'http://0.0.0.0:8050/execute?lua_source={}'.format(quote(lua_))
    # print(url)
    res_ = requests.get(url)
    cookies_data = res_.json()
    # print(datas)
    # print(clo.yellow('得到Cookies'))
    # print(res_.text)
    return {each['name']:each['value'] for each in cookies_data['1']}



if __name__ == "__main__":
    cookies = cookies_splash()
    print(cookies)
    # json = get_json('1',cookies=cookies,page='1',city='上海',position='python')
    # print(json)
    
    
