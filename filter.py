import cPickle as pickle
from collections import defaultdict
import  operator

import re
import string

exclude = set(string.punctuation)
table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))
printable = set(string.printable)


'''
vocab_q.add('<EOS>')
vocab_q.add('**NULL**')
vocab_q.add('**UNKNOWN**')
vocab_a.add('<EOS>')
vocab_q.add('**NULL**')
vocab_q.add('**UNKNOWN**')
vocab_a.add('**NULL**')
vocab_a.add('**UNKNOWN**')
'''
import itertools


def unk_swaping():
    fr = open('cleaned_paired_data.txt', 'r').read().split('\n')
    len_q = 100
    len_a = 60
    fw = open('filtered_paried_data.txt', 'w')
    high_q = pickle.load(open('high_freq_s2s.reddit.vocab.enc.pkl', 'r'))
    alter_dict_q = pickle.load(open('alter_dict_s2s.reddit.vocab.enc.pkl', 'r'))
    high_a = pickle.load(open('s2s.reddit.vocab.dec.pkl', 'r'))
    alter_dict_a = pickle.load(open('alter_dict_s2s.reddit.vocab.dec.pkl', 'r'))
    num=0
    bad_tup=0
    for line in fr:
        num+=1
        if num%1000==0:
            print num*100./len(fr)
        line=filter(lambda x: x in printable, line)
        tup=line.split("<EOS>#TAB#")
        if not len(tup)==2: continue
        query=tup[0].split(' ')
        answer=tup[1].split(' ')

        if len(query)>len_q or len(answer)>len_a:
            continue
        new_query=[]
        bad_q=0
        for q in query:
            if q not in high_q:
                if q in alter_dict_q:
                    new_query.append(" ".join(alter_dict_q[q]))
                else:
                    bad_q+=1
            new_query.append(q)

        new_ans=[]
        bad_a=0
        for a in answer:
            if a not in high_a:
                if a in alter_dict_a:
                    new_ans.append(" ".join(alter_dict_a[a]))
                else:
                    bad_a+=1
            new_ans.append(a)

        if bad_q*1./len(query)>0.1 and bad_a*1./len(answer)>0.1:
            bad_tup+=1
            continue
        fw.write(" ".join(new_query)+'<EOS>#TAB#')
        fw.write(" ".join(new_ans)+'\n')
    print bad_tup
    fw.close()


def judge_split(word,high_freq):
    st = 0
    ed = len(word)
    sub_words=[]
    while (st < ed-3):
        if word[st:ed] in high_freq:
            st=ed
            ed=len(word)
            sub_words.append(word[st:ed])
        else:
            ed -= 1
    return sub_words


def clean_vocab(fp):
    vocab=pickle.load(open(fp,'r'))
    high_freq=set()
    for w,freq in vocab:
        if len(w)<15 and freq>3:
            high_freq.add(w)
    alter_dict=defaultdict()
    num=0
    for w,freq in vocab:
        sub_words=judge_split(w, high_freq)
        if w not in high_freq and len(w)>10 and len(sub_words):
            alter_dict[w]=sub_words
            num+=1
    print num

    pickle.dump(high_freq,open('high_freq_'+fp,'w'))
    pickle.dump(alter_dict,open('alter_dict_'+fp,'w'))

    print len(high_freq)


#clean_vocab('s2s.reddit.vocab.enc.txt')


'''
index=0
high_a=set()
high_q=set()
for k, v in vocab_q:
    if v > 1:
        high_q.add(k)
for k,v in vocab_a:
    if v>1:
        high_a.add(k)


    else:

'''
def build_vocab():
    fr = open('cleaned_paired_data.txt', 'r').read().split('\n')
    high_q = defaultdict(int)#open('', 'r')
    high_a = defaultdict(int)#open('s2s.reddit.vocab.dec.pkl', 'r')
    for line in fr:
        line = filter(lambda x: x in printable, line)
        tup = line.split("<EOS>#TAB#")
        if not len(tup) == 2: continue
        query = tup[0].split(' ')
        answer = tup[1].split(' ')
        for q in query:
            q=re.split(regex,q)
            for w in q:
                high_q[w]+=1
        for a in answer:
            a=re.split(regex,a)
            for w in a:
                high_a[w]+=1

    vocab_a = sorted(high_a.items(), key=operator.itemgetter(1), reverse=True)
    vocab_q = sorted(high_q.items(), key=operator.itemgetter(1), reverse=True)

    with open('s2s.reddit.vocab.enc.pkl','w')as f:
        pickle.dump(vocab_q,f)
    with open('s2s.reddit.vocab.dec.pkl','w')as f:
        pickle.dump(vocab_a,f)

    print len(vocab_a)
    print len(vocab_q)
'''
fw=open('s2s.reddit.vocab.enc.txt','w')
for it in high_q:
    fw.write(it+'\n')
fw.close()
fw=open('s2s.reddit.vocab.dec.txt','w')
for it in high_a:
    fw.write(it+'\n')
fw.close()
'''

#build_vocab()
#clean_vocab('s2s.reddit.vocab.dec.pkl')
unk_swaping()

