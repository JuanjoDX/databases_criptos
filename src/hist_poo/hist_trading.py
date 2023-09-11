from binance import Client
import pandas as pd
import time
import config as cf
import mysql.connector
from sqlalchemy import create_engine
import warnings
from datetime import timedelta
warnings.filterwarnings("ignore")

class TradingBot:
    def __init__(self, api_key, api_secret, database_config):
        self.api_key = api_key
        self.api_secret = api_secret
        self.database_config = database_config
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)

        ### Se crea conexión a mysql server para crear la tabla donde va la información
        self.conn = mysql.connector.connect(**self.database_config)
        self.cursor = self.conn.cursor()
        self.engine = create_engine(f"mysql+mysqlconnector://{database_config['user']}:{database_config['password']}@{database_config['host']}/{database_config['database']}")

    def close_database_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            self.conn = None
            self.engine.dispose()
            self.engine = None

    def __del__(self):
        self.close_database_connection()

    def historical(self,symbol,temp,str_hora_inicio,str_hora_fin):
        while True:
            try:
                historical = self.client.futures_historical_klines(symbol=symbol,
                                                            interval=temp,
                                                            start_str=str_hora_inicio,
                                                            end_str=str_hora_fin
                                                            )
                if historical is not None and len(historical) > 0:
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

                    return(hist_df)
                
            except Exception as e:
                # No se obtuvieron datos, esperar un tiempo antes de volver a intentar
                time.sleep(1)
        
    def crear_db_symbol(self, symbol, temp, dias_ant):
        ### Se crea el nombre de la tabla para insertar los registros 
        nombre_tabla = symbol + "_" + temp

        self.cursor.execute("""CREATE TABLE {0} (open_time VARCHAR(255), 
                   open FLOAT, high FLOAT, low FLOAT, close FLOAT, 
                   volume FLOAT, close_time VARCHAR(255), 
                   quote_asset_volume FLOAT, number_of_trades INT,
                   tb_base_volume FLOAT, tb_quote_volume FLOAT);""".format(nombre_tabla))
    
        res = self.client.get_exchange_info() ### de aca deberia sacar la ultima hora 
        hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

        ### Se define el inicio y el fin de obtención de los registros
        hora_inicio = hora_ser-timedelta(days = dias_ant)
        hora_fin = hora_ser

        ### Se convierten las fechas de inicio y fin a un formato especifico
        str_hora_inicio = hora_inicio.strftime('%Y-%m-%d %H:%M:%S')
        str_hora_fin = hora_fin.strftime('%Y-%m-%d %H:%M:%S')

        ### Se hace la consulta y se trae el historico por simbolo, temporalidad, fecha_inicio y fecha_fin
        hist_df = self.historical(symbol, temp, str_hora_inicio, str_hora_fin)

        try:
            # Inserta el DataFrame en la tabla MySQL
            hist_df.to_sql(name=nombre_tabla, con=self.engine, if_exists='append', index=False)

        except Exception as e:
            print("Error:", e)

    def act_db_symbol(self, symbol, temp):
    ### Función para traer los ultimos registros historicos del simbolo y se actualiza
    ### symbol : Criptomoneda de interes
    ### temp : Temporalidad que se desea traer

        ### Se crea el nombre de la tabla para insertar los registros 
        nombre_tabla = symbol + "_" + temp

        self.cursor.execute("""SELECT open_time FROM db_criptos.{0}
                        ORDER BY open_time DESC
                        LIMIT 1;""".format(nombre_tabla))

        ot = self.cursor.fetchall()[0][0]
        fecha = pd.to_datetime(ot)

        delete_query = """DELETE FROM db_criptos.{0}
                        WHERE open_time = %s;""".format(nombre_tabla)

        # Ejecuta la consulta de eliminación con el valor de ot formateado
        self.cursor.execute(delete_query, (ot,))

        ### Se hace el commit y se cierra la conexión   
        self.conn.commit()

        res = self.client.get_exchange_info() ### de aca deberia sacar la ultima hora 
        hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

        ### Se define el inicio y el fin de obtención de los registros
        hora_inicio = fecha
        hora_fin = hora_ser

        ### Se convierten las fechas de inicio y fin a un formato especifico
        str_hora_inicio = hora_inicio.strftime('%Y-%m-%d %H:%M:%S')
        str_hora_fin = hora_fin.strftime('%Y-%m-%d %H:%M:%S')

        ### Se hace la consulta y se trae el historico por simbolo, temporalidad, fecha_inicio y fecha_fin
        hist_df = self.historical(symbol, temp, str_hora_inicio, str_hora_fin)

        try:
            # Inserta el DataFrame en la tabla MySQL
            hist_df.to_sql(name=nombre_tabla, con=self.engine, if_exists='append', index=False)

        except Exception as e:
            print("Error:", e)