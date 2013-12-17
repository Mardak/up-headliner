import os
import sys
import logging
import json
from up.headliner import settings, DEFAULT_CONFIG_FILEPATH

class SettingsObj(object):
    def __init__(self, **settings):
        self.__dict__.update(settings)

def __read_config_file(options=None):
    # read default config
    config_obj = SettingsObj()
    config_obj.server = settings.server 
    config_obj.redis = settings.redis
    config_obj.providers = settings.providers
    config_obj.message_broker = settings.message_broker
    config_obj.scheduler = settings.scheduler
    config_obj.tasks = settings.tasks

    if options is None:
        options = SettingsObj()
        options.config = None

    # load external JSON
    if os.path.isfile(DEFAULT_CONFIG_FILEPATH) or options.config:
        file_path = DEFAULT_CONFIG_FILEPATH
        if options.config and os.path.isfile(options.config):
            file_path = option.config
        with open(file_path, "r") as config_file:
            config = json.load(config_file)

        if config.get('server') and config.get('storage'):
            sys_settings = SettingsObj(**config)
            config_obj.server['host'] = sys_settings.server.get('host', "127.0.0.1")
            config_obj.server['port'] = sys_settings.server.get('port', 4355)
            config_obj.server['debug'] = sys_settings.server.get('debug', False)
            config_obj.redis['host'] = sys_settings.redis.get('host', '127.0.0.1')
            config_obj.redis['port'] = sys_settings.redis.get('port', 6379)
            config_obj.redis['database'] = sys_settings.redis.get('database', 0)
            config_obj.redis['user'] = sys_settings.redis.get('user', None)
            config_obj.redis['password'] = sys_settings.redis.get('password', None)

    return config_obj

def setup_basic_logger(loglevel=None):
    loglevel = loglevel or logging.DEBUG
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(loglevel)

    fmt = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(fmt)

    logger = logging.getLogger("headliner")
    logger.addHandler(handler)
    logger.setLevel(loglevel)
