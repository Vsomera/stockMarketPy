from sqlalchemy import Column, Integer, String, Float, DateTime
from base import Base
import datetime

# Define the 'orders' table
class Order(Base):
    ''' Orders '''

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    trace_id =Column(String(250), nullable=False)
    stock_id = Column(String(250), nullable=False)
    order_type = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_date = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, trace_id, stock_id, order_type, quantity, price, order_date):
        ''' Initializes a stock order '''
        self.stock_id = stock_id
        self.trace_id = trace_id
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.order_date = order_date
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        ''' Dict representation of stock order information '''
        dict = {}
        dict['id'] = self.id
        dict['trace_id'] = self.trace_id
        dict['stock_id'] = self.stock_id
        dict['order_type'] = self.order_type
        dict['quantity'] = self.quantity
        dict['price'] = self.price
        dict['order_date'] = self.order_date
        dict['date_created'] = self.date_created

        return dict