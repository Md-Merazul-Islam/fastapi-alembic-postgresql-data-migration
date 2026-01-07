from sqlalchemy.orm import Session
from app.product.repository import ProductRepository

class ProductService:
  def __init__(self):
    self.repo = ProductRepository()
  
  def create(self, db:Session, data):
    return self.repo.create(db, data)
  
  def list_products(self, db:Session):
     return self.repo.get_all(db)
   
  def get_product_by_id(self, db:Session, id:int):
    return self.repo.get_by_id(db, id)
  
  def update_product(self, db:Session, id:int, data:dict):
    return self.repo.update_data(db, id, data)
  
  def delete_product(self, db:Session, id:int):
    return self.repo.delete(db, id)