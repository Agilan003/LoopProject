import pandas as pd
import pyodbc
print("1")
# Import CSV
data = pd.read_csv(r'store status.csv')
df = pd.DataFrame(data)
print("2")
# Connect to SQL Server
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-4KMT3JP\SQLEXPRESS;'
                      'Database=DatasetLoop;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
print("3")
# Create Table
cursor.execute('''
		CREATE TABLE activity (
			store_id nvarchar(50),
			 status nvarchar(50),
			timestamp nvarchar(50)
			)
               ''')
print("4")
# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO activity (store_id, status, timestamp)
                VALUES (?,?,?)
                ''',
                   row.store_id,
                   row.status,
                   row.timestamp_utc
                   )
conn.commit()
print("5")