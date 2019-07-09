from enhancment_words import cancerdict, aizdict, infectdict, eyedict, genedict, chemdict
import spacy
from gensim import corpora, models, similarities
import numpy as np
import operator as op
import re
from stoplist import stoplist


nlp = spacy.load('en', parser=False, ner=False)


new_path = '/home/BIOCAD/chuvakin/serge/science_search/pubmed_model/'
new_path_CUB = '/home/BIOCAD/chuvakin/serge/science_search/CUB_models/'

# загружаем словарь, векторное пространство, модель Lsi (вектороное пространство)
# общий корпус натренированный на pubmed 
dictionary = corpora.Dictionary.load(new_path+'pubmed5.dict')      #Here and later - the first one is PubMed-based LSI-object, other - CUB-based LSI-objects
corpus = corpora.MmCorpus(new_path+'pubmed5.mm') 
lsi = models.LsiModel.load(new_path+'pubmed5.lsi')

# химики куб
dictionary_CUB_chem = corpora.Dictionary.load(new_path_CUB+"chem_CUB.dict")
lsi_CUB_chem = models.LsiModel.load(new_path_CUB+"chem_CUB.lsi")
corpus_CUB_chem = corpora.MmCorpus(new_path_CUB+"chem_CUB.mm")

# онко куб
dictionary_CUB_onco = corpora.Dictionary.load(new_path_CUB+"cancer_CUB.dict")
lsi_CUB_onco = models.LsiModel.load(new_path_CUB+"cancer_CUB.lsi")
corpus_CUB_onco = corpora.MmCorpus(new_path_CUB+"cancer_CUB.mm")

# аутоимунные куб
dictionary_CUB_aiz = corpora.Dictionary.load(new_path_CUB+"aiz_CUB.dict")
lsi_CUB_aiz = models.LsiModel.load(new_path_CUB+"aiz_CUB.lsi")
corpus_CUB_aiz = corpora.MmCorpus(new_path_CUB+"aiz_CUB.mm")

# инфекции куб 
dictionary_CUB_inf = corpora.Dictionary.load(new_path_CUB+"infect_CUB.dict")
lsi_CUB_inf = models.LsiModel.load(new_path_CUB+"infect_CUB.lsi")
corpus_CUB_inf = corpora.MmCorpus(new_path_CUB+"infect_CUB.mm")

# офтальмология куб
dictionary_CUB_eye = corpora.Dictionary.load(new_path_CUB+"eye_CUB.dict")
lsi_CUB_eye = models.LsiModel.load(new_path_CUB+"eye_CUB.lsi")
corpus_CUB_eye = corpora.MmCorpus(new_path_CUB+"eye_CUB.mm")

# гететические куб
dictionary_CUB_gene = corpora.Dictionary.load(new_path_CUB+"gene_CUB.dict")
lsi_CUB_gene = models.LsiModel.load(new_path_CUB+"gene_CUB.lsi")
corpus_CUB_gene = corpora.MmCorpus(new_path_CUB+"gene_CUB.mm")



index = similarities.MatrixSimilarity(lsi[corpus])          #Indexes
index_CUB_chem = similarities.MatrixSimilarity(lsi_CUB_chem[corpus_CUB_chem])
index_CUB_onco = similarities.MatrixSimilarity(lsi_CUB_onco[corpus_CUB_onco])
index_CUB_aiz = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_aiz])
index_CUB_inf = similarities.MatrixSimilarity(lsi_CUB_inf[corpus_CUB_inf])
index_CUB_eye = similarities.MatrixSimilarity(lsi_CUB_eye[corpus_CUB_eye])
index_CUB_gene = similarities.MatrixSimilarity(lsi_CUB_gene[corpus_CUB_gene])




