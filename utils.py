#!/usr/bin/env python3

import pyasn
from IP2Location import IP2Location

cache = {}
ipgeo = IP2Location()
ipgeo.open('/home/rancher/access_log/ip2location.bin')
ipasn = pyasn.pyasn('/home/rancher/access_log/ipasn.bin')


def ip2geo(ip):
    asn = ipasn.lookup(ip)[0]
    geo = ipgeo.get_all(ip)
    result = {
        'asn': asn,
        'country': geo.country_short,
        'region': geo.region,
        'city': geo.city,
    }
    return result


def is_valid(ip, package) -> bool:
    if package.get('status') < 200 or package.get('status') >= 400:
        return False
    if package.get('method') != 'GET':
        return False
    if package.get('status') == 204:
        hash_key = ip + package.get('name') + package.get('ua')
        t = cache.get(hash_key)
        cache[hash_key] = package.get('time')
        # Only count once in 120 seconds
        if t and package.get('time') < t + 120:
            return False
    return True
