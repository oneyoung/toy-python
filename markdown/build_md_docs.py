#!/usr/bin/env python2
import markdown
import os
import codecs
import json


class build_docs():

    def __init__(self, **kwargs):
        self.indir = kwargs.pop("indir", ".")
        self.outdir = kwargs.pop("outdir", ".")
        self.tpl = kwargs.pop("tpl", None)
        self.tpl_conf = kwargs.pop("tpl_conf", None)
        self.extension = kwargs.pop("extension", ['fenced_code'])

        self.finalize_options()

    def _get_docs(self):
        for root, dirs, files in os.walk(self.indir):
            for f in files:
                if f.endswith(".md"):
                    path = os.path.join(root, f)
                    yield path

    def finalize_options(self):
        self.docs = self._get_docs()
        self.template = self._get_tpl()

    def _get_tpl(self):
        try:
            if self.tpl:
                conf = {}
                f = codecs.open(self.tpl, encoding='utf-8')
                template = f.read()
                f.close()
                if self.tpl_conf:
                    fp_conf = open(self.tpl_conf)
                    conf = json.load(fp_conf, encoding='utf-8')
                    fp_conf.close()
                # TODO: there is something wrong with template, just return
                # template now
                #return template % conf
                return template
        except IndexError:
            print ("generate template failed, skip.")

    def run(self):
        md = markdown.Markdown(extensions=self.extension)
        for infile in self.docs:
            fname = os.path.basename(infile).split('.')[0] + ".html"
            outfile = os.path.join(os.path.realpath(self.outdir), fname)
            print ('Conv %s ==> %s' % (infile, outfile))
            f = codecs.open(infile, encoding='utf-8')
            body = md.convert(f.read())
            f.close()
            if self.template:
                out = self.template % {'body': body}
            else:
                out = body
            doc = open(outfile, 'wb')
            doc.write(out.encode('utf-8'))
            doc.close()


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
    build = build_docs(tpl="template.html")
    build.run()
