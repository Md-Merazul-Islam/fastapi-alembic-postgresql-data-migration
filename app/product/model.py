from sqlalchemy import Column, Integer, String,DateTime, Float
from app.core.database import Base
from datetime import datetime
class Product(Base):
  __tablename__="products"
  id= Column(Integer,primary_key=True)
  name = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  created_at = Column(DateTime, default = datetime.utcnow,nullable=False)