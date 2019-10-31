import boto3
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


class Csv_And_S3:

    def __init__(self):
        self.docker_cmd = 'docker exec dtl-influxdb influx -database trader -execute'
        self.sql_cmd = "select * from {} where exchange='{}' and time>={} and time<{}"
        self.filename_cmd = '{}-{}-{}.csv'
        self.to_csv_cmd = '{} "{}" -format csv > {}'

        self.s3 = boto3.resource('s3')
        self.bucket_name = 'll-raw-data-ap-1'
        self.source = 'crypto'

    def create_bucket(self):
        self.s3.Bucket(name=self.bucket_name).create(
            ACL = 'public-read',
            CreateBucketConfiguration = {
                'LocationConstraint': 'ap-southeast-1'
            }
        )

    def _get_date_and_hour(self):
        end_datetime = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        start_datetime = end_datetime - datetime.timedelta(hours=1)
        return start_datetime.strftime("%Y-%m-%d"), start_datetime.strftime("%Y-%m-%d_%H"), end_datetime.strftime("%Y-%m-%d_%H")

    def _get_timestamp(self, date):
        return int((datetime.datetime.strptime(date, '%Y-%m-%d_%H') - datetime.timedelta(hours=8)).timestamp() * 1e9)

    def _make_key(self, *args):
        return '/'.join(args)

    def upload_file(self, file_path, file_key):
        self.s3.meta.client.upload_file(file_path, self.bucket_name, file_key)
        obj_acl = self.s3.ObjectAcl(self.bucket_name, file_key)
        obj_acl.put(ACL = 'public-read')

    def save(self):
        date, start_hour, end_hour = self._get_date_and_hour()
        start_time = self._get_timestamp(start_hour)
        end_time = self._get_timestamp(end_hour)

        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + f'/backups/{start_hour}'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        for table in TABLES.keys():
            for exchange in EXCHANGES.keys():
                if table == 'MktBarGen' and exchange == 'BITMEX':
                    continue

                sql = self.sql_cmd.format(table, exchange, start_time, end_time)
                filename = self.filename_cmd.format(TABLES[table], EXCHANGES[exchange], start_hour)
                file_path = base_dir + '/' + filename
                to_csv_cmd = self.to_csv_cmd.format(self.docker_cmd, sql, file_path)

                print('start save to csv. (cmd){}'.format(to_csv_cmd))
                os.system(to_csv_cmd)

                file_key = self._make_key(self.source, EXCHANGES[exchange], TABLES[table], date, filename)

                print('start upload to s3. (key){}'.format(file_key))
                self.upload_file(file_path, file_key)

        print('end.')


if __name__ == "__main__":
    Csv_And_S3().save()
