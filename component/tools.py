from json import loads
from pprint import pformat
from typing import Dict

class J2Dict:
    def __init__(self):
        from os.path import join,dirname
        path = join(dirname(__file__),'citys.json')
        with open(path,'r') as f_json:
            city_dict = loads(f_json.read())
        self._dict = city_dict
        
    def __getitem__(self,key:str) -> Dict[str,str]:
        return self._dict[key]
    
    
    def __len__(self):
        return len(self._dict)
    
    def __repr__(self) -> str:
        return pformat(self._dict)
    

class Demands(J2Dict):
    def __init__(self,path:str):
        with open(path, 'r') as f:
            demand_json = loads(f.read())
        self._dict = demand_json



if __name__ == "__main__":
    citys = J2Dict()
    print(citys['贵阳'])
    