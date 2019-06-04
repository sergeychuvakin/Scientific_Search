import feedparser
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
import json
import Levenshtein as lv
import numpy as np
from gensim import corpora, models, similarities
import spacy

rss = [("ScienceDirect Publication: Biotechnology Advances", "http://rss.sciencedirect.com/publication/science/07349750"),
       ("Wiley: Arthritis Care & Research: Table of Contents", "https://onlinelibrary.wiley.com/action/showFeed?jc=21514658&type=etoc&feed=rss"),
       ("Frontiers in Immunology", "https://www.frontiersin.org/journals/immunology/rss"),
       ("Annual Reviews: Annual Review of Immunology: Table of Contents", "https://www.annualreviews.org/action/showFeed?ui=45mu4&mi=3fndc3&ai=sl&jc=immunol&type=etoc&feed=rss"),
       ("ScienceDirect Publication: Clinical Immunology", "http://rss.sciencedirect.com/publication/science/15216616"),
       ("ScienceDirect Publication: Molecular Cell", "http://rss.sciencedirect.com/publication/science/10972765"),
       ("ScienceDirect Publication: Neuroscience", "http://rss.sciencedirect.com/publication/science/03064522"),
       ("ScienceDirect Publication: Journal of Autoimmunity", "https://www.journals.elsevier.com/journal-of-autoimmunity/rss"),
       ("ScienceDirect Publication: EBioMedicine", "http://rss.sciencedirect.com/publication/science/23523964"),
       ("ScienceDirect Publication: DNA Repair", "http://rss.sciencedirect.com/publication/science/15687864"),
       ("ScienceDirect Publication: Bioorganic Chemistry", "http://rss.sciencedirect.com/publication/science/00452068"),
       ("ScienceDirect Publication: Biology of Blood and Marrow Transplantation", "http://rss.sciencedirect.com/publication/science/10838791"),
       ("ScienceDirect Publication: Cancer Treatment Reviews", "http://rss.sciencedirect.com/publication/science/03057372"),
       ("ScienceDirect Publication: Neuropharmacology", "http://rss.sciencedirect.com/publication/science/00283908"),
       ("ScienceDirect Publication: European Journal of Medicinal Chemistry"),
       ("Antimicrobial Agents and Chemotherapy", "https://aac.asm.org/rss/current.xml"),
       ("Journal of Antimicrobial Chemotherapy", "https://academic.oup.com/rss/site_5301/3167.xml"),
       ("PLOS Biology: New Articles", "http://biology.plosjournals.org/perlserv/?request=get-rss&issn=1545-7885&type=new-articles", "1544-9173"),
       ("ScienceDirect Publication: Cell", "http://rss.sciencedirect.com/publication/science/00928674", "0092-8674"),
       ("Molecular Therapy", "http://rss.sciencedirect.com/publication/science/15250016", "1525-0016"),
       ("Current Opinion in Immunology - Just Published", "http://www.current-opinion.com/rss/just-published/current-opinion-in-immunology/", "0952-7915"),
       ("ScienceDirect Publication: Metabolic Engineering", "http://rss.sciencedirect.com/publication/science/10967176", "1096-7176"),
       ("Wiley: The Journal of Gene Medicine: Table of Contents", "https://onlinelibrary.wiley.com/action/showFeed?jc=15212254&type=etoc&feed=rss", "1099-498X"),
       ("Wiley: Angewandte Chemie", "https://onlinelibrary.wiley.com/feed/15213773/most-recent"),
       ("Wiley: Chemical Biology & Drug Design", "https://onlinelibrary.wiley.com/feed/17470285/most-recent"),
       ("Wiley: Cancer Science", "https://onlinelibrary.wiley.com/feed/13497006/most-recent"),
       ("Wiley: Journal of Biochemical and Molecular Toxicology", "https://onlinelibrary.wiley.com/feed/10990461/most-recent"),
       ("Wiley: Journal of Cellular and Molecular Medicine", "https://onlinelibrary.wiley.com/feed/15824934/most-recent"),
       ("Wiley: International Journal of Cancer", "https://onlinelibrary.wiley.com/feed/10970215/most-recent"),
       ("Wiley: Journal of Cellular Physiology", "https://onlinelibrary.wiley.com/feed/10974652/most-recent"),
       ("Wiley: Hepatology", "https://aasldpubs.onlinelibrary.wiley.com/action/showFeed?jc=15273350&type=etoc&feed=rss"),
       ("JAIDS", "https://cdn.journals.lww.com/jaids/_layouts/15/OAKS.Journals/feed.aspx?FeedType=CurrentIssue"),
       ("Wiley: Journal of Viral Hepatology", "https://onlinelibrary.wiley.com/feed/13652893/most-recent"),
       ("ScienceDirect Publication: Immunity", "http://rss.sciencedirect.com/publication/science/10747613", "1074-7613"),
       ("Massachusetts Medical Society: New England Journal of Medicine: Table of Contents", "http://content.nejm.org/rss/current.xml"),
       ("ScienceDirect Publication: Journal of Biotechnology", "http://rss.sciencedirect.com/publication/science/01681656"),
       ("ScienceDirect Publications: Bioorganic and Medicinal Chemistry Letters", "http://rss.sciencedirect.com/publication/science/0960894X"),
       ("Cancer Cell", "http://rss.sciencedirect.com/publication/science/15356108"),
       ("ScienceDirect Publication: Tetrahedron", "https://rss.sciencedirect.com/publication/science/00404020"),
       ("Science Immunology current issue", "http://immunology.sciencemag.org/rss/current.xml"),
       ("Science Translational Medicine", "http://stm.sciencemag.org/rss/current.xml?_ga=2.174655714.1749457138.1528469008-922381873.1528469008"),
       ("Science Signaling", "http://stke.sciencemag.org/rss/current.xml"),
       ("Science current issue", "http://www.sciencemag.org/rss/current.xml"),
       ("Blood current issue", "http://www.bloodjournal.org/rss/current.xml"),
       ("JAMA Oncology Current Issue", "http://oncology.jamanetwork.com/rss/site_159/174.xml"),
       ("JAMA Current Issue", "http://jama.jamanetwork.com/rss/site_3/67.xml"),
       ("The Journal of Immunology current issue", "http://www.jimmunol.org/rss/current.xml"),
       ("Aging and Disease-Forthcoming Articles", "http://www.aginganddisease.org/EN/rss_zxly_2152-5250.xml"),
       ("Aging and Disease-Current Issue", "http://www.aginganddisease.org/EN/rss_dqml_2152-5250.xml"),
       ("Clinical Cancer Research current issue", "http://clincancerres.aacrjournals.org/rss/current.xml"),
       ("JNCI: Journal of the National Cancer Institute Current Issue", "http://jnci.oxfordjournals.org/rss/current.xml"),
       ("Proceedings of the National Academy of Sciences current issue", "http://www.pnas.org/rss/current.xml"),
       ("Most Recent Articles: Arthritis Research & Therapy", "http://arthritis-research.com/latest/rss"),
       ("Journal of Allergy and Clinical Immunology", "http://www.jacionline.org/current.rss"),
       ("Wiley: Biotechnology Journal: Table of Contents", "https://onlinelibrary.wiley.com/action/showFeed?jc=18607314&type=etoc&feed=rss"),
       ("Annals of Oncology Current Issue", "http://annonc.oxfordjournals.org/rss/current.xml"),
       ("Trends in Biotechnology", "http://www.cell.com/trends/biotechnology/current.rss"),
       ("Most Recent Articles: Clinical Epigenetics", "https://clinicalepigeneticsjournal.biomedcentral.com/articles/most-recent/rss.xml"),
       ("The Lancet Oncology comments", "http://www.thelancet.com/rssfeed/lanonc_online.xml"),
       ("The Lancet Oncology", "https://www.thelancet.com/rssfeed/lanonc_current.xml?code=lancet-site"),
       ("Glycobiology Current Issue", "http://glycob.oxfordjournals.org/rss/current.xml"),
       ("Rheumatology Advance Access", "https://academic.oup.com/rss/site_5347/advanceAccess_3213.xml"),
       ("Nucleic Acids Research Current Issue", "http://nar.oxfordjournals.org/rss/current.xml"),
       ("Latest Results for Applied Microbiology and Biotechnology", "http://link.springer.com/search.rss?facet-content-type=Article&facet-journal-id=253&channel-name=Applied%20Microbiology%20and%20Biotechnology"),
       ("Rheumatology Current Issue", "https://academic.oup.com/rss/site_5347/3213.xml"),
       ("Wiley: Immunological Reviews: Table of Contents", "https://onlinelibrary.wiley.com/action/showFeed?jc=1600065x&type=etoc&feed=rss"),
       ("Wiley: Journal of Leukocyte Biology: Table of Contents", "https://jlb.onlinelibrary.wiley.com/action/showFeed?jc=19383673&type=etoc&feed=rss"),
       ("Wiley: CA: A Cancer Journal for Clinicians: Table of Contents", "https://onlinelibrary.wiley.com/action/showFeed?jc=15424863&type=etoc&feed=rss"),
       ("Wiley: Biotechnology and Bioengenineering", "https://onlinelibrary.wiley.com/action/showFeed?jc=10970290&type=etoc&feed=rss"),
       ("Latest Results for Journal of Molecular Medicine", "https://link.springer.com/search.rss?facet-content-type=Article&facet-journal-id=109&channel-name=Journal+of+Molecular+Medicine"),
       ("Rheumatology Current Issue", "http://rheumatology.oxfordjournals.org/rss/current.xml"),
       ("Latest Results for GeroScience", "https://link.springer.com/search.rss?facet-content-type=Article&facet-journal-id=11357&channel-name=GeroScience"),
       ("Clinical Rheumatology", "https://link.springer.com/search.rss?facet-content-type=Article&facet-journal-id=10067&channel-name=Clinical+Rheumatology"),
       ("Nature Reviews Immunology - Issue - nature.com science feeds", "http://feeds.nature.com/nri/rss/current"),
       ("Nature Communications - current - nature.com science feeds", "http://feeds.nature.com/ncomms/rss/current"),
       ("British Journal of Cancer - Issue - nature.com science feeds", "http://feeds.nature.com/bjc/rss/current"),
       ("Blood Cancer Journal - Issue - nature.com science feeds", "http://feeds.nature.com/bcj/rss/current"),
       ("Leukemia - Issue - nature.com science feeds", "http://feeds.nature.com/leu/rss/current"),
       ("Nature - Issue - nature.com science feeds", "http://feeds.nature.com/nature/rss/current"),
       ("Oncogene - Issue - nature.com science feeds", "http://feeds.nature.com/onc/rss/current"),
       ("Nature Biotechnology", "http://www.nature.com/nbt/current_issue/rss/"),
       ("Nature Reviews Cancer - Issue - nature.com science feeds", "http://feeds.nature.com/nrc/rss/current"),
       ("Nature Immunology - Issue - nature.com science feeds", "http://feeds.nature.com/ni/rss/current"),
       ("Nature Reviews Rheumatology - Issue - nature.com science feeds", "http://feeds.nature.com/nrrheum/rss/current"),
       ("Nature Reviews Molecular Cell Biology", "http://feeds.nature.com/nrm/rss/current"),
       ("Nature Medicine - Issue - nature.com science feeds", "http://feeds.nature.com/nm/rss/current"),
       ("Cell Death and Disease - nature.com science feeds", "http://feeds.nature.com/cddis/rss/current"),
       ("Mucosal Immunology - Issue - nature.com science feeds", "http://feeds.nature.com/mi/rss/current"),
       ("Cellular & Molecular Immunology - Issue - nature.com science feeds", "http://feeds.nature.com/cmi/rss/current"),
       ("Journal of Medicinal Chemistry", "http://feeds.feedburner.com/acs/jmcmar"),
       ("Journal of Organic Chemistry", "http://feeds.feedburner.com/acs/joceah"),
       ("Organic Process Research & Development", "http://feeds.feedburner.com/acs/oprdfk"),
       ("Journal of Chemical Information and Modelling", "http://feeds.feedburner.com/acs/jcisd8"),
       ("Biochemistry", "http://feeds.feedburner.com/acs/bichaw"),
       ("Bioconjugate Chemistry", "http://feeds.feedburner.com/acs/bcches"),
       ("Chemical Reviews", "http://feeds.feedburner.com/acs/chreay"),
       ("Organic Letters", "http://feeds.feedburner.com/acs/orlef7"),
       ("Journal of the American Chemical Society", "http://feeds.feedburner.com/acs/jacsat"),
       ("Journal of Clinical Oncology", "http://ascopubs.org/action/showFeed?type=etoc&feed=rss&jc=jco")]

