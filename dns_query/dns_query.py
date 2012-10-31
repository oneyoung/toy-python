#!/usr/bin/env python3
import os
import sys
import re
from ip_location import ip_location


def INFO(*args, **kwargs):
    print(*args, **kwargs)


def get_avr_ping(host):
    cmd = "ping -c 4 %s" % host
    p = os.popen(cmd)
    #result example: rtt min/avg/max/mdev = 183.628/254.661/326.847/66.045 ms\n
    try:
        tmp = p.readlines()[-1].split()[-2]  # tmp = "183.628/254.661/326.847/66.045"
    except IndexError:  # catch except if host is unreachable
        return 0
    result = float(tmp.split("/")[1])
    INFO("ping host %s\ttakes %f ms" % (host, result))
    return result


def query_host(hostname, dns_server=None):
    cmd = "host {host} {dns}".format(host=hostname, dns=dns_server)
    p = os.popen(cmd)
    for line in p.readlines():
        if "has address" in line:
            ip_addr = line.split()[-1]
            INFO("query server %s\twith result %s" % (dns_server.strip(), ip_addr))
            return ip_addr
    #print("host not found")
    INFO("query server %s\tfailed" % (dns_server.strip()))
    return None


def build_list(hostname, dns_list):
    reg_exp = re.compile("\d+.\d+.\d+.\d+")
    print(hostname)
    ips = map(lambda s: query_host(hostname, s), filter(lambda s: reg_exp.search(s), dns_list))
    ip_set = frozenset(filter(None, ips))  # remove empty and the same IP
    pings = map(get_avr_ping, ip_set)
    result = list(zip(ip_set, pings))  # result format: [ip, ping]
    result.sort(key=lambda s: s[1])  # sort the result
    INFO('#' * 20)
    for each in result:
        print("{ip}\t{time} ms\t{loc}".format(ip=each[0], time=each[1], loc=ip_location(each[0])))
    return

    #old code
    for server in dns_list:
        if reg_exp.search(server):
            ip = query_host(hostname, server)
            ping = get_avr_ping(ip)
            print("IP:{ip}\t{time} ms".format(ip=ip, time=ping))


if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    a = build_list("www.google.com", f.readlines())
