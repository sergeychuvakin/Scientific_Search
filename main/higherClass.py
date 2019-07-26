import time 
class NER:
    '''
    class designed to process several texts using SemanticRepresentation class.
    It's supposed to run MM inside current object
    '''
    def __init__(self, texts): 
        self.t = texts
        self.os = __import__('os')
        sr = SemanticRepresentation('run_MM')
        #sr.startMM()
        time.sleep(30)
    def multipleTexts(self):
        a = pd.DataFrame({'subject':[], 'object':[], 'relation':[], 'utterance':[]})
        b = pd.DataFrame({'Sem':[], 'id':[],'name':[], 'text':[], 'begin':[], 'end':[] })
        for i in self.t:
            if self.os.path.isfile(i)==True:
                sr = SemanticRepresentation(i)
                if self.os.path.splitext(i)[1]=='.pdf':
                    sr.pdf()
                p, e = sr.findRelations()
                a = a.append(p, ignore_index=True)
                b = b.append(e, ignore_index=True)
            else:
                print('ERROR: invalid file path ---  ', i)
        return a, b
    
artcles = ['Acute Myeloid Leukaemia New Targets.pdf',
           'A natural killer-dendritic cell axis defines checkpoint therapy-responsive tumor microenvironments..pdf',
           'A technology platform to assess multiple cancer agents simultaneously within a patient’s tumor.pdf', 
           'CD103+ Dendritic Cells Producing Interleukin-12 in Anticancer Immunosurveillance(1).pdf']
artcles = ['/home/BIOCAD/chuvakin/serge/science_search/'+i for i in artcles] # list of full pathes of processed articles

ner = NER(artcles)
a, b = ner.multipleTexts()
#TODO:add method multipleTexts to __init__ to run it from instnace initialization
