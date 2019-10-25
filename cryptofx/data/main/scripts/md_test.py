
from trader.client import Client
from trader.constant import ExchangeID

class MdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='mac1', addr="tcp://localhost:9000")
        self.init_market('market1')

    def on_mkt_snap(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

    def on_mkt_bar(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

    def on_mkt_trade(self, obj, msg_type, frame_nano):
        self.logger.info(obj)

if __name__ == '__main__':
    md = MdTest()

    md.subscribe_trade(ExchangeID.BINANCE, "btc/usdt")
    md.subscribe_trade(ExchangeID.BITMEX, "xbtusd")
    md.subscribe_trade(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_trade(ExchangeID.OKEX, "btc/usdt")

    md.subscribe_bar(ExchangeID.BINANCE, "btc/usdt")
    md.subscribe_bar(ExchangeID.BITMEX, "xbtusd")
    md.subscribe_bar(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_bar(ExchangeID.OKEX, "btc/usdt")

    # md.subscribe_trade(ExchangeID.BINANCE, "*")
    # md.subscribe_trade(ExchangeID.BITMEX, "*")
    # md.subscribe_trade(ExchangeID.HUOBI, "*")
    # md.subscribe_trade(ExchangeID.OKEX, "*")

    md.subscribe_snap(ExchangeID.BINANCE, "*")
    md.subscribe_snap(ExchangeID.BITMEX, "*")
    md.subscribe_snap(ExchangeID.HUOBI, "*")
    md.subscribe_snap(ExchangeID.OKEX, "*")

    md.start()
    md.join()
