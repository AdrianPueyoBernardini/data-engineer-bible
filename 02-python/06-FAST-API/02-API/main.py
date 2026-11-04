from fastapi import FastAPI, HTTPException, status
from typing import List
from pydantic import BaseModel


app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

products: List[Product] = [
    Product(id=1, name="Jamon", price=75, stock=10),
    Product(id=2, name="Cecina", price=90, stock=5),
    Product(id=3, name="Queso", price=5.99, stock=20)
]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/products", response_model=List[Product], summary="Get all products", description="Retrieve a list of all available products.")
def get_products():
    return products

@app.put("/products/{product_id}", response_model=Product, summary="Update a product")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return updated_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cannot update. Product with ID {product_id} not found"
    )