dictionary = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/dictionaries/mincount_50/75000_docs_dict.dict")      #Here and later - the first one is PubMed-based LSI-object, other - CUB-based LSI-objects
dictionary_CUB_chem = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/chem.dict")                 #Dictionaries
dictionary_CUB_onco = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/onco.dict")
dictionary_CUB_aiz = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/aiz.dict")
dictionary_CUB_inf = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/inf.dict")
dictionary_CUB_eye = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/eye.dict")
dictionary_CUB_gene = corpora.Dictionary.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/gene.dict")

lsi = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/models/model_50_mincount_90_topics.lsi")    #Models
lsi_CUB_chem = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/chem.lsi")
lsi_CUB_onco = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/onco_model.lsi")
lsi_CUB_aiz = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/aiz.lsi")
lsi_CUB_inf = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/inf.lsi")
lsi_CUB_eye = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/eye.lsi")
lsi_CUB_gene = models.LsiModel.load("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/gene.lsi")

corpus = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/corpuses_5/corpus_50_mincount.mm")        #Corpuses
corpus_CUB_chem = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_chem.mm")
corpus_CUB_onco = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_onco.mm")
corpus_CUB_aiz = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_aiz.mm")
corpus_CUB_inf = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_inf.mm")
corpus_CUB_eye = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_eye.mm")
corpus_CUB_gene = corpora.MmCorpus("C:/Users/pboby/Desktop/Biocad/TabulaRasa/CUB_based_model/corpus_gene.mm")

