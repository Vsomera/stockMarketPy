from sqlalchemy import Column, Integer, String, Float, DateTime
from base import Base
import datetime

# Defines the stock table
class Stock(Base):
    ''' Stock '''
    
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_date = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, symbol, name, quantity, purchase_price, purchase_date):
        ''' Initializes a stock to add to list '''
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date 
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        ''' Dict representation of stock information '''
        dict = {}
        dict['id'] = self.id
        dict['symbol'] = self.symbol
        dict['name'] = self.name
        dict['quantity'] = self.quantity
        dict['purchase_price'] = self.purchase_price
        dict['purchase_date'] = self.purchase_date
        dict['date_created'] = self.date_created

        return dict