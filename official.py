#!/usr/bin/env python3

import re
import sys
from datetime import datetime, timezone
from influxdb import InfluxDBClient
from config import *
from utils import *

regexp = r'^(.*?) - - \[(.*?)\] "(.*?) (.*?) .*?" (\d+) \d+ ".*?" "(.*?)"$'
SOURCE = "official"
archs = ['aarch64', 'any', 'arm', 'armv6h', 'armv7h', 'i686', 'x86_64']


def parser(line):
    result = {}
    match = re.match(regexp, line)
    if not match:
        return result
    result['remote_addr'] = match.group(1)
    date = datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z')
    result['time'] = int(datetime.timestamp(date))
    result['method'] = match.group(3)
    result['url'] = match.group(4)
    result['status'] = int(match.group(5))
    result['ua'] = match.group(6)
    while '//' in result['url']:
        result['url'] = result['url'].replace('//', '/')
    path = result.get('url').split('/')
    if len(path) > 1 and path[1] not in archs:
        return result
    if '.pkg.' in result['url']:
        package = path[-1].split('.pkg.')[0].split('-')
        try:
            result['package'] = {
                'arch': path[2],
                'name': '-'.join(package[:-3]),
                'pkgver': package[-3],
                'pkgrel': package[-2]
            }
        except:
            print(line)
            return result
    elif result['url'].endswith('archlinuxcn.db'):
        result['package'] = {
            'arch': path[2],
            'name': "archlinuxcn.db",
            'pkgver': "0",
            'pkgrel': "0"
        }
    elif result['url'].endswith('archlinuxcn.files'):
        result['package'] = {
            'arch': path[2],
            'name': "archlinuxcn.files",
            'pkgver': "0",
            'pkgrel': "0"
        }
    return result


if __name__ == '__main__':
    client = InfluxDBClient(DBHOST, DBPORT, DBUSER, DBPASS, DBNAME, True, True)
    result = []
    for line in sys.stdin:
        i = parser(line)
        if i.get('package') and is_valid(i.get('remote_addr'), i):
            geo = ip2geo(i.get('remote_addr'))
            if '.' in i.get('remote_addr'):
                address_type = 4
            else:
                address_type = 6
            result.append({
                "measurement": "pkgstats",
                "time": datetime.fromtimestamp(i.get('time'), timezone.utc),
                "tags": {
                    "source": SOURCE,
                    'asn': geo.get('asn'),
                    'country': geo.get('country'),
                    'region': geo.get('region'),
                    'city': geo.get('city'),
                    'address_type': address_type,
                    "arch": i.get('package').get('arch'),
                    "name": i.get('package').get('name'),
                    "pkgver": i.get('package').get('pkgver'),
                    "pkgrel": i.get('package').get('pkgrel'),
                    "ua": i.get('ua'),
                },
                "fields": {
                    "value": 1
                }
            })
    client.write_points(result, batch_size=5000)