index = similarities.MatrixSimilarity(lsi[corpus])          #Indexes
index_CUB_chem = similarities.MatrixSimilarity(lsi_CUB_onco[corpus_CUB_chem])
index_CUB_onco = similarities.MatrixSimilarity(lsi_CUB_onco[corpus_CUB_onco])
index_CUB_aiz = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_aiz])
index_CUB_inf = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_inf])
index_CUB_eye = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_eye])
index_CUB_gene = similarities.MatrixSimilarity(lsi_CUB_aiz[corpus_CUB_gene])

stoplist = set("% a a's able about above abstract according fig accordingly across actually after afterwards again against ain't all allow allows almost alone along already also although always author(s) am among amongst an and another any anybody anyhow anyone anything anyway anyways anywhere apart appear appreciate appropriate are aren't around as aside ask asking associated at available away awfully be became because become becomes becoming been before beforehand behind being believe below beside besides best better between beyond both brief but by c c'mon c's came can can't cannot cant cause causes cells) cell certain certainly changes clearly co com come comes concerning consequently consider considering contain containing contains corresponding could couldn't course currently d definitely described despite did didn't different do does doesn't doing don't done down downwards during e each edu eg eight either else elsewhere enough entirely especially et etc even ever every everybody everyone everything everywhere ex exactly example except f far few fifth first five followed following follows for former formerly forth four from further furthermore g get gets getting given gives go goes going gone got gotten greetings h had hadn't happens hardly has hasn't have haven't having he he's hello help hence her here here's hereafter hereby herein hereupon hers herself hi him himself his hither hopefully how howbeit however i i'd i'll i'm i've ie if ignored immediate in inasmuch inc indeed indicate indicated indicates inner insofar instead into inward is isn't it it'd it'll it's its itself j just k kda keep keeps kept know knows known l last lately later latter latterly least less lest let let's level like liked likely little look looking looks ltd m mainly many may maybe me mean meanwhile methods merely mg mg/kg might more moreover most mostly much must my myself n name namely nd near nearly necessary need needs neither never nevertheless new next nine no nobody non none noone nor normally not nothing novel now nowhere o obviously of off often oh ok okay old on once one ones only onto or other others otherwise ought our ours ourselves out outside over overall own p particular particularly patients per perhaps placed please plus possible presumably probably provides q que quite qv r rather rd re really reasonably regarding regardless regards relatively results respectively right s said same saw say saying says second secondly see seeing seem seemed seeming seems seen self selves sensible sent serious seriously seven several shall she should shouldn't since six so some somebody somehow someone something sometime sometimes somewhat somewhere soon sorry specified specify specifying still study sub such sup sure t's take taken tell tends th than thank thanks thanx that that's thats the their theirs them themselves then thence there there's thereafter thereby therefore therein theres thereupon these they they'd they'll they're they've think third this thorough thoroughly those though three through throughout thru thus to together too took total toward towards treatment tried tries truly try trying twice two u un under unfortunately unless unlikely until unto up upon us use used useful uses using usually uucp v value various very via viz vs w want wants was wasn't way we week we'd we'll we're we've welcome well went were weren't what what's whatever when whence whenever where where's whereafter whereas whereby wherein whereupon wherever whether which while whither who who's whoever whole whom whose why will willing wish with within without won't wonder would would wouldn't x y yes yet you you'd you'll you're you've your yours yourself yourselves z".split())
nlp = spacy.load('en', parser=False, ner=False)     #A dictionary for lemmatization. We use the library named "Spacy"

