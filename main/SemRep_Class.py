import os
import textract
from bs4 import BeautifulSoup
import pandas as pd
import time
class SemanticRepresentation: 
    '''class aims to parse text for NER purposes. It returns Predications, 
    Entities and etities from findRelations method
    ---------------
    args: 
    path - path to file
    ---------------
    prerequisites: 
    1) installed and run MetaMap (it can be run by startMM() method)
    2) installed SemRep (check all pathes)
    3) check libpcre.so.1 to be on your computer, don't forget pathes
    ---------------
    Notes: 
    1) if your pass pdf file, run pdf() first
    2) after all actions don't forget to stopMM()
    3) MM  starts apprximately 1 min.
    '''
    def __init__(self, path): 
        self.file = os.path.splitext(path)[0]
        self.path = path
        #self.output = self.file+'.xml'
        #self.output = '/home/BIOCAD/chuvakin/serge/science_search/outtext.xml'
        path, name = os.path.split(path)
        self.output = path + '/' + os.path.splitext(name.replace(' ', ''))[0] + '.xml' # убираем в имени файла пробелы и формируем аутпут
        self.newname = path + '/'+ os.path.splitext(name.replace(' ', ''))[0] + '.txt' # новое имя, чтобы переименовать 
    def startMM(self):
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/skrmedpostctl start')
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/wsdserverctl start')
        time.sleep(30)
    def stopMM(self):
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/skrmedpostctl stop')
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/wsdserverctl stop')
    def semrep(self, inputT=None, output=None):
        if inputT == None:
            inputT = self.path 
        if output == None:
            output = self.output
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_semrep/bin/semrep.v1.8 -X -L 2018 {x} {y}'.format(x=inputT, y=output)) 
    def check(self): 
        os.system('ln -svf /usr/local/chuvakin/pcre-8.42/lib/libpcre.so.1 libpcre.so.1')
    def run(self): 
        self.check()
        #self.startMM()
        self.path = self.aux(self.path)
    def pdf(self): 
        with open(self.file+'.txt', 'w') as f: 
            f.write(textract.process(self.path).decode('utf-8'))
        self.path = self.file+'.txt'
    def findRelations(self):
        self.run()
        self.semrep()
        with open(self.output, 'r') as f:
            t = f.read()
    
        soup = BeautifulSoup(t, 'lxml')
        semtypes = [i['semtypes']for i in soup.find_all('entity')]
        _id = [i['id']for i in soup.find_all('entity')]
        name = [i.get('name') for i in soup.find_all('entity')]
        text = [i['text']for i in soup.find_all('entity')]
        begin = [i['begin']for i in soup.find_all('entity')]
        end = [i['end']for i in soup.find_all('entity')]
        Entities = pd.DataFrame({'Sem':semtypes, 'id':_id,'name':name, 'text':text, 'begin':begin, 'end':end })
        rule = dict(zip(Entities['id'], Entities['name']))
        subject_id = [i.find('subject')['entityid'] for i in soup.find_all('predication')]
        object_id = [i.find('object')['entityid'] for i in soup.find_all('predication')]
        rel  = [i.find('predicate')['type'] for i in soup.find_all('predication')]
        Predications = pd.DataFrame({'subject':subject_id, 'object':object_id, 'relation':rel})
        Predications = Predications.replace(rule)
        #self.stopMM()
        #self.stop()
        return Predications, Entities
        
    def aux(self,name):
        '''rename path - remove white spaces'''
        os.rename(name, self.newname)
        return self.newname
    def stop(self):
        os.remove(self.output)
        os.remove(self.newname)
