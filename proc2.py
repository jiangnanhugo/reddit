import json
from collections import defaultdict
singleturn=json.load(open('cleaned_singleturn.json','r'))

en_vocab=defaultdict(int)
de_vocab=defaultdict(int)
TOKENS=' <EOS>#TAB#'

def build_vocab(words,vocab):
    for w in words:
        if len(w)>1:
            vocab[w]+=1


fw=open('cleaned_paired_data.txt','w')
for q,a in singleturn:
    sp_q=q.split(' ')
    sp_a=a.split(' ')
    if len(sp_q)>100 or len(sp_a)>60: continue
    build_vocab(sp_q,en_vocab)
    build_vocab(sp_a,de_vocab)
    string=q+TOKENS+a+'\n'
    try:
        fw.write(string)
    except Exception:
        fw.write(string.encode('utf-8','ignore'))
fw.flush()
fw.close()

import operator
def sort_and_prun(x):
    print len(x)
    sorted_x = sorted(x.items(), key=operator.itemgetter(1),reverse=True)
    ratio=0.9
    xlen=int(len(sorted_x)*ratio)
    pruned_x=sorted_x[:xlen]
    print len(pruned_x)
    return pruned_x
sort_en_vocab=sort_and_prun(en_vocab)
sort_de_vocab=sort_and_prun(de_vocab)
def save(vocab,fp):
    fw=open(fp,'w')
    for k,v in vocab:
        try:
            fw.write(k+'\n')
        except Exception:
            fw.write(k.encode('utf-8','ignore')+'\n')
    fw.close()
save(sort_en_vocab,'encoder_vocab.txt')
save(sort_de_vocab,'decoder_vocab.txt')
