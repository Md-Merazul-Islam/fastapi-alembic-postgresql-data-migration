from sqlalchemy.orm import Session
from app.product.model import Product


class ProductRepository:
    def create(self, db: Session, data):
        product = Product(**data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def get_all(self, db: Session):
        return db.query(Product).order_by(Product.created_at.desc()).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(Product).filter(Product.id == id).first()

    def delete(self, db: Session, id: int):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            return None
        db.delete(product)
        db.commit()
        return product

    def update_data(self, db: Session, id: int, data):
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
