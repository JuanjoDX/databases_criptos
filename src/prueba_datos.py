from binance import Client
import pandas as pd
import config as cf
import time 
from datetime import datetime, timedelta
import mysql.connector
from sqlalchemy import create_engine

config = {
    'user': 'juanjodx',
    'password': '1234',
    'host':'localhost',
    "database": "criptos",
}

client = Client(api_key= cf.apikey, api_secret= cf.secret)

res = client.get_exchange_info() ### de aca deberia sacar la ultima hora 
hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

hora_inicio = hora_ser-timedelta(days = 1)
hora_fin = hora_ser-timedelta(minutes = 100)

str_hora_inicio = hora_inicio.strftime('%Y-%m-%d %H:%M:%S')
str_hora_fin = hora_fin.strftime('%Y-%m-%d %H:%M:%S')

historical = client.futures_historical_klines(symbol='1000SHIBUSDT',
                                              interval='1m',
                                              start_str=str_hora_inicio,
                                              end_str=str_hora_fin
                                              )

hist_df = pd.DataFrame(historical)

hist_df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 
                    'number_of_trades', 'tb_base_volume', 'tb_quote_volume', 'Ignore']

hist_df['open_time'] = pd.to_datetime(hist_df['open_time']/1000, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
hist_df['close_time'] = pd.to_datetime(hist_df['close_time']/1000, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'tb_base_volume', 'tb_quote_volume']
hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

hist_df.drop(["Ignore"],axis = 1,inplace = True)

engine = create_engine(f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}")

try:
    # Inserta el DataFrame en la tabla MySQL
    hist_df.to_sql(name='1000shib_1m', con=engine, if_exists='append', index=False)

except Exception as e:
    print("Error:", e)

finally:
    # Cierra la conexión de SQLAlchemy
    engine.dispose()