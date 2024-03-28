from typing import Literal
import patito as pt

class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    name: str
    temperature_zone: Literal["dry", "cold", "frozen"]
    demand_percentage: float = pt.Field(constraints=pt.field.sum() == 100.0)

data = dict(
        product_id=1,
        name="apple",
        temperature_zone="cold",
        demand_percentage=50
    )
