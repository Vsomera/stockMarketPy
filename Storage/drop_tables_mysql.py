import mysql.connector

db_conn = mysql.connector.connect(
    host="localhost", 
    user="root",
    password="$apache2023%s",
    database="storage"    
)

db_cursor = db_conn.cursor() 


# Drops both orders and stocks table
db_cursor.execute(''' 
                  DROP TABLE orders, stocks 
                  ''') 
 
db_conn.commit() 
db_conn.close()