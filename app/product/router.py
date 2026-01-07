from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, File, UploadFile
from sqlalchemy.orm import Session
from app.product.service import ProductService
from app.core.database import get_db, SessionLocal
from app.product.schema import ProductCreate, ProductRead, ProductUpdate
import pandas as pd
import os

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


# background  excel upload
def process_excel(file_path: str):
    db = SessionLocal()
    try:
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            if pd.isna(row["name"]) or pd.isna(row["price"]):
                continue
            product_data = ProductCreate(name=row["name"], price=row["price"])
            service.create(db, product_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@router.post("/upload-excel")
async def upload_execl(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Invalid file format")

    tmp_file = f"tmp_{file.filename}"
    with open(tmp_file, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(process_excel, tmp_file)
    return {"message": "File uploaded successfully"}
