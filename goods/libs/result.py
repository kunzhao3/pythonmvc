from goods.libs.httpResponse import HttpResponse
from goods.libs.statusCode import StatusCode


class Result(HttpResponse):
    @staticmethod
    def success(code=StatusCode.OK.value, msg='操作成功', data=[], mimetype="application/json", headers=None, ensure_ascii = False):
        result = {
            'code': code,
            'msg': msg,
            'data': data
        }

        return HttpResponse.setResponse(data=result, code=HttpResponse.getResponseStatus(), mimetype=mimetype, headers=headers, ensure_ascii = ensure_ascii)

    @staticmethod
    def error(code = 0, msg='操作失败', data=[],  mimetype="application/json", headers=None, ensure_ascii = False):
        result = {
            'code': code,
            'msg': msg,
            'data':data
        }
        return HttpResponse.setResponse(data=result, code=HttpResponse.getResponseStatus(), mimetype=mimetype, headers=headers, ensure_ascii=ensure_ascii)

    @staticmethod
    def http_error(code, msg='操作失败', data=[]):
        result = {
            'code': code,
            'msg': msg,
            'data':data
        }
        return HttpResponse.setHtmlResponse(data=result, code=code)

    @staticmethod
    def upload_success(code=0, msg='操作成功', data=[], mimetype="application/json", headers=None, ensure_ascii = False):
        result = {
            'errno': code,
            'message': msg,
            'data': data
        }
        return HttpResponse.setResponse(data=result, code=HttpResponse.getResponseStatus(), mimetype=mimetype, headers=headers, ensure_ascii = ensure_ascii)

    @staticmethod
    def upload_error(code=1, msg='操作失败', data=[], headers=None, ensure_ascii = False):
        result = {
            'errno': code,
            'message': msg,
            'data':data
        }
        return HttpResponse.setResponse(data=result, code=HttpResponse.getResponseStatus(), headers=headers, ensure_ascii=ensure_ascii)

    @staticmethod
    def text_success(code=StatusCode.OK.value, data='', mimetype="text/plain", headers=None, ensure_ascii = False):
        return HttpResponse.setTextResponse(data=data, code=HttpResponse.getResponseStatus(), mimetype=mimetype, headers=headers, ensure_ascii = ensure_ascii)