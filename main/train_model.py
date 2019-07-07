from preData import MyCorpus, PrepareTexts

import warnings
warnings.filterwarnings('ignore')

from stoplist import stoplist
import os

path_to_files = '/home/serge/Desktop/lsi_model/data/corpuses_CUB/'


for i in os.listdir(path_to_files): 
    p = PrepareTexts(path=path_to_files+i,newNames=i.split('.')[0], n=1, repo='testmodels/')
    p.run()
    
pubmed = '/home/serge/Desktop/lsi_model/data/corpus_pubmed_clean_5docs.txt'
p = PrepareTexts(path=pubmed,newNames='pubmed5', n=1, repo='pubmed/')
p.run()
