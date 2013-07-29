#!/usr/bin/env python2
from md import MdBase
from os import path


def build(f_en, f_cn):
    tpl = path.join(path.dirname(__file__), 'resume.tpl.html')
    md = MdBase(tpl=tpl)
    en = md.convert(f_en)
    cn = md.convert(f_cn)

    out = md.render({'en': en, 'cn': cn})
    md.save(out, 'resume.html')


def get_option(sysargs):
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-c", "--cnfile", dest="cnfile", default="cn.md",
                      help="Chinese Resume, default cn.md", metavar="file")
    parser.add_option("-e", "--enfile", dest="enfile", default="en.md",
                      help="English Resume, default en.md")

    (options, args) = parser.parse_args(sysargs)
    return options


if __name__ == '__main__':
    import sys
    opts = get_option(sys.argv)
    build(opts.enfile, opts.cnfile)
