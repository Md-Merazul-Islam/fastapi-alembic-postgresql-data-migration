from fastapi import FastAPI
from app.product.router import router as product_router
from app.auth.router import router as auth_router

app = FastAPI()
app.include_router(product_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
  return {"Message":"Hello how are you?"}