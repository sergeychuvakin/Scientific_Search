from bs4 import BeautifulSoup
import re
import time 
import requests
import os
import textract


# doi 
doi = '10.1021/jacs.9b02266'

time.sleep(3)
#найти ссылку на скачивание и сохранить ее в h 
r = requests.get("https://sci-hub.se/{}".format(doi))
soup = BeautifulSoup(r.text, 'html.parser')

for i in soup.find_all('a'): 
    if 'сохранить' in str(i):
        h = i.get('onclick')

# обрабатываем ссылку, на случай некорректных имен
g = re.findall(r'href=(.*)', h)
s = re.sub(r"'", '', g[0])
s = ''.join(re.findall(r'(sci-hub.se)(.*)', s)[0])
s = 'https://'+ s

time.sleep(2)
# сохраняем в файл
res = requests.get(s)
with open('testtest2.pdf', 'wb') as f: 
    f.write(res.content)



file_name = 'testtest2.pdf'
t = textract.process(file_name).decode('utf-8')
#os.remove(file_name)
