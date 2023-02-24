import pandas as pd
import pyodbc
print("1")
# Import CSV
data = pd.read_csv(r'Menu hours.csv')
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
		CREATE TABLE menuhours (
			store_id nvarchar(50),
			 day int,
			start_time nvarchar(50),
			end_time nvarchar(50)
			)
               ''')
print("4")
# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO menuhours (store_id, day, start_time, end_time)
                VALUES (?,?,?)
                ''',
                   row.store_id,
                   row.day,
                   row.start_time_local,
                   row.end_time_local
                   )
conn.commit()
print("5")