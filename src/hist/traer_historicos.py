### Se importan las librerias necesarias

from binance import Client
import pandas as pd
import config as cf
import time 
from datetime import timedelta
import mysql.connector
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")

def crear_historico_symbol(client, symbol, temp, dias_ant):

    ### Función para traer la información historica 
    ### symbol : Criptomoneda de interes
    ### temp : Temporalidad que se desea traer
    ### dias_ant : Cuantos dias hacia atras respecto a la hora del servidor se quiere traer la info

    res = client.get_exchange_info() ### de aca deberia sacar la ultima hora 
    hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

    ### Se define el inicio y el fin de obtención de información
    hora_inicio = hora_ser-timedelta(days = dias_ant)
    hora_fin = hora_ser

    ### Se convierten las fechas de inicio y fin a un formato especifico
    str_hora_inicio = hora_inicio.strftime('%Y-%m-%d %H:%M:%S')
    str_hora_fin = hora_fin.strftime('%Y-%m-%d %H:%M:%S')

    ### Se hace la consulta y se trae el historico por simbolo, temporalidad, fecha_inicio y fecha_fin
    while True:
        try:
            historical = client.futures_historical_klines(symbol=symbol,
                                                          interval=temp,
                                                          start_str=str_hora_inicio,
                                                          end_str=str_hora_fin
                                                          )
            if historical is not None and len(historical) > 0:
                break
        except Exception as e:
            # No se obtuvieron datos, esperar un tiempo antes de volver a intentar
            time.sleep(1)

    ### Se convierte en DataFrame historical
    hist_df = pd.DataFrame(historical)

    ### Se le dan el nombre a las columnas
    hist_df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 
                        'number_of_trades', 'tb_base_volume', 'tb_quote_volume', 'Ignore']

    ### Se dan formato de fecha a open_time y close_time
    hist_df['open_time'] = pd.to_datetime(hist_df['open_time']/1000, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    hist_df['close_time'] = pd.to_datetime(hist_df['close_time']/1000, unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    ### Se definen las columnas que son numericas
    numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'tb_base_volume', 'tb_quote_volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

    ### Se elimina una columna innecesaria
    hist_df.drop(["Ignore"], axis = 1, inplace = True)

    ### Se crea el nombre de la tabla
    nombre_tabla = symbol + "_" + temp

    ### Se crea conexión a mysql server para crear la tabla donde va la información
    conn = mysql.connector.connect(**cf.config)
    cursor = conn.cursor()

    ### Se manda el query de creación de tabla
    cursor.execute("""CREATE TABLE {0} (open_time VARCHAR(255), 
                   open FLOAT, high FLOAT, low FLOAT, close FLOAT, 
                   volume FLOAT, close_time VARCHAR(255), 
                   quote_asset_volume FLOAT, number_of_trades INT,
                   tb_base_volume FLOAT, tb_quote_volume FLOAT);""".format(nombre_tabla))
    
    ### Se cierra la conexión
    cursor.close()
    conn.close()

    ### Se crea una nueva conexión para almacenar la información a las tablas
    engine = create_engine(f"mysql+mysqlconnector://{cf.config['user']}:{cf.config['password']}@{cf.config['host']}/{cf.config['database']}")

    try:
        # Inserta el DataFrame en la tabla MySQL
        hist_df.to_sql(name = nombre_tabla, con = engine, if_exists = 'append', index = False)

    except Exception as e:
        print("Error:", e)

    finally:
        # Cierra la conexión de SQLAlchemy
        engine.dispose()

### Se definen los simbolos y las temporalidades de los simbolos que se tiene interes
simbolos = ["BTCUSDT", "ETHUSDT", "1000SHIBUSDT", "1000LUNCUSDT", "OCEANUSDT", "OMGUSDT", "TRXUSDT", 
            "HOTUSDT", "FTMUSDT", "XRPUSDT", "DOGEUSDT", "XLMUSDT"]
temporalidades = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "8h", "12h", "1d"]

### Se conecta a Binance para obtener datos mediante la API
client = Client(api_key= cf.apikey, api_secret= cf.secret)

### Se ejecuta la función crear_historico_symbol para traer la información historica del simbolo
for sym in simbolos:
    for tem in temporalidades:
        print(sym + "_" + tem)
        crear_historico_symbol(client, sym, tem, 100)