# coding: UTF-8
from gensim.summarization import keywords
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
from bs4 import BeautifulSoup

target_url = "http://news.livedoor.com/article/detail/14828284/"

r = requests.get(target_url)   
soup = BeautifulSoup(r.text, 'lxml')
print("##"*40)
texts = []
#Make List
for p in soup.find_all('p'):
    texts.append(p.string)

#Remove None
removeWord = ["None"]
filterdArray = []

for text in texts:
    if text != None:
        filterdArray.append(text)

#List to String Clear Text
filterdSentence = ''.join(filterdArray)
print(filterdSentence)




