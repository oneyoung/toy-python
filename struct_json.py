#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import json
import sys


def convert(obj):
    tmp = json.loads(obj, encoding="utf-8")
    s = json.dumps(tmp, indent=4)
    obj_out = "\n".join(l.rstrip() for l in s.splitlines())
    return obj_out.decode('unicode-escape')


def convert_file(fn_in, fn_out=None):
    fp_in = open(fn_in)
    if fn_out:
        fp_out = open(fn_out, "w")
    else:
        fp_out = sys.stdout

    out = convert(fp_in.read())
    fp_out.write(out.encode("utf-8"))

    fp_in.close()
    fp_out.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        convert_file(sys.argv[1])
    elif len(sys.argv) == 3:
        convert_file(sys.argv[1], sys.argv[2])
    else:
        print ("%s IN_FILE [OUT_FILE]" % sys.argv[0])
