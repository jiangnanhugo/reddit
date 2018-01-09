
import re
import string

exclude = set(string.punctuation)
table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))

def prune_words(word_list):
    for w in word_list:
        index=w.find('-')
        if index>0 and index<len(w)-1:
          words=w.split('-')


def clean_corpus(fp_q,fp_a):
    q_vocab=open(fp_q,'r').read().split('\n')
    qset=set()
    print len(q_vocab)
    for w in q_vocab:
        w=re.sub(r'[^\x00-\x7F]+', ' ', w)
        words=re.split(regex,w)
        for word in words:
            qset.add(word.strip())
    print qset

    #a_vocab = open(fp_a, 'r').read().split('\n')

clean_corpus('encoder_vocab.txt',"")