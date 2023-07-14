import sys

from nonebot import get_driver
from pydantic import BaseModel

# get package version
try:
    from importlib.metadata import version
except Exception:
    from importlib_metadata import version

try:
    __version__ = version("nonebot_plugin_bilichat")
except Exception:
    __version__ = None


class Config(BaseModel):
    # general
    mongo_uri: str
    mongo_database_name: str = "nonebot2"


plugin_config = Config.parse_obj(get_driver().config)
