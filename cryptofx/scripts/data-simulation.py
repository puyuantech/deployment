import time
import math
import threading
import argparse
import signal

from influxdb import InfluxDBClient


stopping = False
stocks = ['foo', 'bar', 'hoge', 'fuga']
to_u = 1000000
start_time = time.time()


def push_stock(client):
    points = list()
    t = time.time()
    for i, stock in enumerate(stocks):
        price = 10*math.sin(t-start_time+i) + 11
        points.append({
            'measurement': 'stocks',
            'tags': {
                'stock_name': stock,
            },
            'fields': {
                'price': price,
            }, 'time': int(t*to_u),
        })
    client.write_points(points, time_precision='u')

def push_balance(client):
    points = list()
    t = time.time()
    for i, stock in enumerate(stocks):
        points.append({
            # we put it into stock so that we can do math easier
            'measurement': 'stocks',
            'tags': {
                'stock_name': stock,
            },
            'fields': {
                'holdings': math.log(t-start_time+1)+i,
            },
            'time': int(t*to_u),
        })
    points.append({
        'measurement': 'balance',
        'fields': {
            'available': 50-2*math.log(t-start_time+1),
        },
        'time': int(t*to_u),
    })
    client.write_points(points, time_precision='u')


def ticker(interval, func, *args):
    # it's said that the client is using requests
    # which is thread-safe if you don't modify anything manually.
    global stopping
    while not stopping:
        func(*args)
        time.sleep(interval)


def main(host, port):
    client = InfluxDBClient(host=host, port=port, database='trader', retries=100)
    client.create_database('trader')
    print('database created')
    client.query('CREATE CONTINUOUS QUERY stock_1s_slice ON trader '
                 'BEGIN '
                 'SELECT LAST(price) AS "price", '
                 '       LAST(holdings) AS "holdings", '
                 '       LAST(holdings)*LAST(price) AS "revenue" '
                 'INTO profit_1s '
                 'FROM stocks GROUP BY time(1s,1s),stock_name '
                 'END')
    print('CONTINUOUS QUERY stock_1s_slice created')
    client.query('CREATE CONTINUOUS QUERY balance_1s_slice ON trader '
                 'BEGIN '
                 'SELECT LAST(available) AS "available" '
                 'INTO profit_1s '
                 'FROM balance GROUP BY time(1s,1s),stock_name '
                 'END')
    print('CONTINUOUS QUERY balance_1s_slice created')

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    threads = [
        threading.Thread(target=ticker, args=(0.5, push_stock, client)),
        threading.Thread(target=ticker, args=(2, push_balance, client))
    ]
    for t in threads:
        t.setDaemon(True)
        t.start()
    print('started!')
    for t in threads:
        t.join()

def signal_handler(signum=None, frame=None):
    global stopping
    stopping = True
    print('Interrupted {}'.format(signum))


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    main(host=args.host, port=args.port)
