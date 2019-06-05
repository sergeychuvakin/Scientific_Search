import feedparser
import jellyfish
import time
import copy
import requests

def findJournal(title):

    '''
    Function requires time, copy, jellyfish, requests modules. By given title, function returns DOI. 
    Func uses Crossref API. Func returns the nearest doi by title (it counts levenshtein_distance)'''
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
    return  res.json()['message']['items'][n]['container-title'][0]