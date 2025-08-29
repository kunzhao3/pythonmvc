from flask import request
def merge_configs(configBase, configEnv):
    if isinstance(configBase, dict) and isinstance(configEnv, dict):
        for key in configEnv:
            if key in configBase and isinstance(configBase[key], dict) and isinstance(configEnv[key], dict):
                merge_configs(configBase[key], configEnv[key])
            else:
                configBase[key] = configEnv[key]
    return configBase
def isPost(request = request):
    '''
    描述：判断是否是POST提交数据
    :return:bool
    '''
    method_type = request.method == 'POST'
    return method_type

def isGet(request = request):
    '''
    描述：判断是否是 GET 提交数据
    :return:bool
    '''
    method_type = request.method == 'GET'
    return method_type

def isDelete(request = request):
    '''
    描述：判断是否是 DELETE 提交数据
    :return:bool
    '''
    method_type = request.method == 'DELETE'
    return method_type

def isPut(request = request):
    '''
    描述：判断是否是 PUT 提交数据
    :return:bool
    '''
    method_type = request.method == 'PUT'
    return method_type
def getRequestJson(request = request):
    data = {}
    if request.args.to_dict():
        data = request.args.to_dict()
    return data

def postRequestJson(request = request):
    data = {}
    if request.method == 'POST' and request.get_json():
        data = request.get_json()
    return data

def postRequestByForm(request = request):
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()
    return data

def filter_xss(data):
    if data != None:
        if type(data) == list:
            for item in data:
                if type(item) == int:
                    continue
                item = item.replace('&', '&amp;')
                item = item.replace('<', '&lt;').replace('>', '&gt;')
                item = item.replace('"', '&quot;').replace("'", '&#39;')
                item = item.replace('/', '')
                item = item.replace('\\', '')
                item = item.replace('\'', '')
        else:
            data = data.replace('&', '&amp;')
            data = data.replace('<', '&lt;').replace('>', '&gt;')
            data = data.replace('"', '&quot;').replace("'", '&#39;')
            data = data.replace('/', '')
            data = data.replace('\\', '')
            data = data.replace('\'', '')
    return data
