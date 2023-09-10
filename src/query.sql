CREATE DATABASE criptos;
use criptos;
CREATE TABLE 1000SHIB_1M (
    open_time VARCHAR(255),
    open FLOAT, 
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    close_time VARCHAR(255),
    quote_asset_volume FLOAT,
    number_of_trades INT,
    tb_base_volume FLOAT,
    tb_quote_volume FLOAT)
;


use criptos;
select * from 1000SHIB_1M ORDER BY open_time;

use criptos;
DELETE FROM 1000SHIB_1M;


use criptos;
SELECT open_time FROM 1000SHIB_1M
ORDER BY open_time DESC
LIMIT 1;