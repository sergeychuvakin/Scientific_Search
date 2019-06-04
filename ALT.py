def altmetrics(doi):
    '''function returns JSON by doi'''
    #doi = '10.1021/jacs.9b02936' 
    url = 'https://api.altmetric.com/v1/doi/{}'.format(doi)
    page = requests.get(url)#, verify=False)
    print(page.status_code)
    p = page.json()
    return p