import numpy as np
from inlinepatterns import Pattern
import json
import cPickle as pickle
from collections import defaultdict
import itertools
import sys

import nltk
from jinja2 import Template

# coment_id1
# comment_name(the same as id1), comment_body parent_name link_id
# ups, down, score,author
# subreddit_name, subreddit_id

CHART_TEMPLATE='base.html'

class Item(object):
    patten= Pattern()
    def __init__(self,param):

        if len(param)==11:
            #self.id=param[0]
            self.id=param[1]
            self.body=[self.patten.sub_text(param[2]),]
            self.p_id=param[3]
            self.link_id=param[4]
            self.visited=[]
            #self.ups=param[5] #
            #self.down=param[6] #
            #self.score=param[7] #
            #self.author=param[8] #
            #self.subreddit_name=param[9] #
            #self.subreddit_id=param[10] #
        else:
            raise ValueError('text line length '+str(len(param))+'does not match ')


def preprocess(filename):
    fr=open(filename,'r').read().split('\n')

    reddit_list=[]
    tree={}
    print 'reading...'
    index=0
    sumlen=len(fr)
    for line in fr:
        index+=1
        print index*1.0/sumlen,'\r',
        sys.stdout.flush()
        if len(line)<=1:   continue
        item=Item(line.split('\t'))
        reddit_list.append(item)
        tree[item.id]=item

    print 'building tree....'
    index=0
    sumlen=len(reddit_list)
    for it in reddit_list:
        index+=1
        print index*1.0/sumlen,'\r',
        sys.stdout.flush()
        while it.p_id in tree:
            p_it=tree[it.p_id]
            it.p_id = p_it.p_id
            p_it.visited.append(it.body[0])
            it.body = p_it.body + it.body

    multiturn=[]
    singleturn=[]
    print 'building dataset....'
    index=0
    sumlen=len(reddit_list)
    for it in reddit_list:
        index+=1
        print index*1.0/sumlen,'\r',
        sys.stdout.flush()
        if len(it.visited)==0 and len(it.body)>1:
            multiturn.append(it.body)
        elif len(it.visited)>0 :
            singleturn.append((it.body[-1],it.visited))

    with open('multiturn.json','w')as f:
        json.dump(multiturn,f)
    with open('singleturn.json','w')as f:
        json.dump(singleturn,f)






def plot_distribution(data_list,response):

    freq_dist={}
    merged_list=list(itertools.chain(*data_list))
    for item in merged_list:
        key=len(item.split(' '))
        if key in freq_dist:
            freq_dist[key]+=1
        else:
            freq_dist[key]=1

    length_data = [['Sentence length','Counter'],]
    for it in freq_dist.items():
        length_data.append([str(it[0]),it[1]])
    response_data=[["Sentence Response",'Counter'],]
    for it in response:
        response_data.append([str(it[0]),it[1]])

    chart_templates=open(CHART_TEMPLATE,'r').read()
    template=Template(chart_templates)
    data2vis=template.render(length_data=str(length_data),resopnse_data=str(response_data))
    fw=open('data2vis.html', 'w')
    fw.write(data2vis)
    fw.flush()
    fw.close()

import operator

def plot_query_and_answer():
    with open('query_dist.pkl','r')as f:
        q=pickle.load(f)
    with open('answer_dist.pkl', 'r')as f:
        a = pickle.load(f)
    q=sorted(q.items(), key=operator.itemgetter(0))#, reverse=True)
    a=sorted(a.items(), key=operator.itemgetter(0))#, reverse=True)

    sumed_q=0
    accu_q=[]
    for k,v in q:

        sumed_q+=v
        accu_q.append((k,sumed_q))


    sumed_a = 0
    accu_a = []
    for k, v in a:
        sumed_a += v
        accu_a.append((k, sumed_a))

    accu_q = [(k,v*100.0/sumed_q)for k,v in accu_q]
    print sumed_q
    print accu_q[50],accu_q[50][1]*sumed_q/100
    print accu_q[100],accu_q[100][1]*sumed_q/100
    accu_a = [(k, v * 100.0 / sumed_a) for k, v in accu_a]
    print sumed_a
    print accu_a[50],accu_a[50][1]*sumed_a/100
    print accu_a[100],accu_a[100][1]*sumed_a/100



    length_data = [['Query length','Coverage (%)'],]
    for it in accu_q:
        length_data.append([str(it[0]),it[1]])
    response_data=[["Answer length",'Coverage (%)'],]
    for it in accu_a:
        response_data.append([str(it[0]),it[1]])

    chart_templates=open(CHART_TEMPLATE,'r').read()
    template=Template(chart_templates)
    data2vis=template.render(length_data=str(length_data),resopnse_data=str(response_data))
    fw=open('data2vis.html', 'w')
    fw.write(data2vis)
    fw.flush()
    fw.close()


if __name__ == "__main__":
    preprocess('combined')

    #clean_corpus('extracted_texts.pkl')
    #plot_distribution(comt,res)
    #plot_query_and_answer()
