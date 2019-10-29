import csv
import datetime
import pytz
import os

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

def get_today():
    return datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")

def get_yesterday():
    return (datetime.datetime.now(pytz.timezone('Asia/Shanghai')) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def get_cmds(start_date, end_date):
    cmds = []
    docker_cmd = 'docker exec dtl-influxdb influx -database trader -precision=rfc3339 -execute'
    start_time = start_date + ' 16:00:00'
    end_time = end_date + ' 16:00:00'
    for table in TABLES.keys():
        for exchange in EXCHANGES.keys():
            if table == 'MktBarGen' and exchange == 'BITMEX':
                continue
            filename = f'{TABLES[table]}-{EXCHANGES[exchange]}-{end_date}.csv'
            sql = f"select * from {table} where exchange='{exchange}' and time>='{start_time}' and time<'{end_time}'"
            cmd = f'{docker_cmd} "{sql}" -format csv > ../backups/{filename}'
            cmds.append(cmd)
    return cmds

def run_cmd(cmd):
    print('[run_cmd] start (cmd){}'.format(cmd))
    os.system(cmd)

if __name__ == "__main__":
    cmds = get_cmds(get_yesterday(), get_today())
    for cmd in cmds:
        run_cmd(cmd)
