import mysql.connector

db_conn = mysql.connector.connect(
    host="ec2-3-143-231-139.us-east-2.compute.amazonaws.com",
    # host="localhost", 
    user="root",
    password="Password123!",
    # database="storage",
    database="events",
)

db_cursor = db_conn.cursor() 


# Drops both orders and stocks table
db_cursor.execute(''' 
                  DROP TABLE orders, stocks 
                  ''') 
 
db_conn.commit() 
db_conn.close()