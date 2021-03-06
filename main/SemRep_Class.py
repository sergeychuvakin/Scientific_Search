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
    4) optional parameters -M -l -g -E
    '''
    def __init__(self, path):
        '''Due to the fact we work with multiple files creating in process, we should name it propely'''
        self.file = os.path.splitext(path)[0]
        self.path = path
        #self.output = self.file+'.xml'
        #self.output = '/home/BIOCAD/chuvakin/serge/science_search/outtext.xml'
        path, name = os.path.split(path)
        #self.output = path + '/' + os.path.splitext(name.replace(' ', ''))[0] + '.xml' # убираем в имени файла пробелы и формируем аутпут
        #self.newname = path + '/'+ os.path.splitext(name.replace(' ', ''))[0] + '.txt' # новое имя, чтобы переименовать
        self.output = path + '/' + os.path.splitext(re.sub(r'[\(\)\s’]', '', name))[0] + '.xml' # убираем в имени файла пробелы (и скобки)  и формируем аутпут
        self.newname = path + '/'+ os.path.splitext(re.sub(r'[\(\)\s’]', '', name))[0] + '.txt' # новое имя, чтобы переименовать 
    def startMM(self):
        '''Start server MetaMap. It takes about 1 minute to start'''
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/skrmedpostctl start')
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/wsdserverctl start')
        time.sleep(30)
    def stopMM(self):
        '''Stop server MetaMap to avoid overloading'''
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/skrmedpostctl stop')
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_mm/bin/wsdserverctl stop')
    def semrep(self, inputT=None, output=None):
        '''Run Semrep itself. Here You can tune parameters'''
        if inputT == None:
            inputT = self.path 
        if output == None:
            output = self.output
        os.system('/home/BIOCAD/chuvakin/serge/science_search/public_semrep/bin/semrep.v1.8 -X -L 2018 -M -l -g -E "{x}" "{y}"'.format(x=inputT, y=output)) 
    def check(self):
        '''Check all pathes'''
        os.system('ln -svf /usr/local/chuvakin/pcre-8.42/lib/libpcre.so.1 libpcre.so.1')
    def run(self):
        '''Prepare file and check pathes'''
        self.check()
        #self.startMM()
        self.path = self.aux(self.path)
    def pdf(self): 
        '''pdf to txt'''
        with open(self.file+'.txt', 'w') as f: 
            f.write(textract.process(self.path).decode('utf-8'))
        self.path = self.file+'.txt'
    def findRelations(self):
        '''Method returns 2 pandas DataFrame.
        First - entities with relations
        Second - all entities in text'''
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
        subject_id = []
        object_id = []
        rel = []
        utter = []
        for i in soup.find_all('utterance'):
            subject_id.extend([ii.find('subject')['entityid'] for ii in i.find_all('predication')])
            object_id.extend([ii.find('object')['entityid'] for ii in i.find_all('predication')])
            rel.extend([ii.find('predicate')['type'] for ii in i.find_all('predication')])
            utter.extend([i.get('text')]*len(i.find_all('predication')))
        Predications = pd.DataFrame({'subject':subject_id, 'object':object_id, 'relation':rel, 'utterance':utter})
        Predications = Predications.replace(rule)
        #self.stopMM()
        #self.stop()
        return Predications, Entities
        
    def aux(self,name):
        '''rename path - remove white spaces and parentheses'''
        os.rename(name, self.newname)
        return self.newname
    def stop(self):
        '''clean enviroment'''
        os.remove(self.output)
        os.remove(self.newname)
        #self.stopMM
        
SR = SemanticRepresentation('/home/BIOCAD/chuvakin/serge/science_search/Acute Myeloid Leukaemia New Targets.pdf') 
SR.pdf() # transfrom pdf 
Predications, Entities = SR.findRelations() # form two tables
SR.stop() # clean eviroment


##TODO: 0. how two deal with list of articles (done in higherClass.py)
#       1. add utterances and documents (+)
#       2. how store all entities and tables, link with neo4j (hold)
