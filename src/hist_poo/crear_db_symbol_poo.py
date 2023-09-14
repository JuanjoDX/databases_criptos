import hist_trading as ht
import config as cf
import time

bot = ht.TradingBot(api_key=cf.apikey, api_secret=cf.secret, database_config=cf.config)

simbolos = ["BTCUSDT", "ETHUSDT", "1000SHIBUSDT", "1000LUNCUSDT", "OCEANUSDT", "OMGUSDT", 
            "TRXUSDT", "HOTUSDT", "FTMUSDT", "XRPUSDT", "DOGEUSDT", "XLMUSDT", "THETAUSDT"]
temporalidades = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "8h", "12h", "1d"]

### Se ejecuta la función crear_db_symbol para actualizar el historico del simbolo
inicio = time.time() 
for sym in simbolos:
    start_time = time.time() 
    for tem in temporalidades:
        print("Actualizando la tabla: " + sym + "_" + tem)
        bot.crear_db_symbol(sym, tem, dias_ant= 100)
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido en segundos
    print(f"Tiempo transcurrido: {round(elapsed_time,2)} segundos")
fin = time.time()
elapsed_time = fin - inicio  # Calcula el tiempo transcurrido en segundos
print(f"Tiempo total transcurrido: {round(elapsed_time,2)} segundos")

bot.close_database_connection()