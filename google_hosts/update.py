#!/usr/bin/env python2
import re
import sys
import os
import gevent
from gevent import monkey


monkey.patch_socket()


re_expr = re.compile("(\d+\.\d+\.\d+\.\d+)\s+(\S+)")  # match "8.8.8.8 hostname.com"
banner = "##### Google #####"


def get_hostname(line):
    m = re_expr.match(line)
    if m:
        return m.group(2)


def get_addr(hostname):
    cmd = "host %s 8.8.8.8" % hostname
    pipe = os.popen(cmd)
    for line in pipe.readlines():
        if "has address" in line:
            return line.split()[-1]
    print("[Error]Host %s not found" % hostname)


white_list = set()
black_list = set()


def is_addr_avail(host):
    def is_avail():
        cmd = "ping -q -c 1 -W 1 %s" % host
        p = os.popen(cmd)
        try:
            tmp = p.readlines()[-1].split()[-2]  # tmp = "183.628/254.661/326.847/66.045"
        except IndexError:  # catch except if host is unreachable
            return False
        result = float(tmp.split("/")[1])
        return result < 200

    if host in white_list:
        ret = True
    elif host in black_list:
        ret = False
    else:
        if is_avail():
            white_list.add(host)
            ret = True
        else:
            black_list.add(host)
            ret = False
    return ret


def gen(filename, ip_addr=None):
    result = []
    f = open(filename, 'r')

    line = ''
    while banner not in line:
        line = f.readline()
        result.append(line)

    if ip_addr:
        return result + list(map(lambda host: "{0} {1}\n".format(ip_addr, host),
                                 filter(None, map(get_hostname, f.readlines()))))
    else:
        hosts = set(filter(None, map(get_hostname, f.readlines())))
        threads = map(lambda h: gevent.spawn(get_addr, h), hosts)
        gevent.joinall(threads)
        pairs = filter(lambda p: p[0], zip(map(lambda g: g.value, threads), hosts))
        threads = map(lambda p: gevent.spawn(is_addr_avail, p[0]), pairs)
        gevent.joinall(threads)
        dc = {}
        for (avail, (addr, host)) in zip(map(lambda g: g.value, threads), pairs):
            dc[host] = addr if avail else DEFAULT_ADDR
        return result + list(map(lambda host: "%s\t%s\n" % (dc[host], host), dc))

DEFAULT_ADDR = get_addr("www.google.com")
if __name__ == "__main__":
    if len(sys.argv) == 3:
        result = gen(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        result = gen(sys.argv[1])
    else:
        print ("Syntax: %s HOST_FILE [IP]" % sys.argv[0])
        exit(-1)

    f = open("/tmp/hosts", "w")
    f.writelines(result)
    f.close()
