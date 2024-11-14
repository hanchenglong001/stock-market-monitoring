from configparser import ConfigParser



class init_config():
    def __init__(self, config_file: str):
        cfg = ConfigParser()
        cfg.read(config_file, encoding='utf-8')
        self.cfg = cfg

    def get_value(self, section, key):
        if section in self.cfg:
            return self.cfg[section][key]
        else:
            raise Exception(f"配置项不存在{section}.{key}")

    def get_keys(self, section):
        keys = []
        for i in self.cfg[section]:
            keys.append(i)
        return keys

init_conf = init_config("config.ini")