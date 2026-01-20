from datetime import datetime

from domain import BaseEntity

class CoursesModel(BaseEntity):
    name: str
    last_price: float
    best_bid_price: float
    best_ask_price: float
    created_at: datetime