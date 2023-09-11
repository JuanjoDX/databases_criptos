import hist_trading as ht
import config as cf

bot = ht.TradingBot(api_key=cf.apikey, api_secret=cf.secret, database_config=cf.config)

simbolos = ["simbolos para crear historico"]
temporalidades = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "8h", "12h", "1d"]

### Se ejecuta la función crear_db_symbol para actualizar el historico del simbolo
for sym in simbolos:
    for tem in temporalidades:
        print("Actualizando la tabla: " + sym + "_" + tem)
        bot.crear_db_symbol(sym, tem, dias_ant = 00)

bot.close_database_connection()