# patito-playground

A package with entrypoints that demonstrate stand-alone tasks using patito,
the Pydantic/Polars hybrid DataFrame data model library, which now supports
Pydantic v2 (since v0.6.1).

## What's Patito for?

The key feature of patito is that the Pydantic data model doubles as the schema
for a Polars DataFrame. Patito's schema is more expressive than Pydantic's.

Its fields are constructed from internal Pydantic models (`ColumnInfo` in `pt._pydantic`),
where the arguments are:
- `constraints`
- `derived_from`
- `unique`
However these are for internal use, they are illustrative at what Patito adds though.

Derived columns are those which would be constructed 'at runtime' (i.e. after ingestion)
from other values. They're commonly expressed in Pydantic through computed fields,
though this can make things a bit verbose (e.g. a simple "take the value and double it").

'Derived columns' in Patito are specified with a Polars expression that's triggered
when the `pt.DataFrame.derive` hook is called (again this is just internal details).

'Unique' is a simple common constraint: all row values must be unique.

## Example workflows

### 1) Validating a database of products

In a database of products, you'd expect

- product IDs to be unique,
- some string-typed columns might be a restricted set of choices
  (which Python has `Enum` or `Literal` to express),
- percentages would sum to 100.0%

```py
import patito as pt

class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    name: str
    temperature_zone: Literal["dry", "cold", "frozen"]
    demand_percentage: float = pt.Field(constraints=pt.field.sum() == 100.0)
```

Patito has a nice trick for the expressions used in the last of these.
It aliases `pt.field` to become `pt.col("_")` and is then replaced with the field name,
so you get a nice shorthand for the column name to use in expressions, a bit like `self`.

I like Pydantic models for progressively whittling out the shape of a dataset (or
making the 'map' to the 'territory' of the underlying dataset values' ground truth).
Typically, if your data model's wrong (your map isn't quite right somehow), you'll get a single error,
and often not even an informative one. A key design feature of Pydantic is that validation errors
aren't collected until all data was validated, so at the individual data point level
(e.g. an individual product) you would see all the ways it was invalid not just the first
one to trip the error handling cascade.

In practice, this means you can iterate: if you solve a little problem, you see its
report disappear, and you can tell you're moving in the right direction. In this case,
you might be adding string values to the `Literal` one by one and re-running (if
there are tons of error messages this might make it more feasible to tackle at all).

What might be unfamiliar here is that **Patito models aren't validated upon ingestion**.
Look again at the last field and you can see why: it doesn't make sense to validate dataset-level
constraints on a single element of a dataset, in this case whether the sum of values adds up to 100%.
(The only situation that'd work in would be the unrealistic trivial case of a dataset of 1 item).
