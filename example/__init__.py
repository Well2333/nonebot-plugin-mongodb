from typing import Optional

from beanie import Document, Indexed
from nonebot import get_driver, require
from pydantic import BaseModel

require("nonebot_plugin_mongodb")


class Category(BaseModel):
    name: str
    description: str


class Product(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(
        float
    )  # You can also specify that a field should correspond to an index
    category: Category  # You can include pydantic models as well
    
    class Settings:
        name = "nonebot_plugin_mongodb.Product"

class Product2(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(
        float
    )  # You can also specify that a field should correspond to an index
    category: Category  # You can include pydantic models as well
    


driver = get_driver()


@driver.on_startup
async def example():
    chocolate = Category(
        name="Chocolate", description="A preparation of roasted and ground cacao seeds."
    )
    # Beanie documents work just like pydantic models
    tonybar = Product(name="Tony's", price=5.95, category=chocolate)
    # And can be inserted into the database
    await tonybar.insert()

    # You can find documents with pythonic syntax
    product = await Product.find_one(Product.price < 10)

    # And update them
    await product.set({Product.name: "Gold bar"})
