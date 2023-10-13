from sqlalchemy import Column, Integer, String, Float, DateTime
from base import Base
import datetime

# Defines the stock table
class Stock(Base):
    ''' Stock '''
    
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    trace_id =Column(String(250), nullable=False)
    symbol = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, trace_id, symbol, name, quantity, purchase_price):
        ''' Initializes a stock to add to list '''
        self.trace_id = trace_id
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        ''' Dict representation of stock information '''
        dict = {}
        dict['id'] = self.id
        dict['trace_id'] = self.trace_id
        dict['symbol'] = self.symbol
        dict['name'] = self.name
        dict['quantity'] = self.quantity
        dict['purchase_price'] = self.purchase_price
        dict['date_created'] = self.date_created

        return dict