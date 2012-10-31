#!/usr/bin/env python3
import os
import re
import sys
from ip_location import ip_location


def tracert(host):
    cmd = "traceroute %s" % host
    regexp = re.compile(r".*\(([0-9.]+)\).*")
    p = os.popen(cmd)
    line = p.readline()
    while line:
        m = regexp.match(line)
        if m:
            ip = m.group(1)
            line = line.strip() + "\t" + ip_location(ip) + '\n'
        print(line, end="")
        line = p.readline()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Syntax: %s host" % sys.argv[0])
    tracert(sys.argv[1])
