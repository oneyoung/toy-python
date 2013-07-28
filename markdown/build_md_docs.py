#!/usr/bin/env python2
import markdown
import os
import codecs


class MdBase():
    def __init__(self, **kwargs):
        self.extension = kwargs.pop("extension", ['fenced_code'])
        self.md = markdown.Markdown(extensions=self.extension)

        tpl = kwargs.pop("tpl", None)
        self.template = self.read(tpl) if tpl else None

    def has_template(self):
        return True if self.template else False

    def read(self, fpath):
        f = codecs.open(fpath, encoding='utf-8')
        content = f.read()
        f.close()

        return content

    def convert(self, md):
        '''
        convert markdown file to html string.
        para: md can be file object or file path
        return: html string.
        '''
        if isinstance(md, file):
            f = md
        elif isinstance(md, str):
            f = codecs.open(md, encoding='utf-8')
        return self.md.convert(f.read())

    def render(self, **kwargs):
        '''
        render html with template
        '''
        return self.template % kwargs

    def save(self, strs, fpath):
        '''
        save strs to fpath
        '''
        doc = open(fpath, 'wb')
        doc.write(strs.encode('utf-8'))
        doc.close()


def scan_dir(indir='.', outdir='.', **kwargs):
        md = MdBase(kwargs)

        def docs():
            for root, dirs, files in os.walk(indir):
                for f in files:
                    if f.endswith(".md"):
                        path = os.path.join(root, f)
                        yield path

        for infile in docs():
            fname = os.path.basename(infile).split('.')[0] + ".html"
            outfile = os.path.join(os.path.realpath(outdir), fname)
            print ('Conv %s ==> %s' % (infile, outfile))
            body = md.convert(infile)
            if md.has_template():
                out = md.render({'body': body})
            else:
                out = body
            md.save(out, outfile)


def get_option(sysargs):
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="infile",
                      help="sepcify a input file", metavar="FILE")
    parser.add_option("-i", "--indir", dest="indir",
                      help="dir that contain *.md file, default is current directory")
    parser.add_option("-o", "--outdir", dest="outdir", help="output dir")
    parser.add_option("--tpl", dest="tpl",
                      help="html template, must contain '\%(body)s' ")
    parser.add_option("-e", "--extension", dest="extension",
                      help="use specified extensions")

    (options, args) = parser.parse_args(sysargs)


if __name__ == "__main__":
    scan_dir(tpl="template.html")
