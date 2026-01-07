from fastapi import FastAPI
from app.product.router import router as product_router

app = FastAPI()
app.include_router(product_router)


@app.get("/")
def read_root():
  return {"Message":"Hello how are you?"}