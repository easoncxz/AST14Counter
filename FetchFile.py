# coding: utf8
__author__ = 'Enigma'

import urllib2


def download_url_to_file(url, file_name):
    print 'Connecting to url...'
    req = urllib2.urlopen(url)
    print 'Loading file...'
    html = req.read()
    f = open(file_name, 'w')
    f.write(html)
    f.close()
    print 'Download url : ', url, '\nto file : ', file_name, 'over.'


def file_convert_pagecode(src_file, src_code, dst_file, dst_code):
    inf = open(src_file, 'r')
    src_text = inf.read()
    inf.close()
    dst_text = src_text.decode(src_code).encode(dst_code)
    ouf = open(dst_file, 'w')
    ouf.write(dst_text)
    ouf.close()