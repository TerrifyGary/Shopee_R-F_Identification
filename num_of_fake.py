import sqlite3
# Create your connection.
conn = sqlite3.connect('./Shopee_R-F_Identification/Data.db')

def num_of_fake(star):
    df = pd.read_sql_query("SELECT * FROM rating", conn)
    df = pd.read_sql_query("SELECT * FROM rating WHERE star == (?)", conn, params=(star,))
    comment_ = df['comment'].to_string()   
    return comment_.count('假')

for x in range(5):
    print(x+1,'Star;','Number of 假:',num_of_fake(x+1))
conn.commit()
conn.close()   
