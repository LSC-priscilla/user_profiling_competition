#! /usr/bin/env python
# -*- coding: utf-8 -*-
from gensim import corpora,models

import logging
import codecs
import logging
import re
import collections
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class getstopword():
    def __init__(self,addr):
        self.addr=addr

    def build(self):
        f=open(self.addr)
        content = ''
        count=0
        while True:
            line = f.readline()
            if line:
                content+=(line.split(",",5)[5])
                count+=1
                print count
            else:
                print 'haha'
                f.close()
                dictionary = corpora.Dictionary([content.split()])
                dic=dictionary.doc2bow(content.split())
                result={}
                for (id,c) in dic:
                    result[dictionary.get(id)]=int(c)
                dword=collections.OrderedDict(sorted(result.items(), key = lambda t: -t[1]))
                f=open("count.txt",'w')
                count=0
                for key, value in dword.items():
                    print key
                    count+=1
                    if count>100:
                        break


a=getstopword('train_status.txt')
a.build()

