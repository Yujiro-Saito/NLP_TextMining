# coding: UTF-8
import gensim
from gensim.summarization import keywords
from gensim import corpora, models, similarities
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
from bs4 import BeautifulSoup
import pprint

#記事読み込み
target_url = "http://news.livedoor.com/article/detail/14825952/"
r = requests.get(target_url)   
soup = BeautifulSoup(r.text, 'lxml')
texts = []
#記事の文章を取得
for p in soup.find_all('p'):
    texts.append(p.string)

#取得したpタグの文字列の中でNone型を取り除く
filterdArray = []
for text in texts:
    if text != None:
        filterdArray.append(text)

#リストから文字列に変換
filterdSentence = ''.join(filterdArray)

#文字列からリストに変換
filteredText = filterdSentence.split("。")
filteredText.remove('')

#形態素解析準備
from janome.tokenizer import Tokenizer
t = Tokenizer()
words = []

#ストップワード読み込み+統合
import codecs
file = codecs.open('stopwords.txt', 'r', 'utf-8')
lines = file.read()
stopwords = lines.split("\n")
stoplist = ['ため','ごと','とおり','それ','これ','これら',"ころ",'よう','こと','もの','の','さまざま','ほか','ん',
            '高','費', '.', '℃',"われわれ",'百','千','万','億','円','等','用','月','日','年','その他','化','比','力',"自分",'的','当社','所','後','前',"1","2","3","4","5","6","7","8","9"]

for sw in stoplist:
    stopwords.append(sw)




#名詞の場合+ストップワード以外の場合リストに追加
for i, line in enumerate(filteredText):
    word_vector = []
    tokens = t.tokenize(line)

    for token in tokens:
        if token.part_of_speech[:2] == "名詞":
            word_vector += [token.base_form]

    fixedList = [w for w in word_vector if not w in stopwords]
    
    words += [fixedList]


#辞書作成
dictionary = corpora.Dictionary(words)
#コーパス作成
corpus = [dictionary.doc2bow(text) for text in words]

#LDA
estimatedTopics = 4
ldaModel = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=estimatedTopics, id2word=dictionary)

for i in range(estimatedTopics):
    print('トピック:', i, '__', ldaModel.print_topic(i))






#LDAニュース記事増やす

#Keywords Extraction
#TF-IDF
#============>20 news data at least

#Similarity--=>

#Text classification

#Recommended
