import hist_trading as ht
import config as cf

bot = ht.TradingBot(api_key=cf.apikey, api_secret=cf.secret, database_config=cf.config)

### Se definen los simbolos y las temporalidades de los simbolos que se deben actualizar
simbolos = ["BTCUSDT", "ETHUSDT", "1000SHIBUSDT", "1000LUNCUSDT", "OCEANUSDT", "OMGUSDT", 
            "TRXUSDT", "HOTUSDT", "FTMUSDT", "XRPUSDT", "DOGEUSDT", "XLMUSDT", "THETAUSDT"]
temporalidades = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "8h", "12h", "1d"]

### Se ejecuta la función act_historico_symbol para actualizar el historico del simbolo
for sym in simbolos:
    for tem in temporalidades:
        print("Actualizando la tabla: " + sym + "_" + tem)
        bot.act_db_symbol(sym, tem)

bot.close_database_connection()