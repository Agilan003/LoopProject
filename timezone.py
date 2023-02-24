import pandas as pd
import pyodbc
print("1")
# Import CSV
data = pd.read_csv(r'bq-results-20230125-202210-1674678181880.csv')
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
		CREATE TABLE timezones (
			store_id nvarchar(50),
			 timezone nvarchar(50)
			)
               ''')
print("4")
# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO timezones (store_id, timezone)
                VALUES (?,?)
                ''',
                   row.store_id,
                   row.timezone_str
                   )
conn.commit()
print("5")