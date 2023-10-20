import psycopg2


#connect to the database
conn = psycopg2.connect(
    database="my_pg_db",
    user="postgres",
    password="password",
    host="localhost",  # Use "localhost" or "127.0.0.1" here
    port="5432"
)

#create a cursor
cur =conn.cursor()



# Execute a command: this creates a new table
create_table_query = '''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);
'''

cur.execute(create_table_query)
conn.commit()

cur.close()
conn.close()
