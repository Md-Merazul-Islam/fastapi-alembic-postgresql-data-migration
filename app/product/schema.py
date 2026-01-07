from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, constr, confloat

class ProductBase(BaseModel):
  name : constr(min_length=3, max_length=50)
  price : confloat(gt=0)


class ProductCreate(ProductBase):
  pass
  
class ProductUpdate(ProductBase):
  pass
  
class ProductRead(ProductBase):
  id : int
  created_at : datetime
  
  class Config:
    from_attributes  = True