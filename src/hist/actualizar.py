import actualizar_historicos as act_hist
from binance import Client
import config as cf

### Se definen los simbolos y las temporalidades de los simbolos que se deben actualizar
simbolos = ["BTCUSDT", "ETHUSDT", "1000SHIBUSDT", "1000LUNCUSDT", "OCEANUSDT", "OMGUSDT", 
            "TRXUSDT", "HOTUSDT", "FTMUSDT", "XRPUSDT", "DOGEUSDT", "XLMUSDT"]
temporalidades = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "6h", "8h", "12h", "1d"]

### Se conecta a Binance para obtener datos mediante la API
client = Client(api_key= cf.apikey, api_secret= cf.secret)

### Se ejecuta la función act_historico_symbol para actualizar el historico del simbolo
for sym in simbolos:
    for tem in temporalidades:
        print("Actualizando la tabla: " + sym + "_" + tem)
        act_hist.act_historico_symbol(client, sym, tem)