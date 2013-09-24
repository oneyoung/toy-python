#!/usr/bin/env python2
import imp
import sys


def generate_pyc(name):
    sys.path.append('.')
    fp, pathname, desc = imp.find_module(name)
    try:
        imp.load_module(name, fp, pathname, desc)
    finally:
        if fp:
            fp.close()

if __name__ == "__main__":
    generate_pyc(sys.argv[1])
