from tlclient.trader import message_trade
from tlclient.trader.client import Client
from tlclient.trader.constant import AssetType, Direction, ExchangeID, OffsetFlag, OrderType

class TdTest(Client):

    def __init__(self):
        Client.__init__(self, name='md_test', env_name='mac1', addr="tcp://localhost:9000")
        self.init_market('market1')
        self.init_trade('trade1')

    def on_rsp_order_insert(self, obj: message_trade.RspOrderInsert, frame_nano):
        self.logger.info('[roi] (obj){}'.format(obj))

    def on_rsp_order_cancel(self, obj: message_trade.RspOrderCancel, frame_nano):
        self.logger.info('[roc] (obj){}'.format(obj))

    def on_rtn_trade(self, obj: message_trade.RtnTrade, frame_nano):
        self.logger.info('[rtt] (obj){}'.format(obj))

    def on_rtn_order(self, obj: message_trade.RtnOrder, frame_nano):
        self.logger.info('[rto] (obj){}'.format(obj))

    def on_rsp_position(self, obj: message_trade.RspPosition, frame_nano):
        self.logger.info('[pos] (obj){}'.format(obj))

if __name__ == '__main__':
    td = TdTest()

    td.insert_order('pybm', ExchangeID.BITMEX, 'xbtusd', -1, 3, OrderType.MARKET, Direction.SELL, asset_type=AssetType.CRYPTO_CONTRACT, offset_flag=OffsetFlag.OPEN)

    oid = td.insert_order('pybm', ExchangeID.BITMEX, 'xbtusd', 7000, 5, OrderType.LIMIT, Direction.BUY, asset_type=AssetType.CRYPTO_CONTRACT, offset_flag=OffsetFlag.OPEN)
    if oid == -1:
        print('order insert error.')
    else:
        td.cancel_order(oid, 'pybm')

    td.req_position('pybm')

    td.start()
    td.join()
