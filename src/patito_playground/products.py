from typing import Literal
from pydantic import TypeAdapter
import patito as pt

__all__ = ["Product"]


class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    name: str
    temperature_zone: Literal["dry", "cold", "frozen"]
    demand_percentage: float = pt.Field(constraints=pt.field.sum() == 100.0)


def main() -> None:
    data = dict(
        product_id=1, name="apple", temperature_zone="cold", demand_percentage=50
    )
    product = Product.model_validate(data)
    print(f"Ingested a product:\n{product!r}")
    more_data = dict(
        product_id=2, name="banana", temperature_zone="dry", demand_percentage=50
    )
    products = TypeAdapter(list[Product]).validate_python([data, more_data])
    fruit_basket = Product.DataFrame(products)
    print(f"Ingested a basket:\n{fruit_basket}")
    fruit_basket.validate()
    print("The DataFrame was a valid Product dataset")
    return
