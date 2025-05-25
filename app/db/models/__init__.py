from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User  
from .products import Product
from .client import Client