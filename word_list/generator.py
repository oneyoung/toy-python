#!/usr/bin/env python2
from HTMLParser import HTMLParser
import urllib
import sys


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    def handle_data(self, data):
        self.data.append(data + '\n')


def get_words_from_url(url):
    print "handling URL:<%s>" % url

    fp = urllib.urlopen(url)

    result = filter(lambda line: "<div class=\"wrapco\">" in line, fp.readlines())[0]
    parser = Parser()
    parser.feed(result)
    return parser.data


def handle(output):
    url_templ = "http://www.manythings.org/vocabulary/lists/l/words.php?f=3esl.%02d"

    of = open(output, "w")
    for words in map(get_words_from_url, map(lambda num: url_templ % num, range(1, 24 + 1))):
        of.writelines(words)
    of.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Syntax: %s OUTPUT_FILE" % sys.argv[0]
        exit(-1)
    handle(sys.argv[1])
