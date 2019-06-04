# https://dev.elsevier.com/apikey/manage

# https://dev.elsevier.com/documentation/PlumXMetricsAPI.wadl


import requests


s = requests.Session()
params = { "apiKey": "9ca2eae595d88de18cad70d487773021",
        'idType': 'doi',
        'idValue': '10.1021/jacs.9b02936'
        }
first = s.get('http://api.elsevier.com/content/search/scopus?query=heart&apiKey=9ca2eae595d88de18cad70d487773021') # просто пробный запрос
r = s.get('https://api.elsevier.com/analytics/plumx/', params = params, headers=h)
r.status_code #401 
s.close()


proxies = {
 'http': 'http://197.159.16.2',
 'https': 'http://197.159.16.2'
}
s = requests.Session()
hh = {'X-ELS-APIKey':'cbe4c351033ad56d82e8c0e0009176aa'}
r = s.get('http://api.elsevier.com/authenticate?', headers=hh)
print(r.status_code) #403
s.close()
