from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from component.Ajax_requests import get_json
# url = f'https://www.lagou.com/jobs/list_{}?&px=default&city={}#filterBox'

def Quiters(mode):
    def QuitDriver(func):
        def f(self,*args,**kwargs):
            try:
                res = func(self,*args,**kwargs)
                return res
            except Exception as e:
                print(e)
                return None
            finally:
                self.driver.quit()
        return f

    def Return_tp(func):#装饰器函数
        def f(self,*args,**kwargs):#新函数
            try:
                res = func(self,*args,**kwargs)
                return res
            except Exception as e:
                print(e)
                return None,None
            finally:
                self.driver.quit()
        return f

    if mode == 'quit':
        return QuitDriver
    elif mode == 'tuple':
        return Return_tp
    else:
        raise ValueError('No such decorator')

class GetCookies:
    def __init__(self, url):
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = Chrome(chrome_options=chrome_options)
    
    @Quiters('quit')
    def cookies(self):
        if self.driver:
            print('关闭创建')
            self.driver.quit()
            self.driver = Chrome()
        
        return self.__cookies()
    
    @Quiters('tuple')
    def getCookiesTotalPage(self):
        cookies = self.__cookies()
        total = self.__total()
        return cookies , total
    
    def __cookies(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        cookies = driver.get_cookies()
        cookies = self.deal_cookies(cookies)
        return cookies


    @staticmethod
    def deal_cookies(cookie_list) -> dict:
        """将从webdriver得到的cookies转化成字典"""
        return {each['name']: each['value'] for each in cookie_list}
    
    def __total(self):
        driver = self.driver
        total_page = driver.find_elements_by_css_selector('.item_con_pager span')
        total_page = total_page[-2].text if total_page else 1
        return int(total_page)
   
   
   

     
     
if __name__ == "__main__":
    url = f'https://www.lagou.com/jobs/list_心理?&px=default&city=贵阳#filterBox'
    cookies,total = GetCookies(url).getCookiesTotalPage()
    print(cookies,total)

    