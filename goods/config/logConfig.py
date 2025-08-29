import logging
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os
import traceback
from flask import request, make_response, Response


# --------------------------
# 自定义JSON格式化器
# --------------------------
class JsonFormatter(logging.Formatter):
    # 系统保留字段列表
    _reserved_fields = {
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
        'message', 'msg', 'name', 'pathname', 'process', 'processName',
        'relativeCreated', 'stack_info', 'thread', 'threadName'
    }

    def format(self, record):
        # 提取用户自定义字段
        extra_data = {
            key: value
            for key, value in record.__dict__.items()
            if key not in self._reserved_fields
        }

        # 构建日志数据结构
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            **extra_data  # 关键修改：正确合并用户字段
        }

        try:
            return json.dumps(log_data, ensure_ascii=False, default=str)
        except Exception as e:
            fallback = {
                "timestamp": datetime.now().isoformat(),
                "level": "ERROR",
                "message": f"日志格式化失败: {str(e)}",
                "original_message": log_data.get("message")
            }
            return json.dumps(fallback)

# --------------------------
# 日志配置
# --------------------------
def setup_logger():
    logger = logging.getLogger('flask_app')
    logger.setLevel(logging.DEBUG)

    # 清除旧处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 统一使用JSON格式化器
    formatter = JsonFormatter()

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出
    os.makedirs("logs", exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        'logs/app.log',
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
# --------------------------
# 请求/响应处理
# --------------------------
def extract_request_info(sensitive_fields=('password',)):
    try:
        info = {
            "method": request.method,
            "path": request.path,
            "query": dict(request.args),
            "remote_addr": request.remote_addr,
            "timestamp": datetime.now().isoformat()
        }

        # 处理headers
        info["headers"] = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ['authorization', 'cookie']
        }

        # 处理请求体
        if request.is_json:
            info["body"] = _filter_sensitive_data(
                request.get_json(silent=True) or {},
                sensitive_fields
            )
        elif request.content_type == 'application/x-www-form-urlencoded':
            info["form"] = _filter_sensitive_data(
                request.form.to_dict(),
                sensitive_fields
            )
        else:
            info["body"] = str(request.get_data())[:500]

        return info
    except Exception as e:
        logging.error(f"请求解析失败: {str(e)}", exc_info=True)
        return {"error": str(e)}

def _filter_sensitive_data(data, fields):
    """递归过滤敏感字段"""
    if isinstance(data, dict):
        return {
            k: '******' if k in fields else _filter_sensitive_data(v, fields)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_filter_sensitive_data(item, fields) for item in data]
    return data

# --------------------------
# 日志装饰器
# --------------------------
def web_log(log_request=True, log_response=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 记录请求开始
            request_info = extract_request_info() if log_request else {}
            logger.info(
                "Request Start",
                extra={
                    "type": "request",
                    "phase": "start",
                    "endpoint": func.__name__,
                    "request": request_info
                }
            )

            try:
                result = func(*args, **kwargs)
                response_info = _process_response(result) if log_response else {}
                # 智能处理HTML响应
                if response_info['headers']['Content-Type'].startswith('text/html'):
                    response_info['body'] = {
                        "note": "HTML content simplified"
                    }
                logger.info(
                    "Request Finish",
                    extra={
                        "type": "request",
                        "phase": "end",
                        "endpoint": func.__name__,
                        "response": response_info
                    }
                )
                return result
            except Exception as e:
                logger.error(
                    "Request Failed",
                    extra={
                        "type": "error",
                        "endpoint": func.__name__,
                        "error": {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc()
                        },
                        "request": request_info
                    }
                )
                raise
        return wrapper
    return decorator

def _process_response(result):
    """处理响应数据"""
    try:
        if isinstance(result, tuple):
            response = make_response(result[0])
            if len(result) > 1 and isinstance(result[1], int):
                response.status_code = result[1]
            if len(result) > 2 and isinstance(result[2], dict):
                response.headers.update(result[2])
        elif isinstance(result, Response):
            response = result
        else:
            response = make_response(result)

        return {
            "status": response.status_code,
            "headers": dict(response.headers),
            "body": _safe_response_data(response)
        }
    except Exception as e:
        return {"error": str(e)}

def _safe_response_data(response):
    """安全提取响应内容"""
    try:
        if response.headers.get('Content-Type', '').startswith('application/json'):
            return response.get_json()
        return str(response.get_data())[:1000]
    except:
        return "[unreadable data]"