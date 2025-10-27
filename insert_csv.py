import pandas as pd
from sqlalchemy import create_engine

# Load the CSV
df = pd.read_csv("aggregated_transaction.csv")  # use the original filename

# MySQL connection string
# Replace 'root' and 'password' with your MySQL username & password
engine = create_engine("mysql+mysqlconnector://root:12345678@localhost/phonepe_insights")

# Insert data into MySQL table 'transactions'
df.to_sql(name='transactions', con=engine, if_exists='replace', index=False)

print("✅ Data inserted into MySQL successfully!")
