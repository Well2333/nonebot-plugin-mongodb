import importlib.util
import json
import sys

# get package version
from importlib.metadata import version

from nonebot import get_driver
from pydantic import BaseModel

try:
    __version__ = version("nonebot_plugin_mongodb")
except Exception:
    __version__ = None


class Config(BaseModel):
    # general
    mongo_uri: str
    mongo_database_name: str = "nonebot2"


plugin_config = Config.parse_obj(get_driver().config)
