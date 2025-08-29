import os
import yaml
from goods.common.utils import merge_configs

def Configure(func):
    def wrapper(*args, **kwargs):
        sep = os.sep # 即：/
        #项目根路径
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        #项目框架路径
        thinkpython_path = os.getcwd() + sep
        with open(file=thinkpython_path + 'resources/application.yml', mode="r", encoding='utf-8') as file:
            cfg = yaml.safe_load(file)

        cfg['sep'] = sep
        cfg['thinkpython_path'] = thinkpython_path

        if cfg['profiles']['active'] != None:
            config_env = f"application-{cfg['profiles']['active']}.yml"
            with open(file=root_path + sep + 'resources/' + config_env, mode='r', encoding='utf-8') as config_env_file:
                runtime_config = yaml.safe_load(config_env_file)
                cfg = merge_configs(cfg, runtime_config)

        return func(cfg, *args, **kwargs)
    return wrapper
