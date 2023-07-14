from typing import Dict, List

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from nonebot import get_driver
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from .config import Config, __version__

__plugin_meta__ = PluginMetadata(
    name="MongoDB",
    description="基于 MongoDB ODM 的数据库管理插件",
    usage="无",
    type="library",
    homepage="https://github.com/Well2333/nonebot-plugin-mongodb",
    config=Config,
    extra={
        "author": "Well404",
        "version": __version__,
        "priority": 1,
    },
)

from .config import plugin_config


class Mongo:
    _client: AsyncIOMotorClient = None

    @classmethod
    def client(cls) -> AsyncIOMotorClient:
        """client of mongodb"""
        if cls._client:
            return cls._client
        try:
            logger.info("Initializing MongoDB Client ...")
            cls._client = AsyncIOMotorClient(plugin_config.mongo_uri)
        except Exception as e:
            raise RuntimeError("MongoDB Client initialization failed") from e

        # if cls._client.get(plugin_config.mongo_database_name)

    @classmethod
    async def _register_models(cls, document_models: List[Document]):
        cls.client()
        database = getattr(cls._client, plugin_config.mongo_database_name)
        await init_beanie(database, document_models=document_models)


driver = get_driver()


@driver.on_startup
async def startup_db():
    document_models = Document.__subclasses__()
    if not document_models:
        raise RuntimeError("No valid Document subclass found")

    # check duplicate models
    document_names: Dict[str, str] = {}
    for cls in document_models:
        cls_path = f"{cls.__module__}.{cls.__name__}"
        try:
            cls_name = cls.Settings.name.lower()
        except Exception as e:
            cls_name = cls.__name__.lower()
        if cls_name in document_names:
            clashed_cls_path = document_names[cls_name]
            raise RuntimeError(
                f"Duplicate Document name: {cls_name} form {cls_path} and {clashed_cls_path}"
            )
        else:
            document_names[cls_name] = cls_path

    logger.debug(
        "Initializing MongoDB Documents:\n"
        + "\n".join(
            [
                f"{cls_name} (from {cls_path})"
                for cls_name, cls_path in document_names.items()
            ]
        )
    )

    await Mongo._register_models(document_models)
