from tlclient.trader.client import Client
from tlclient.trader.constant import ExchangeID

class MdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='mac1', addr="tcp://localhost:9000")
        self.init_market('market1')
        self.init_trade('trade1')

    def on_mkt_trade(self, obj, msg_type, frame_nano):
        print('[on_mkt_trade] (msg_type){} (obj){}'.format(msg_type, obj))

    def on_mkt_bar(self, obj, msg_type, frame_nano):
        print('[on_mkt_bar] (msg_type){} (obj){}'.format(msg_type, obj))

    def on_mkt_snap(self, obj, msg_type, frame_nano):
        print('[on_mkt_snap] (msg_type){} (obj){}'.format(msg_type, obj))

if __name__ == '__main__':
    md = MdTest()
    md.subscribe_trade(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_bar(ExchangeID.HUOBI, "btc/usdt")
    md.subscribe_snap(ExchangeID.HUOBI, "btc/usdt")
    md.start()
    md.join()