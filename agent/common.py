import json

def dataReturn(code: int, msg: str | int, data=None):
    if data != None:
        return {'code': code, 'msg': msg, 'data': data}
    else:
        return {'code': code, 'msg': msg, 'data': data}

