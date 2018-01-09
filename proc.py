fw=open('paired_data.txt','w')
import nltk
import cPickle as pickle
from transformation import Item
reddit_list=pickle.load(open('reddit_list.pkl','r'))
from collections import defaultdict

len_q=defaultdict(int)
len_a=defaultdict(int)
for it in reddit_list:
    if len(it.visited)!=0 and len(it.body)==1:
        continue
    temp=" ".join(nltk.word_tokenize(unicode(it.body[0],errors='ignore')))
    len_q[len(temp)]+=1
    for i in range(1,len(it.body)):
        current_line=" ".join(nltk.word_tokenize(unicode(it.body[i],errors='ignore')))
        len_a[len(current_line)]+=1
        fw.write(temp+" <EOS>#TAB#"+current_line+'\n')
        temp=current_line

with open('len_q.pkl','w')as f:
    pickle.dump(len_q,f)
with open('len_a.pkl','w')as f:
    pickle.dump(len_a,f)

fw.close()

