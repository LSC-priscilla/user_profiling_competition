#! /usr/bin/env python
# -*- coding: utf-8 -*-
from gensim import corpora,models
from sklearn import svm,linear_model,tree
import numpy as np
from gensim.models.doc2vec import TaggedDocument

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class haha():
    def __init__(self,addr1):
        self.addr1=addr1#traindata


    def getage(self,age):
        print age
        age=int(age)
        if age <1980:
            return 0
        elif age<1990:
            return 1
        else:
            return 2
    def getaddr(self,addr):
        mes=addr.split()
        dic={"辽宁":0,"吉林":0,"黑龙江":0,
             "北京":1,"天津":1,"河北":1,"山西":1,"内蒙古":1,
             "湖北":2,"湖南":2,"河南":2,
             "江西":3,"山东":3,"江苏":3,"安徽":3,"浙江":3,"福建":3,"上海":3,"台湾":3,
             "宁夏":4,"新疆":4,"青海":4,"陕西":4,"甘肃":4,
             "四川":5,"云南":5,"贵州":5,"西藏":5,"重庆":5,
             "广东":6,"广西":6,"海南":6,"香港":6,"澳门":6,
             "None":-1}
        if dic.has_key(mes[0]):
            return dic[mes[0]]
        else:
            return 7

    def getmess(self):
        file = open(self.addr1)
        dic={}#id:mes
        while True:
            line =file.readline()
            if line:
                info=line.split('||')
                print info
                mes1=0 if info[1]=='m'else 1#sex
                mes2=self.getage(info[2])#age
                mes3=self.getaddr(info[3])#loc
                dic[info[0]]=[mes1,mes2,mes3]
            else:
                file.close()
                return dic



    def getstatus(self,addr):
        f=open(addr)
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
                return user

    def doc_dis(self,content1,size,w2v):
        vec = [0 for i in range(size)]
        content=content1.split()
        for i in range(len(content)):
            for j in range(size):
                if w2v.vocab.has_key(content[i]):
                    vec[j] += w2v[content[i]][j]
        return [i/float(len(content))*100 for i in vec]



    def doc_dis_all(self,dic,size,w2v):
        vec={}
        count=0
        print len(dic)
        for key,value in dic.items():
            vec[key]=self.doc_dis(value,size,w2v)
            count+=1
            print count
        return vec

    def writedis(self,name,dis):
        f=open(name,'w')
        for key,value in dis.items():
            f.write(key)
            f.write(' ')
            for i in value:
                f.write(str(i))
                f.write(' ')
            f.write('\n')
        f.close()

    def load_dis(self,addr):
        dic={}
        f=open(addr)
        while True:
            line=f.readline()
            if(line):
                d=line.split()
                dic[d[0]]=[float(x) for x in d[1:]]
            else:
                return dic




    def builddic(self):
        '''
        sentence = models.doc2vec.TaggedDocument([u'some', u'words', u'here'], [u'SENT_1'])
        print sentence
        model = models.Doc2Vec(size=100, window=8, min_count=0,alpha=0.025, min_alpha=0.025)  # use fixed learning rate
        model.build_vocab([sentence,sentence])
        print(model)
        for epoch in range(10):
            model.train([sentence,sentence])
            model.alpha -= 0.002  # decrease the learning rate
            model.min_alpha = model.alpha  # fix the learning rate, no decay
        print 'done'
        '''
        user=self.getstatus("train_status.txt")
        '''content=[user[key] for key in user.keys()]
        w2v = models.Word2Vec(content, size=100, min_count=5)
        w2v.save("word2vec.data")'''
        w2v=models.Word2Vec.load('word2vec.data')
        print 'already loaded'
        mes = self.getmess()
        print 'mes length'
        print len(mes)
        print len(self.getstatus("test_status.txt"))
        '''
        doc_dis=self.doc_dis_all(user, 100, w2v)
        self.writedis("doc_dis.txt",doc_dis)
        print 'already get matrix'
        test = self.doc_dis_all(self.getstatus("test_status.txt"),100,w2v)
        self.writedis("test_dis.txt", test)
        '''
        doc_dis=self.load_dis("doc_dis.txt")
        test=self.load_dis("test_dis.txt")
        x=[]
        y=[]
        x_train=[]
        x_id=[]
        for key in mes.keys():
            x.append(doc_dis[key])
            y.append(mes[key])
        for key in test.keys():
            x_train.append(test[key])
            x_id.append(key)
        print 'test len'
        print len(test)

        y=np.array(y)
        print 'y'
        print y
        data=[]
        for num in range (3):
            clf=svm.SVC()
            clf.fit(x,y[:,num])
            data.append(clf.predict(x_train))
        print data
        data=np.array(data)
        sex = {0: "m", 1: "f"}
        age={0:"-1979",1:"1980-1989",2:"1990+"}
        loc={0:'东北',1:'华北',2:'华中',3:'华东',4:'西北',5:'西南',6:'华南',7:'境外'}
        f=open("final.csv",'w')
        f.write("uid,age,gender,province"+'\n')
        print len(data)
        for i in range (980):
            line=str(x_id[i])+","+age[data[1][i]]+','+sex[data[0][i]]+','+loc[data[2][i]]+'\n'
            f.write(line)
        f.close()

        '''
        w2v=models.Word2Vec(content,size=100,min_count=5)
        w2v.save("word2vec.data")
        print self.doc_dis_all(content, 100, w2v)

        print 'hhhh'
         hdp = models.hdpmodel.HdpModel(corpus=vec, id2word=dictionary)
        hdp.show_topics(-1)
        lda=hdp.hdp_to_lda()
        print len(content)
        print len(lda[0])
        print len(lda[1][0])
        print lda'''








a=haha('train_labels.txt')
a.builddic()
