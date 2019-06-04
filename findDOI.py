import feedparser
import jellyfish
import time
import copy
# https://stackoverflow.com/questions/44234221/download-pubmed-papers-based-on-doi-from-sci-hub-api-in-python3-5
def findDOI(title):

    '''
    Function requires time, copy, jellyfish, requests modules. By given title, function returns DOI. 
    '''
    time.sleep(3)
    params = { 
        'rows':'7',
        'query.title': title
            }
    res = requests.get('https://api.crossref.org/works', params = params)
    aux = []
    for i in dict(res.json())['message']['items']:
        aux.append(jellyfish.levenshtein_distance(title, i['title'][0]))
    n = aux.index(min(aux))
    return  res.json()['message']['items'][n]['DOI']