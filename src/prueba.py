import mysql.connector 

config = {
    'user': 'juanjodx',
    'password': '1234',
    'host':'localhost',
}

conn = mysql.connector.connect(**config)

cursor = conn.cursor()

cursor.execute("""SELECT open_time FROM criptos.1000shib_1m
               ORDER BY open_time DESC
               LIMIT 1;""")

fecha = cursor.fetchall()[0][0]
print(fecha)

cursor.close()
conn.close()