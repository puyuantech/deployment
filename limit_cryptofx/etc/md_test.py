
from trader.client import Client
from trader.constant import ExchangeID

class MdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='env1', addr="tcp://localhost:9000")
        self.init_market('market1')

    def on_mkt_bar(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

    def on_mkt_snap(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

    def on_mkt_trade(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

    def on_mkt_index(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

if __name__ == '__main__':
    md = MdTest()

    for exchange in [ExchangeID.BINANCE, ExchangeID.BITMEX, ExchangeID.HUOBI, ExchangeID.OKEX]:
        md.subscribe_bar(exchange, "*")
        md.subscribe_snap(exchange, "*")
        md.subscribe_trade(exchange, "*")

    for exchange in [ExchangeID.BITSTAMP, ExchangeID.COINBASE]:
        md.subscribe_snap(exchange, 'btc/usd')

    md.subscribe_snap(ExchangeID.KRAKEN, 'xbt/usd')
    md.subscribe_index(ExchangeID.OKEX, 'btc/usd')

    md.start()
    md.join()
