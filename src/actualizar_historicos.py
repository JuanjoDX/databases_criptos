def act_historico_symbol(symbol, temp):
    ### Función para traer los ultimos registros historicos del simbolo y se actualiza
    ### symbol : Criptomoneda de interes
    ### temp : Temporalidad que se desea traer

    from binance import Client
    import pandas as pd
    import config as cf
    import time 
    import mysql.connector
    from sqlalchemy import create_engine
    import warnings
    warnings.filterwarnings("ignore")

    ### Se crea el nombre de la tabla para insertar los registros 
    nombre_tabla = symbol + "_" + temp
    
    ### Se crea conexión a mysql server para crear la tabla donde va la información
    conn = mysql.connector.connect(**cf.config)
    cursor = conn.cursor()

    cursor.execute("""SELECT open_time FROM db_criptos.{0}
                   ORDER BY open_time DESC
                   LIMIT 1;""".format(nombre_tabla))
    
    ot = cursor.fetchall()[0][0]
    fecha = pd.to_datetime(ot)
    print(nombre_tabla)
    print(fecha)

    delete_query = """DELETE FROM db_criptos.{0}
                   WHERE open_time = %s;""".format(nombre_tabla)

    # Ejecuta la consulta de eliminación con el valor de ot formateado
    cursor.execute(delete_query, (ot,))

    ### Se hace el commit y se cierra la conexión   
    conn.commit()
    cursor.close()
    conn.close()

    ### Se conecta a Binance para obtener datos mediante la API
    client = Client(api_key= cf.apikey, api_secret= cf.secret)

    res = client.get_exchange_info() ### de aca deberia sacar la ultima hora 
    hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

    ### Se define el inicio y el fin de obtención de los registros
    hora_inicio = fecha
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
            print(len(historical))
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

    ### Se crea una nueva conexión para almacenar los registros  a las tablas
    engine = create_engine(f"mysql+mysqlconnector://{cf.config['user']}:{cf.config['password']}@{cf.config['host']}/{cf.config['database']}")

    try:
        # Inserta el DataFrame en la tabla MySQL
        hist_df.to_sql(name=nombre_tabla, con=engine, if_exists='append', index=False)

    except Exception as e:
        print("Error:", e)

    finally:
        # Cierra la conexión de SQLAlchemy
        engine.dispose()