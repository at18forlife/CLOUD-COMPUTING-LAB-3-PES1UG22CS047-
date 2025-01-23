import json
import products
from cart import dao
from products import Product
from typing import List, Optional

class Cart:
    def _init_(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @classmethod
    def load(cls, data: dict) -> 'Cart':
        return cls(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])
            for content in contents:
                temp_product = products.get_product(content)
                if temp_product:
                    items.append(temp_product)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error processing cart contents: {e}")
    
    return items

def add_to_cart(username: str, product_id: int) -> None:
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int) -> None:
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str) -> None:
    dao.delete_cart(username)
