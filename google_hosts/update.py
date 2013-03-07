#!/usr/bin/env python2
import re
import sys
import os
import gevent
from gevent import monkey


class HostUtils():
    banner = "##### Google #####"
    default_hostname = "www.google.com"

    @staticmethod
    def get_hostname(line):
        # match "8.8.8.8 hostname.com"
        m = re.match("(\d+\.\d+\.\d+\.\d+)\s+(\S+)", line)
        if m:
            return m.group(2)

    @staticmethod
    def get_addr(hostname):
        cmd = "host %s 8.8.8.8" % hostname
        pipe = os.popen(cmd)
        for line in pipe.readlines():
            if "has address" in line:
                return line.split()[-1]
        print("[Error]Host %s not found" % hostname)

    def __init__(self):
        self._default_addr = self.get_addr(self.default_hostname)
        self._white_list = set()
        self._black_list = set()

    def is_addr_avail(self, host):
        def is_avail():
            cmd = "ping -q -c 1 -W 1 %s" % host
            p = os.popen(cmd)
            try:
                tmp = p.readlines()[-1].split()[-2]  # tmp = "183.628/254.661/326.847/66.045"
            except IndexError:  # catch except if host is unreachable
                return False
            result = float(tmp.split("/")[1])
            return result < 200

        if host in self._white_list:
            ret = True
        elif host in self._black_list:
            ret = False
        else:
            if is_avail():
                self._white_list.add(host)
                ret = True
            else:
                self._black_list.add(host)
                ret = False
        return ret

    def gen(self, filename, ip_addr=None):
        result = []
        f = open(filename, 'r')

        line = ''
        while self.banner not in line:
            line = f.readline()
            result.append(line)

        if ip_addr:
            return result + list(map(lambda host: "{0} {1}\n".format(ip_addr, host),
                                     filter(None, map(self.get_hostname, f.readlines()))))
        else:
            hosts = set(filter(None, map(self.get_hostname, f.readlines())))
            threads = map(lambda h: gevent.spawn(self.get_addr, h), hosts)
            gevent.joinall(threads)
            pairs = filter(lambda p: p[0], zip(map(lambda g: g.value, threads), hosts))
            threads = map(lambda p: gevent.spawn(self.is_addr_avail, p[0]), pairs)
            gevent.joinall(threads)
            dc = {}
            for (avail, (addr, host)) in zip(map(lambda g: g.value, threads), pairs):
                dc[host] = addr if avail else self._default_addr
            return result + list(map(lambda host: "%s\t%s\n" % (dc[host], host), dc))

monkey.patch_socket()
if __name__ == "__main__":
    utils = HostUtils()
    if len(sys.argv) == 3:
        result = utils.gen(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        result = utils.gen(sys.argv[1])
    else:
        print ("Syntax: %s HOST_FILE [IP]" % sys.argv[0])
        exit(-1)

    f = open("/tmp/hosts", "w")
    f.writelines(result)
    f.close()
