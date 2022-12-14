from  flask import Blueprint
modbus_controller       = Blueprint('modbus',__name__)
stock_controller        = Blueprint('stock',__name__)
other_controller        = Blueprint('other',__name__)
tickerOrder_controller  = Blueprint('tickerOrder',__name__)
from . import modbus
from . import other
from . import stock
from . import tickerOrder