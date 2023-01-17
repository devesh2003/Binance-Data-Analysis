from binance.client import Client

class FuturesModule:
    with open("API.txt", "r") as f:
        api_key = f.readline().strip()
        api_secret = f.readline().strip()

    def __init__(self,leverage=5,symbol='ETHUSDT'):
        self.symbol = symbol
        self.leverage = leverage
        self.client = Client(self.api_key, self.api_secret)
        self.client.futures_change_leverage(symbol=self.symbol,leverage=self.leverage)
        try:
            self.client.futures_change_margin_type(symbol=self.symbol,marginType="ISOLATED")
        except:
            pass
    
    def limit_long(self,quantity,price,stop_loss=0,take_profit=0):
        self.order = self.client.futures_create_order(symbol=self.symbol,side="BUY",type="LIMIT",quantity=quantity,price=price,timeInForce="GTC")
        self.tp = self.client.futures_create_order(symbol=self.symbol,side="SELL",type="TAKE_PROFIT_MARKET",quantity=quantity,stopPrice=take_profit,timeInForce="GTC",
                                                    closePosition=True)
        self.sl = self.client.futures_create_order(symbol=self.symbol,side="SELL",type="STOP_MARKET",quantity=quantity,stopPrice=stop_loss,timeInForce="GTC",
                                                    closePosition=True)
    
    def limit_short(self,quantity,price,stop_loss=0,take_profit=0):
        self.order = self.client.futures_create_order(symbol=self.symbol,side="SELL",type="LIMIT",quantity=quantity,price=price,timeInForce="GTC")
        self.tp = self.client.futures_create_order(symbol=self.symbol,side="BUY",type="TAKE_PROFIT_MARKET",quantity=quantity,stopPrice=take_profit,timeInForce="GTC",
                                                    closePosition=True)
        self.sl = self.client.futures_create_order(symbol=self.symbol,side="BUY",type="STOP_MARKET",quantity=quantity,stopPrice=stop_loss,timeInForce="GTC",
                                                    closePosition=True)

    def market_long(self,quantity):
        self.order = self.client.futures_create_order(symbol=self.symbol,side="BUY",type="MARKET",quantity=quantity)

    def market_short(self,quantity):
        self.order = self.client.futures_create_order(symbol=self.symbol,side="SELL",type="MARKET",quantity=quantity)
