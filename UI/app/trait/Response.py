# 响应工具
import json
class Response():
    @staticmethod
    def jsonReturn(code:int,msg:str|int,data=None):
        if data != None:
            return json.dumps({'code':code,'msg':msg,'data':data})
        else:
            return json.dumps({'code':code,'msg':msg,'data':data})