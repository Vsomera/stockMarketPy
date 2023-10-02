import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()

# creates orders table
c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id TEXT NOT NULL,
        order_type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        order_date DATE NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')

# creates stocks table
c.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_price REAL NOT NULL,
        purchase_date DATE NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')

conn.commit()
conn.close()
