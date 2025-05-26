from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models.user import User
from app.db.models.client import Client
from app.db.models.products import Product
from app.db.models.orders import Order
from app.db.models.orders import OrderItem
