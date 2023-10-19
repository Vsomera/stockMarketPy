import mysql.connector

db_conn = mysql.connector.connect(
    host="ec2-3-142-46-177.us-east-2.compute.amazonaws.com", # connecting to vm
    # host="localhost", 
    user="root",
    password="Password123!",
    # database="storage",
    database="events", # connecting to vm
    auth_plugin='mysql_native_password' 
)

db_cursor = db_conn.cursor()


# Create orders table
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        trace_id VARCHAR(255) NOT NULL,
        stock_id VARCHAR(255) NOT NULL,
        order_type VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')

# Create stocks table
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        trace_id VARCHAR(255) NOT NULL,
        symbol VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        purchase_price DECIMAL(10, 2) NOT NULL,
        date_created VARCHAR(100) NOT NULL
    )
''')


db_conn.commit()
db_conn.close()