def lemmatization(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'], stoplist=stoplist):
    """https://spacy.io/api/annotation"""
    sentence = []
    doc_lem = nlp(text)
    for token in doc_lem:
        if token.pos_ in allowed_postags:
            sentence.append(token.lemma_)
        else:
            sentence.append(token)

    docs_out = " ".join(str(i).lower() for i in sentence)
    docs_out = re.sub(r' - ', '-', docs_out, flags=re.I)
    docs_out = re.sub(r'[^A-Za-z0-9\-]', ' ', docs_out)
    docs_out = re.sub(r' \d+ ', ' ', docs_out)
    docs_out = re.sub(r'\s+', ' ', docs_out)

    del doc_lem
    return docs_out

def scores_themes(txt, cancerdict=cancerdict, aizdict=aizdict, infectdict=infectdict, eyedict=eyedict, genedict=genedict, chemdict=chemdict, short=False, stoplist=stoplist):
    '''
    Note that the order of multipliers should correspond the order d rule.
    
    Function returns following values:
    
    - theme: topic based on cosine similarity
    - chem_multiplier: chemical score, which is number of token occurences in chemical dict
    - score_pubmed: lsi score, based on svd decomposition
    - score_CUB: wierd number, seems to be constant all the time 
    - theme_lsi: theme based in svd decomposition
    
    NB: lsi model returns empty list on too short texts, therefore don't forget to check short=True
    
    TODO: remove extra scores. Focus on just appropriate values. Right order of themes. 
    '''
    assert type(txt)==str, 'на вход подается не текст'

    txt = txt.lower() # lower register
    words = corpora.Dictionary([txt.split()]) # own dictionary
    ids = words.token2id # dictionary of tokens 

    # lists of ids of enhancemnet words
    cancer_idlist = [ids[i] for i in list(set(ids.keys()) & set(cancerdict)) if i in ids]
    aiz_idlist = [ids[i] for i in list(set(ids.keys()) & set(aizdict)) if i in ids]
    infect_idlist = [ids[i] for i in list(set(ids.keys()) & set(infectdict)) if i in ids]
    eye_idlist = [ids[i] for i in list(set(ids.keys()) & set(eyedict)) if i in ids]
    gene_idlist = [ids[i] for i in list(set(ids.keys()) & set(genedict)) if i in ids]
    chem_idlist = [ids[i] for i in list(set(ids.keys()) & set(chemdict)) if i in ids]

    # vectorize article abstract
    words = words.doc2bow(txt.split())

    # lists of multipliers
    cancer_multiplier = sum([e[1] for e in words if e[0] in cancer_idlist])
    aiz_multiplier = sum([e[1] for e in words if e[0] in aiz_idlist])
    infect_multiplier = sum([e[1] for e in words if e[0] in infect_idlist])
    eye_multiplier = sum([e[1] for e in words if e[0] in eye_idlist])
    gene_multiplier = sum([e[1] for e in words if e[0] in gene_idlist])
    chem_multiplier = sum([e[1] for e in words if e[0] in chem_idlist])

    # one multiplier
    multipliers = [eye_multiplier, cancer_multiplier ,  gene_multiplier, aiz_multiplier, infect_multiplier]
    multipliers = np.array([(1+0.08*y) for y in multipliers])
    if short==False:
        # preproc 
        txt = lemmatization(txt, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
        txt = [x for x in txt.split() if x not in stoplist]

        # preporation for model estimation
        vec_bow = dictionary.doc2bow(txt)
        vec_bow_chem = dictionary_CUB_chem.doc2bow(txt)

        # modeling
        vec_lsi = lsi[vec_bow]      # convert the query to LSI space
        vec_lsi_chem = lsi_CUB_chem[vec_bow_chem]

        # find similarities
        sims  = index[vec_lsi] * multipliers
        sims_chem = index_CUB_chem[vec_lsi_chem] # наверное это лишнее

        #  темы 
        d = dict(zip(['глаза', 'онко', 'геннетические', 'аутоимунные', 'инфекции'], sims))

        # find most relevant topic, which is more than 0.65 score similarity 
        try:
            theme, score_pubmed = max(list(filter(lambda x: x[1]>0.65, d.items())), key=op.itemgetter(1))
        except: 
            theme, score_pubmed = 'uncategorized', np.nan

        score_chem = sum(sims_chem) # зачем это??

        # define theme by lsi_model 
        theme_lsi, score_lsi = sorted([(x[0],x[1]*y) for x, y in zip(vec_lsi, multipliers)], key=op.itemgetter(1), reverse=True)[0]
        theme_lsi = dict(enumerate(d.keys()))[theme_lsi] 


        # count similirities with cub (Всегда отдает одно число!)
        if  theme == "онко":
            vec_bow_CUB = dictionary_CUB_onco.doc2bow(txt)
            vec_lsi_CUB = lsi_CUB_onco[vec_bow_CUB]
            sims_CUB = index_CUB_onco[vec_lsi_CUB]
        elif theme == "аутоимунные":
            vec_bow_CUB = dictionary_CUB_aiz.doc2bow(txt)
            vec_lsi_CUB = lsi_CUB_aiz[vec_bow_CUB]
            sims_CUB = index_CUB_aiz[vec_lsi_CUB]
        elif theme == "инфекции":
            vec_bow_CUB = dictionary_CUB_inf.doc2bow(txt)
            vec_lsi_CUB = lsi_CUB_inf[vec_bow_CUB]
            sims_CUB = index_CUB_inf[vec_lsi_CUB]
        elif theme == "глаза":
            vec_bow_CUB = dictionary_CUB_eye.doc2bow(txt)
            vec_lsi_CUB = lsi_CUB_eye[vec_bow_CUB]
            sims_CUB = index_CUB_eye[vec_lsi_CUB]
        elif theme == "геннетические":
            vec_bow_CUB = dictionary_CUB_gene.doc2bow(txt)
            vec_lsi_CUB = lsi_CUB_gene[vec_bow_CUB]
            sims_CUB = index_CUB_gene[vec_lsi_CUB]
        else:
            sims_CUB = [0,0,0]

        score_CUB = sum(sims_CUB)
    
    else:
        score_CUB = "too short for similarities"
        theme = max(zip(['глаза', 'онко', 'геннетические', 'аутоимунные', 'инфекции'], multipliers), key=op.itemgetter(1))[0]
        theme_lsi = 'undefined'
        score_pubmed = 'undefined'
    return theme, chem_multiplier, score_pubmed, score_CUB, theme_lsi