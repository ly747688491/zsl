import argparse
import os
import sys
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    应用配置
    """
    app_env: str = 'dev'
    app_name: str = 'FasAPI'
    app_root_path: str = '/dev-api'
    app_host: str = '0.0.0.0'
    app_port: int = 9099
    app_version: str = '1.0.0'
    app_reload: bool = True


class JwtSettings(BaseSettings):
    """
    Jwt配置
    """
    jwt_secret_key: str = 'b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55'
    jwt_algorithm: str = 'HS256'
    jwt_expire_minutes: int = 1440
    jwt_redis_expire_minutes: int = 30


class DataBaseSettings(BaseSettings):
    """
    数据库配置
    """
    db_host: str = '127.0.0.1'
    db_port: int = 3306
    db_username: str = 'caiqian'
    db_password: str = 'Liy_0123'
    db_database: str = 'test_temp'


class RedisSettings(BaseSettings):
    """
    Redis配置
    """
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_username: str = ''
    redis_password: str = 'Liy_0123'
    redis_database: int = 1


class GetConfig:
    """
    获取配置
    """

    def __init__(self):
        self.parse_cli_args()

    @lru_cache()
    def get_app_config(self):
        """
        获取应用配置
        """
        # 实例化应用配置模型
        return AppSettings()

    @lru_cache()
    def get_jwt_config(self):
        """
        获取Jwt配置
        """
        # 实例化Jwt配置模型
        return JwtSettings()

    @lru_cache()
    def get_database_config(self):
        """
        获取数据库配置
        """
        # 实例化数据库配置模型
        return DataBaseSettings()

    @lru_cache()
    def get_redis_config(self):
        """
        获取Redis配置
        """
        # 实例化Redis配置模型
        return RedisSettings()

    @staticmethod
    def parse_cli_args():
        """
        解析命令行参数
        """
        if 'uvicorn' in sys.argv[0]:
            # 使用uvicorn启动时，命令行参数需要按照uvicorn的文档进行配置，无法自定义参数
            pass
        else:
            # 使用argparse定义命令行参数
            parser = argparse.ArgumentParser(description='命令行参数')
            parser.add_argument('--env', type=str, default='', help='运行环境')
            # 解析命令行参数
            args = parser.parse_args()
            # 设置环境变量，如果未设置命令行参数，默认APP_ENV为dev
            os.environ['APP_ENV'] = args.env if args.env else 'dev'
        # 读取运行环境
        run_env = os.environ.get('APP_ENV', '')
        # 运行环境未指定时默认加载.env.dev
        env_file = '.env.dev.dev'
        # 运行环境不为空时按命令行参数加载对应.env文件
        if run_env != '':
            env_file = f'.env.dev.{run_env}'
        # 加载配置
        load_dotenv(env_file)


# 实例化获取配置类
get_config = GetConfig()
# 应用配置
AppConfig = get_config.get_app_config()
# Jwt配置
JwtConfig = get_config.get_jwt_config()
# 数据库配置
DataBaseConfig = get_config.get_database_config()
# Redis配置
RedisConfig = get_config.get_redis_config()
