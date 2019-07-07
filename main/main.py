import logging
logging.basicConfig(filename=u"main.log", format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)

logging.debug( u'debug' )
logging.info( u'info' )

import warnings
warnings.filterwarnings('ignore')


import pandas as pd
from gensim import corpora, models, similarities



from rss import rss # список рассылки
from findDOI import findDOI # функция поиска doi по названию
from ALT import altmetrics # функция поиска альтметрик (нужно понять, какие альтметрики нам нужны)
from stoplist import stoplist #стоп-лист
from rssParser import Parser # класс, который парсит рсс, в датафрейм, - предлагаю его использовать для наполненния
from findJournal import findJournal # функция поиска названия журнала по названию статьи



# p = Parser(rss)
# df = p.main()
#df.to_csv('example_table.csv')
df = pd.read_csv('example_table.csv')

new_path = '/home/serge/Desktop/local_dev/testmodels/'

# загружаем словарь, векторное пространство, модель Lsi (вектороное пространство)
# общий корпус натренированный на pubmed 
dictionary = corpora.Dictionary.load('/home/serge/Desktop/local_dev/pubmed/pubmed5.dict')      #Here and later - the first one is PubMed-based LSI-object, other - CUB-based LSI-objects
corpus = corpora.MmCorpus('/home/serge/Desktop/local_dev/pubmed/pubmed5.mm') 
lsi = models.LsiModel.load('/home/serge/Desktop/local_dev/pubmed/pubmed5.lsi')

# химики куб
dictionary_CUB_chem = corpora.Dictionary.load(new_path+"chem_CUB.dict")
lsi_CUB_chem = models.LsiModel.load(new_path+"chem_CUB.lsi")
corpus_CUB_chem = corpora.MmCorpus(new_path+"chem_CUB.mm")

# онко куб
dictionary_CUB_onco = corpora.Dictionary.load(new_path+"cancer_CUB.dict")
lsi_CUB_onco = models.LsiModel.load(new_path+"cancer_CUB.lsi")
corpus_CUB_onco = corpora.MmCorpus(new_path+"cancer_CUB.mm")

# аутоимунные куб
dictionary_CUB_aiz = corpora.Dictionary.load(new_path+"aiz_CUB.dict")
lsi_CUB_aiz = models.LsiModel.load(new_path+"aiz_CUB.lsi")
corpus_CUB_aiz = corpora.MmCorpus(new_path+"aiz_CUB.mm")

# инфекции куб 
dictionary_CUB_inf = corpora.Dictionary.load(new_path+"infect_CUB.dict")
lsi_CUB_inf = models.LsiModel.load(new_path+"infect_CUB.lsi")
corpus_CUB_inf = corpora.MmCorpus(new_path+"infect_CUB.mm")

# офтальмология куб
dictionary_CUB_eye = corpora.Dictionary.load(new_path+"eye_CUB.dict")
lsi_CUB_eye = models.LsiModel.load(new_path+"eye_CUB.lsi")
corpus_CUB_eye = corpora.MmCorpus(new_path+"eye_CUB.mm")

# гететические куб
dictionary_CUB_gene = corpora.Dictionary.load(new_path+"gene_CUB.dict")
lsi_CUB_gene = models.LsiModel.load(new_path+"gene_CUB.lsi")
corpus_CUB_gene = corpora.MmCorpus(new_path+"gene_CUB.mm")



index = similarities.MatrixSimilarity(lsi[corpus])          #Indexes
index_CUB_chem = similarities.MatrixSimilarity(lsi_CUB_onco[corpus_CUB_chem])
index_CUB_onco = similarities.MatrixSimilarity(lsi_CUB_onco[corpus_CUB_onco])
index_CUB_aiz = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_aiz])
index_CUB_inf = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_inf])
index_CUB_eye = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_eye])
index_CUB_gene = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_gene])



