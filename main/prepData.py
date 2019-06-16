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
    -------------
    
    Object make his best to save RAM resources, don't store full files in memmory. 
    
    Developed for Science Search (Monitoring) ends. 
    '''
    def __init__(self, path, stoplist=stoplist, newNames='processedFiles', n=5): 
        '''path to initial text. It's assumed that separate docs separeted by new line (\n)''' 
        self.path = path
        self.stop = stoplist
        self.name = newNames
        self.dictionary = None
        self.n = n
        self.corpus = None
        self.lsi = None
    def diction(self): 
        '''Form dictonary from gensim.corpora. Corpora module should be imported'''
        dictionary = corpora.Dictionary(line.lower().split() for line in open(self.path))
        stop_ids = [dictionary.token2id[stopword] for stopword in self.stop if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
        self.dictionary = dictionary
        dictionary.save(self.name+'.dict')
        return dictionary
    def bow(self): 
        b = MyCorpus(self.path, self.dictionary)
        corpora.MmCorpus.serialize(self.name+'.mm', b)
        self.corpus = b
        return b
    def lsi_modeling(self):
        tfidf = models.TfidfModel(self.corpus)
        corpus_tfidf = tfidf[self.corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=self.n)   
        lsi.save(self.name+'.lsi') 
        self.lsi = lsi
        return lsi
    def run(self): 
        self.diction()
        self.bow()
        self.lsi_modeling()
