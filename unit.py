#! /usr/bin/env python
# -*- coding: utf-8 -*-
from gensim import corpora,models

import logging
import codecs
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class haha():
    def __init__(self,addr,addr1):
        self.addr=addr#status
        self.addr1=addr1

    def getstatus(self):
        f=open(self.addr)
        state=[]
        userid=''
        user={}
        while True:
            line = f.readline()
            if line:
                info=line.split(",",5)
                if userid==info[0]:
                    state+=info[5]
                else:
                    if userid:
                        user[userid]=state
                    userid=info[0]
                    state=info[5]
            else:
                user[userid]=state
                print state
                return user

    def doc_dis(self,content,size,w2v):
        vec = [0 for i in range(size)]
        for i in range(len(content)):
            for j in range(size):
                if w2v.vocab.has_key(content[i]):
                    vec[j] += w2v[content[i]][j]
        sum=0.0
        for i in range (size):
            sum+=(vec[i]*vec[i])
        return [j/sum for j in vec]

    def doc_dis_all(self,content,size,w2v):
        vec=[]
        for i in range (len(content)):
            vec.append(self.doc_dis(content[i],size,w2v))
        return vec





    def builddic(self):
        self.user=self.getstatus()
        usrrec=[]
        content=[]
        for key,value in self.user.items():
            usrrec.append(key)
            content.append(value.split())
            print key,value
        w2v=models.Word2Vec(content,size=100,min_count=5)
        print self.doc_dis_all(content, 100, w2v)
        print 'hhhh'
        ''' hdp = models.hdpmodel.HdpModel(corpus=vec, id2word=dictionary)
        hdp.show_topics(-1)
        lda=hdp.hdp_to_lda()
        print len(content)
        print len(lda[0])
        print len(lda[1][0])
        print lda'''








a=haha("train_status.txt",'train_labels.txt')
a.builddic()
