#!/usr/bin/env python3

import socket
import re
import sys
import os


re_expr = re.compile("(\d+\.\d+\.\d+\.\d+)\s+(\S+)")  # match "8.8.8.8 hostname.com"
banner = "##### Google #####"


def get_hostname(line):
    m = re_expr.match(line)
    if m:
        return m.group(2)


def get_addr(hostname):
    cmd = "host %s 8.8.8.8"%hostname
    pipe = os.popen(cmd)
    for line in pipe.readlines():
        if "has address" in line:
            return line.split()[-1]
    print("Error: no host found")


def gen(filename, ip_addr):
    result = []
    f = open(filename, 'r')

    while True:
        line = f.readline()
        result.append(line)
        if banner in line:
            break
    return result + list(map(lambda host: "{0} {1}\n".format(ip_addr, host), filter(None, map(get_hostname, f.readlines()))))


if len(sys.argv) == 3:
    result = gen(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
    result = gen(sys.argv[1], get_addr("www.google.com"))
else:
    print("Syntax: %s HOST_FILE [IP]"%sys.argv[0])
    exit(-1)
for i in result:
    print(i, end = "")
