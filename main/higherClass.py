import time 
class NER:
    def __init__(self, texts): 
        self.t = texts
        self.os = __import__('os')
        sr = SemanticRepresentation('run_MM')
        sr.startMM()
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
                a = a.append(p)
                b = b.append(e)
            else:
                print('ERROR: invalid file path ---  ', i)
        return a, b
