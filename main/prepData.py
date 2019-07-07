from gensim import corpora, models, similarities
from stoplist import stoplist
import os

class MyCorpus(object):
    def __init__(self, path, dictionary):
        self.path = path
        self.dictionary = dictionary
    def __iter__(self):
        for line in open(self.path):
            # assume there's one document per line, tokens separated by whitespace
            yield self.dictionary.doc2bow(line.lower().split())

class PrepareTexts:
    '''
    class forms tree files:  
    
    1) .dict of text file - mapping of words
    2) .mm file - vectorised text
    3) .lsi - trained model 
    
    Arguments:
    -------------
    path - os path to file
    stoplist - list of words
    newName - name for files, produced be gensim.
    n - number of topics
    repo - folder in workng directory to save trained models. Specifying folder, don't forget type '/' to make folder, e.g. repo='newdata/'
    -------------
    
    Object make his best to save RAM resources, don't store full files in memmory. 
    
    Developed for Science Search (Monitoring) ends.
    -------------------------------
    TODO: add lda, word2vec models.
    -------------------------------
    '''
    def __init__(self, path, stoplist=stoplist, newNames='processedFiles', n=5, repo=''): 
        '''
        path to initial text. It's assumed that separate docs separeted by new line (\n)
        ''' 
        self.path = path
        self.stop = stoplist
        self.name = newNames
        self.dictionary = None
        self.n = n
        self.corpus = None
        self.lsi = None
        self.repo = repo
        if repo != '' and os.path.exists(repo) == False: # для того, чтобы сохрнять в директорию, которой может не быть 
            os.mkdir(repo)
        #self.six = __import__('six')
    def diction(self): 
        '''
        Form dictonary from gensim.corpora. Corpora module should be imported'''
        dictionary = corpora.Dictionary(line.lower().split() for line in open(self.path)) # memory friendly way to make dictionary
        stop_ids = [dictionary.token2id[stopword] for stopword in self.stop if stopword in dictionary.token2id] # itartion over dictionary to remove stopwords
        once_ids = [tokenid for tokenid, docfreq in dict.items(dictionary.dfs) if docfreq == 1] # take ids of stop words 
        dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
        self.dictionary = dictionary # make attribute
        dictionary.save(self.repo+self.name+'.dict') # save .dict file
        return dictionary # return to assign new variable
    def bow(self): 
        '''
        Method for BOW creation. Run after creation dictionary.  
        '''
        b = MyCorpus(self.path, self.dictionary) # memory friendly way to convert document to bow
        corpora.MmCorpus.serialize(self.repo+self.name+'.mm', b) # save to .mm file
        self.corpus = b # make attribute
        return b # return to assign new variable
    def lsi_modeling(self):
        '''
        LSI model training. Run after corpus creation (bow method).  
        '''
        tfidf = models.TfidfModel(self.corpus) # class initialization
        corpus_tfidf = tfidf[self.corpus] # model training 
        lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=self.n) # model object creation 
        lsi.save(self.repo+self.name+'.lsi') # save model as separate file
        self.lsi = lsi # make attribute
        return lsi # return to assign new variable
    def run(self): 
        self.diction()
        self.bow()
        self.lsi_modeling()


p = PrepareTexts(path='data/corpuses_CUB/aiz_CUB.txt',newNames='aiz', n=1, repo='testest/')
p.run()
