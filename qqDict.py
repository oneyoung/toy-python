#!/usr/bin/env python2
import urllib
import json
import sys
import HTMLParser


class qqDict():
    def __init__(self, word):
        self.word = word

    def fetch(self, word=None):
        urlBase = "http://dict.qq.com/dict?q=%s"
        query = urllib.quote(word if word else self.word)
        url = urlBase % query
        f = urllib.urlopen(url)
        return f.read()

    def unpackJson(self, obj=None):
        d = json.loads(obj if obj else self.fetch(), encoding="utf8")
        return d

    def show(self):
        html_parser = HTMLParser.HTMLParser()
        d = self.unpackJson()
        lang = d.get('lang')

        def handler(root, node, mem_list, sep=" "):
            d = root.get(node, [])
            return "\n".join(map(lambda e: sep.join(
                map(lambda m: html_parser.unescape(e.get(m, "")), mem_list)), d))

        for local in d.get('local', []):
            if lang == "eng":
                for pho in local.get('pho', []):
                    print ("[%s] " % html_parser.unescape(pho))
                print handler(local, 'des', ['p', 'd'], " ")
                print handler(local, 'ph', ['phs', 'phd'], " -- ")
            elif lang == "ch":
                for des in local.get('des', []):
                    print des
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        d = qqDict(" ".join(sys.argv[1:]))
        d.show()
    else:
        print ("%s WORD" % sys.argv[0])
