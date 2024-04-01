from __future__ import annotations
from typing import Literal
from pydantic import TypeAdapter
import patito as pt

__all__ = ["Product"]

class Shop(pt.Model):
    name: str
    town: str

class Product(pt.Model):
    name: str
    place: "Shop"


def main() -> pt.DataFrame:
    data = dict(name="apple", place=dict(name="Kwik-E-Mart", town="Springfield"))
    product = Product.model_validate(data)
    print(f"Ingested a product:\n{product!r}")
    more_data = dict(name="slushee", place=dict(name="Kwik-E-Mart", town="Springfield"))
    products = TypeAdapter(list[Product]).validate_python([data, more_data])
    basket = Product.DataFrame(products)
    print(f"Ingested a basket:\n{basket}")
    basket.validate()
    print("The DataFrame was a valid Product dataset")
    return basket
