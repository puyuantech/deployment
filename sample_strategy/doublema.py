# -*- coding: UTF-8 -*-

import sys
import pandas as pd
import numpy as np
from tlclient.trader.client import Client
from tlclient.trader.constant import Direction, ExchangeID, MsgType, OffsetFlag, OrderType

class TradeSample(Client):

    long_window = 0
    short_window = 0
    history_data = []
    long_ma0 = 0
    long_ma1 = 0
    short_ma0 = 0
    short_ma1 = 0

    ticker = ''
    exchange = ''
    tg = ''
    position = 0
    direction = 0

    def __init__(self):
        Client.__init__(self, name='trade_test', env_name='laptop', addr="tcp://127.0.0.1:5000")
        self.init_trade('trade1')
        self.init_market('market1')

    #重载所需的函数
    def on_mkt_snap(self, obj, msg_type, frame_nano):
        print('[mkt_snap] ' + str(obj))  
        # 实现收到行情时需要进行的计算、下单及其他操作
        self.history_data.append(obj.last_price)
        self.long_ma1 = np.mean(self.history_data[-self.long_window:])
        self.short_ma1 = np.mean(self.history_data[-self.short_window])
        print('lma0,lma1', self.long_ma0, self.long_ma1)
        print('sma0,sma1', self.short_ma0, self.short_ma1)
        over_flag = self.short_ma1 > self.long_ma1 and self.short_ma0 <= self.long_ma0
        below_flag = self.short_ma1 < self.long_ma1 and self.short_ma0 >= self.long_ma0
        pos = self.position

        if over_flag:
            print('------------cross over--------------')
            #撤销所有可撤委托
            self.req_cancel_active_orders(self.tg, -1)
            if pos >= 0 :
                print('======buy=====')
                #下单
                self.insert_order(tg_name = self.tg , exchange = self.exchange, ticker = self.ticker, price = 0, 
                                 volume = 100, order_type = OrderType.MARKET, direction = Direction.BUY, offset_flag= OffsetFlag.OPEN)

        elif below_flag:
            print('------------cross below--------------')
            #撤销所有可撤委托
            self.req_cancel_active_orders(self.tg, -1)
            if pos >= 0 :
                print('======sell=====')
                #下单
                self.insert_order(tg_name = self.tg , exchange = self.exchange, ticker = self.ticker, price = 0, 
                                 volume = 100, order_type = OrderType.MARKET, direction = Direction.SELL, offset_flag= OffsetFlag.CLOSE)


        self.long_ma0 = self.long_ma1
        self.short_ma0 = self.short_ma1   

    def on_rsp_position(self, obj, nano):
        #查询持仓的响应
        if obj is None:
            self.position = 0
        else:
            for pos in obj.pos_list:
                if pos.exchange == self.exchange and pos.ticker is self.ticker:
                    self.position = pos.position
                    self.direction = pos.posi_direction
                    break

        print('position------',self.position)    
        print('direction------',self.direction)   
        print('[rpos] ' + str(obj))       

    def on_rsp_order_insert(self, obj, nano):
        #委托响应
        print('[roi] ' + str(obj))

    def on_rtn_order(self, obj, nano):
        #委托回报
        print('[o] ' + str(obj))

    def on_rtn_trade(self, obj, nano):
        #成交回报
        self.position += obj.volume
        print('[t] ' + str(obj))
    
    def on_gateway_connection_change(self, obj, frame_nano):
        #监控网络状态变化
        # turn on the next line, the client will print received message when gateway is offline
        # print('[conn] ' + str(obj))
        pass

    def on_gateway_heart_beat(self, obj, frame_nano):
        #监控网关心跳
        # turn on the next line, the client will print received heartbeat in console
        # print('[hb] ' + str(obj))
        pass


if __name__ == '__main__':

    # 声明客户端实例
    ts = TradeSample()

    # 策略变量
    ts.long_window = 1000
    ts.short_window = 50
    ts.tg = 'ctp1'
    ts.ticker = 'rb1906'
    ts.exchange = ExchangeID.SHFE

    # 目前不支持获取历史数据，需要从其他数据源获取
    path = 'data.csv'
    ts.history_data = list(pd.read_csv(path,delimiter="\t")['price'])

    # 初始化指标
    ts.long_ma0 = np.mean(ts.history_data[-ts.long_window:], 0)
    ts.short_ma0 = np.mean(ts.history_data[-ts.short_window:], 0)
    # 查询持仓
    ts.req_position(ts.tg)

    # 订阅实时数据
    ts.subscribe(exchange = ts.exchange, ticker = ts.ticker, msg_type = MsgType.MKT_SNAP)

    ts.start()
    ts.join()