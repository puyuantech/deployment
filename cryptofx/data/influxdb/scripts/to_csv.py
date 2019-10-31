import datetime
import os
import pytz

TABLES = {
    'MktTrade': 'trade',
    'MktSnapOpt': 'snap',
    'MktBarGen': 'bar',
}
EXCHANGES = {
    'BINANCE': 'binance',
    'BITMEX': 'bitmex',
    'HUOBI': 'huobi',
    'OKEX': 'okex',
}

def get_date():
    return datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")

def get_date_and_hour():
    return datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d_%H")

def get_date_and_hour_ago(days=0, hours=0):
    return (datetime.datetime.now(pytz.timezone('Asia/Shanghai')) - datetime.timedelta(days=days, hours=hours)).strftime("%Y-%m-%d_%H")

def get_timestamp(date):
    return int((datetime.datetime.strptime(date, '%Y-%m-%d_%H') - datetime.timedelta(hours=8)).timestamp() * 1e9)

def get_cmds(start_date, end_date, use_precision=False):
    cmds = []
    # use precision: 2019-10-31T02:00:03.632Z, else: 1572487201622999000
    if use_precision:
        docker_cmd = 'docker exec dtl-influxdb influx -database trader -precision=rfc3339 -execute'
    else:
        docker_cmd = 'docker exec dtl-influxdb influx -database trader -execute'

    directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + f'/backups/{start_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    start_time = get_timestamp(start_date)
    end_time = get_timestamp(end_date)

    for table in TABLES.keys():
        for exchange in EXCHANGES.keys():
            if table == 'MktBarGen' and exchange == 'BITMEX':
                continue
            filename = f'{TABLES[table]}-{EXCHANGES[exchange]}-{start_date}.csv'
            sql = f"select * from {table} where exchange='{exchange}' and time>={start_time} and time<{end_time}"
            cmd = f'{docker_cmd} "{sql}" -format csv > {directory}/{filename}'
            cmds.append(cmd)
    return cmds

def run_cmd(cmd):
    print('[run_cmd] start (cmd){}'.format(cmd))
    os.system(cmd)

if __name__ == "__main__":
    cmds = get_cmds(get_date_and_hour_ago(hours=1), get_date_and_hour())
    for cmd in cmds:
        run_cmd(cmd)
