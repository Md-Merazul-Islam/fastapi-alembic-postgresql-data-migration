from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.product.service import ProductService
from app.core.database import get_db
from app.product.schema import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)
service = ProductService()


@router.post("/", response_model=ProductRead)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return service.create(db, product)


@router.get("/", response_model=list[ProductRead])
def list_all(db: Session = Depends(get_db)):
    return service.list_products(db)


@router.get("/{id}", response_model=ProductRead)
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        return service.get_product_by_id(db, id)
    except:
        raise HTTPException(status_code=404, detail="Product not found")


@router.put("/{id}", response_model=ProductRead)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    update = service.update_product(db, id, product)
    if not update:
        raise HTTPException(status_code=404, detail="Product not found")
    return update




@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        return service.delete_product(db, id)
    except:
        raise HTTPException(status_code=404, detail="Product not found")
