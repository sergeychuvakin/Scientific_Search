import feedparser
import pandas as pd
class Parser:
    def __init__(self, rss):
        self.rss = rss
        self.ll = []
        
    def Parse_rss_link(self, link):
        '''
        Function returns list of dicts with article_name, journal, doi, summary of current rss link
        '''
        d = feedparser.parse(link[1])
        for i in d['entries']: 
            dd = dict.fromkeys(['article_name'], None)
            dd['article_name'] = i['title']
            try:
                dd['journal'] = i['prism_publicationname']
            except:
                dd['journal'] = ''
            try:
                dd['doi'] = i['prism_doi']
            except:
                dd['doi'] = ''
            try:
                dd['summary'] = i['summary']
            except:
                dd['summary'] = ''
            self.ll.append(dd)
        return self.ll
    
    def main(self):
        for link in self.rss: 
            self.Parse_rss_link(link)
        return pd.DataFrame(self.ll)