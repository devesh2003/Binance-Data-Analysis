from FuturesModule import FuturesModule

client = FuturesModule()

client.limit_long(0.01,1000,stop_loss=900,take_profit=5000)