#Declare some variables
errors = []
errors_next = 0
errors_previous = 0
altmetrics = 0
doi = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
crossref_result = []
r = {}
res_array = []
txt = ""


#Declare some functions
def lemmatization(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
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


def CrossrefApi(num, title):

    global r
    r = requests.get('https://api.crossref.org/works?rows=' + str(num) + '&query.title=' + title + '&mailto=pbobyrev11@gmail.com')  # requesting the first 5 results from crossref, most relevant to our title
    global doi
    global crossref_result
    lv_vec = []  # creaing an empty list for the following loop

    if "200" in str(r):
        r = r.json()

        for x in range(num):  # for each result we calculate the Levenshteind ratio between our "xml" title and crossref one to find most similar. Sometimes due to minor unicode changes the title can not be exact the same
            ratio = lv.ratio(str(r['message']['items'][x]['title']), title)
            lv_vec.append((x, ratio))
            crossref_result = sorted(lv_vec, key=lambda x: -x[1])

    else:
        crossref_result = [(0,0)]
        r = "error"
    return crossref_result, r


def AltMetrics(doi, articlerecord):

    global altmetrics
    r = requests.get('https://api.altmetric.com/v1/doi/' + doi)

    #Check whether the response is OK
    if '200' in str(r):
        j = r.json()
        try:
            #Altmetrics has 4 useful metrics - the rating of the article among all indexed articles, the rating of the article among the other articles in this journal
            #and the same rating for +- 3 months articles (because old ones can accumulate rating over time)
            all_metric = j['context']['all']['pct']
            journal_metric = j['context']['journal']['pct']

            all_3m_metric = j['context']['similar_age_3m']['pct']
            journal_3m_metric = j['context']['similar_age_journal_3m']['pct']

            altmetrics = 2*(float(all_3m_metric)+float(journal_3m_metric))+(float(all_metric)+float(journal_metric))
        except:
            altmetrics = 0  #Sometimes Altmetrics doesn't provide "Contex" section, while the response is not empty. Not sure why
    else:
        altmetrics = 0

    articlerecord.append(altmetrics)
    return articlerecord


def FirstLevelTags(articlerecord):

    global txt

    cancerdict = ["tumor", "tumour", "trophoblastic", "triple-negative", "thyroid cancer", "thymoma", "sclc", "sarcoma",
                  "rhabdomyosarcoma", "prostate", "pineoblastoma", "pheochromocytoma", "papillary", "paget's",
                  "osteosarcoma", "oligodendroglioma", "nsclc", "non-small", "non-hodgkin", "neuroblastoma", "net",
                  "myeloma", "myelodysplastic", "metastatic", "metastases", "mesothelioma", "mesenchymous",
                  "meningioma", "melanoma", "medulloblastoma", "liposarcoma", "leukemia", "leiomyosarcoma",
                  "infiltrating", "hodgkin's", "hodgkin", "hnc", "hemangioendothelioma", "glioma", "glioblastoma",
                  "gastrointestinal", "fungoides", "fibrosarcoma", "ewing", "esophageal", "ependymoma",
                  "craniopharyngioma", "colorectal", "chondrosarcoma", "chondrosarcoma", "cholangiocarcinoma",
                  "cervical", "cancer", "breast", "astrocytoma", "angiosarcoma", "adenosarcoma", "adenocarcinoma"]      #Here are some lists of our topic keywords. We use them to help LSI determine the topic of the article
    aizdict = ["aidp ", "aied ", "alps  ", "angiitis ", "antiphospholipid ", "autoimmune", "aps", "ar", "arteritis",
               "buerger's ", "cah", "celiac", "cholangitis", "chronic", "churg-strauss", "cidp ", "cogan's ",
               "cryoglobulinemia ", "cryopathies ", "css", "encephalomyelitis ", "gammopathy ", "gcv ",
               "graft-versus-host", "granulomatosis", "gullain-barre", "gvhd ", "hypersensitivity ", "inflammatory",
               "isaacs'", "kawasaki", "kd ", "lambert-eaton", "lems ", "lymphoproliferative", "lupus", "meniere's",
               "mmn ", "moersch-woltmann ", "ms", "sclerosis", "myasthenia", "neuromyotonia", "oms",
               "opsoclonus-myoclonus", "pan", "paraneoplastic", "pbc", "pernicious", "pnd", "pnd's", "polyarteritis",
               "polyradiculoneuropathy", "psc", "rar", "raynaud's", "rheumatica ", "sarcoidosis ", "tak", "takayasu’s ",
               "thromboangiitis", "vascolitides ", "vasculitis ", "wegener's"]
    infectdict = ["immunodeficiency", "bmd", "chb", "eculizumab", "hbeag", "hbsag", "hbv", "hcc", "hcv", "ifn",
                  "infant", "liver", "rbv", "hiv", "hev", "hiv-1", "hiv-2", "hiv-3", "hiv+", "infection", "virus",
                  "malaria", "hepatitis", "aids", "streptococcus", "antiretroviral", "art", "hiv-associated", "hand",
                  "ebolavirus", "hiv-infected", "hiv-uninfected"]
    eyedict = ["amd", "cataract", "corneal", "eye", "glaucoma", "iol", "iop", "myopia", "poag", "retina", "retinal",
               "retinopathy", "rgcs", "rnfl", "rop", "trachoma", "uveitis", "visual"]
    genedict = ["uremic", "ahus", "allele", "dmd", "dna", "dystrophin", "fviii", "gene", "genotype", "hemophilia",
                "lncrna", "mdx", "mirna", "sma", "smn", "smn2", "snp", "tdf", "hereditary"]
    chemdict = ['bcl', 'bcl2', 'bcl-2', 'b-cell lymphoma', 'b-cell lymphoma 2', 'egfr', 'epidermal growth factor receptor',
                'osimertinib', 't790m', 'c797s', 'cis', 'cytokine-induced stat inhibitor', 'socs', 'stat', 'cish', 'btk',
                'bruton tyrosine kinase', 'ibrutinib', 'obinutuzumab', 'parp', "brca-2", "brca2", 'parp-1', 'poly adp ribose polymerase',
                'olaparib', 'talazoparib', 'parpis', 'poly(adp-ribose) polymerase', 'poly(adp-ribose)', 'parpi', 'taar',
                'trace amine-associated receptor', 'taar-5', 'taar-1', 'taar1', 'taar5', 'trace amine (ta)‐associated',
                'cdk8', 'cdk19', 'cdks', 'cyclin-dependent protein kinases', 'cyclin-dependent protein kinase', 'retinoic-acid-related orphan receptor γt',
                'rorγt', 'ror', 'ror gamma-t', 'ror(gamma)t', 'roryt', 'synthesis', 'compound', 'chemical']

    cancer_idlist, aiz_idlist, infect_idlist, eye_idlist, gene_idlist, chem_idlist = [], [], [], [], [], []
    cancer_multiplier, aiz_multiplier, infect_multiplier, eye_multiplier, gene_multiplier, chem_multiplier = 0, 0, 0, 0, 0, 0

    txt = articlerecord[2].lower()

    words = corpora.Dictionary([txt.split()])
    ids = words.token2id

    # Checking the presence of the target words from our dictionaries in text and adding them to corresponding lists
    for x in ids.keys():
        for elem in cancerdict:
            if x == elem:
                cancer_idlist.append(ids[x])
        for elem in aizdict:
            if x == elem:
                aiz_idlist.append(ids[x])
        for elem in infectdict:
            if x == elem:
                infect_idlist.append(ids[x])
        for elem in eyedict:
            if x == elem:
                eye_idlist.append(ids[x])
        for elem in genedict:
            if x == elem:
                gene_idlist.append(ids[x])
        for elem in chemdict:
            if x == elem:
                chem_idlist.append(ids[x])
    words = [words.doc2bow(text) for text in [txt.split()]]

    # Calculating the amount of target words in the text
    for e in words[0]:
        for i in cancer_idlist:
            if e[0] == i:
                cancer_multiplier += e[1]
        for i in aiz_idlist:
            if e[0] == i:
                aiz_multiplier += e[1]
        for i in infect_idlist:
            if e[0] == i:
                infect_multiplier += e[1]
        for i in eye_idlist:
            if e[0] == i:
                eye_multiplier += e[1]
        for i in gene_idlist:
            if e[0] == i:
                gene_multiplier += e[1]
        for i in chem_idlist:
            if e[0] == i:
                chem_multiplier += e[1]

    # Constructing a list of amounts of target words for each topic
    multipliers = [cancer_multiplier, aiz_multiplier, infect_multiplier, eye_multiplier, gene_multiplier]

    #Now if we have a long abstact we will try to make LSI magic upon it. Else, we will use keywords approach
    #On this step we try to classify our articles by five medical topics + chemical theme. So, using 2 models: 5-in-1 biological one and chemical one
    if len(txt.split()) >= 50:
        txt = [x for x in txt if x not in stoplist]
        txt = lemmatization(str(txt), allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

        vec_bow = dictionary.doc2bow(txt.split())
        vec_bow_chem = dictionary_CUB_chem.doc2bow(txt.split())

        vec_lsi = lsi[vec_bow]      # convert the query to LSI space
        vec_lsi_chem = lsi_CUB_chem[vec_bow_chem]

        sims = index[vec_lsi]       # perform a similarity query against the corpus
        sims_chem = index[vec_lsi_chem]
        comp_keyword_multiplied = [x*(1+0.08*y) for x, y in zip(sims, multipliers)]   # multiplying the Gensim result to the multiplier from previous steps
        sims = list(enumerate(comp_keyword_multiplied))

        # Tagging the text with one of the first-level-tags basing on the treshold
        number, value = max(sims, key=lambda item: item[1])
        if number == 0 and value >= 0.65:  # Pay attentions to the treshold: it is a matter of choice. It is 0.65 now
            articlerecord.append("cancer")
        elif number == 1 and value >= 0.65:
            articlerecord.append("autoimmunity")
        elif number == 2 and value >= 0.65:
            articlerecord.append("infectious")
        elif number == 3 and value >= 0.65:
            articlerecord.append("ophtalmological")
        elif number == 4 and value >= 0.65:
            articlerecord.append("gene")
        else:
            articlerecord.append("uncategorized")

        #calculating the chemical relation
        score_chem = sum(sims_chem)

    #The keywords approach to title
    else:
        txt = articlerecord[1].lower()
        words = corpora.Dictionary([txt.split()])
        ids = words.token2id

        # Checking the presence of the target words from our dictionaries in text and adding them to corresponding lists
        for x in ids.keys():
            for elem in cancerdict:
                if x == elem:
                    cancer_idlist.append(ids[x])
            for elem in aizdict:
                if x == elem:
                    aiz_idlist.append(ids[x])
            for elem in infectdict:
                if x == elem:
                    infect_idlist.append(ids[x])
            for elem in eyedict:
                if x == elem:
                    eye_idlist.append(ids[x])
            for elem in genedict:
                if x == elem:
                    gene_idlist.append(ids[x])
            for elem in chemdict:
                if x == elem:
                    chem_idlist.append(ids[x])
        words = [words.doc2bow(text) for text in [txt.split()]]

        # Calculating the amount of target words in the text
        for e in words[0]:
            for i in cancer_idlist:
                if e[0] == i:
                    cancer_multiplier += e[1]
            for i in aiz_idlist:
                if e[0] == i:
                    aiz_multiplier += e[1]
            for i in infect_idlist:
                if e[0] == i:
                    infect_multiplier += e[1]
            for i in eye_idlist:
                if e[0] == i:
                    eye_multiplier += e[1]
            for i in gene_idlist:
                if e[0] == i:
                    gene_multiplier += e[1]
            for i in chem_idlist:
                if e[0] == i:
                    chem_multiplier += e[1]

        # Constructing a list of amounts of target words for each topic
        multipliers = [cancer_multiplier, aiz_multiplier, infect_multiplier, eye_multiplier, gene_multiplier, chem_multiplier]
        multipliers = list(enumerate(multipliers))
        number, value = max(multipliers, key=lambda item: item[1])

        if number == 0:
            articlerecord.append("cancer")
        elif number == 1:
            articlerecord.append("autoimmunity")
        elif number == 2:
            articlerecord.append("infectious")
        elif number == 3:
            articlerecord.append("ophtalmological")
        elif number == 4:
            articlerecord.append("gene")
        else:
            articlerecord.append("uncategorized")

        score_chem = chem_multiplier

    articlerecord.append(str(score_chem)+' based on title')
    return articlerecord, txt


def FirstLevelSimilarities(articlerecord, txt):

    if len(txt.split()) >= 40:

        if articlerecord[5] == "cancer":
            vec_bow_CUB = dictionary_CUB_onco.doc2bow(txt.split())
            vec_lsi_CUB = lsi_CUB_onco[vec_bow_CUB]
            sims_CUB = index_CUB_onco[vec_lsi_CUB]
        elif articlerecord[5] == "autoimmunity":
            vec_bow_CUB = dictionary_CUB_aiz.doc2bow(txt.split())
            vec_lsi_CUB = lsi_CUB_aiz[vec_bow_CUB]
            sims_CUB = index_CUB_aiz[vec_lsi_CUB]
        elif articlerecord[5] == "infectious":
            vec_bow_CUB = dictionary_CUB_inf.doc2bow(txt.split())
            vec_lsi_CUB = lsi_CUB_inf[vec_bow_CUB]
            sims_CUB = index_CUB_inf[vec_lsi_CUB]
        elif articlerecord[5] == "ophtalmological":
            vec_bow_CUB = dictionary_CUB_eye.doc2bow(txt.spilt())
            vec_lsi_CUB = lsi_CUB_eye[vec_bow_CUB]
            sims_CUB = index_CUB_eye[vec_lsi_CUB]
        elif articlerecord[5] == "gene":
            vec_bow_CUB = dictionary_CUB_gene.doc2bow(txt.split())
            vec_lsi_CUB = lsi_CUB_gene[vec_bow_CUB]
            sims_CUB = index_CUB_gene[vec_lsi_CUB]
        else:
            sims_CUB = [0,0,0]


        score = sum(sims_CUB)   #we sum the similarities to all the topics, because all our topics is about our disease

        articlerecord.append(score)
    else:
        articlerecord.append("too short for similarities")

    return articlerecord


def Parser(rsslinks):
    global errors
    global errors_previous
    global errors_next
    global doi
    global res_array

    counter = 0
    errors = []
    for i in rsslinks:
        try:
            feed = feedparser.parse(i[1])

            if len(feed.entries) == 0:
                errors.append(i)
                print("empty xml, will retry to parse them separately")

            for item in range(len(feed.entries)):
                text = feed.entries[item].description
                title = feed.entries[item].title
                articlerecord = []          #a list looking like [journal, title, abstract, doi, altmetrics, topic, chemscore, score]

                articlerecord.append(i[0])      #JOURNAL added
                articlerecord.append(title)     #TITLE added

                if text != '':
                    text = re.sub(r'doi:.*?<', '<', text)
                    text = ' '.join(BeautifulSoup(text, "lxml").findAll(text=True))
                    text = re.sub(r'\n+', ' ', text)

                    articlerecord.append(text)  #ABSTRACT added
                    #Here we can write the abstracts to text file, if we want

                else:
                    articlerecord.append("no abstract")

                textfordoi = feed.entries[item]                 #parse all the text of an xml entry to find doi using regular expressions
                doi_result = re.search(doi, str(textfordoi))    #searching the doi pattern

                if doi_result == None:                          #if cannot find doi in xml trying to acess it using crossref api and article's title

                    CrossrefApi(3, title)                       #start from top 3 results from Crossref

                    if crossref_result[0][1] >= 0.85:           #checking whether the first result is good enough. If does, pull the doi from crossref result
                        doi = r['message']['items'][crossref_result[0][0]]['DOI']

                    elif r == "error":
                        doi = "not found"

                    else:
                        CrossrefApi(10, title)                  #if the relevant title cannot be found in the first 3 rows of crossref results - trying to achieve it from top 10 rows

                        if crossref_result[0][1] >= 0.85:
                            doi = r['message']['items'][crossref_result[0][0]]['DOI']

                        else:
                            doi = "not found"

                    sleep(2)  # sleep for 2 seconds because of crossref policies

                else:
                    doi = doi_result.group(1)

                articlerecord.append(doi)       #DOI added (It will be cool to split the Parser function to the smaller ones, each of whom will append its return to the articlerecord list. I've made it for subsequent parameters)

                AltMetrics(doi, articlerecord)  #ALTMETRICS added

                FirstLevelTags(articlerecord)   #TOPIC added

                FirstLevelSimilarities(articlerecord, txt)    #SCORE added

                res_array.append(articlerecord)             #Finally adding a 8-valued vector of a single article to the resulting array

        except Exception as E:
            print(E)
            continue

        counter += 1
        print("I've asked ", counter, " of ", len(rsslinks), " sources")

    errors_previous = len(errors)
    return errors_previous, res_array

Parser(rss)

print("errors previous = ", errors_previous, "; errors next = ", errors_next)
a = np.array(res_array)

np.save("C:/Users/pboby/Desktop/res_array.npy", res_array)

b = np.load("C:/Users/pboby/Desktop/res_array.npy")
print(b)


'''while errors_previous > errors_next:
    print("An error loop has started")
    sleep(20)
    errors_next = errors_previous
    Parser(errors)
    print(errors)'''



