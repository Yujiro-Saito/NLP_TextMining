# coding: UTF-8
import gensim
from gensim.summarization import keywords
from gensim import corpora, models, similarities
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
from bs4 import BeautifulSoup
import pprint

#読み込む記事
target_url = ["http://news.livedoor.com/article/detail/14831948/","http://news.livedoor.com/article/detail/14834387/","http://news.livedoor.com/article/detail/14835786/","http://news.livedoor.com/article/detail/14835890/","http://news.livedoor.com/article/detail/14838960/","http://news.livedoor.com/article/detail/14838961/","http://news.livedoor.com/article/detail/14838967/","http://news.livedoor.com/article/detail/14838738/","http://news.livedoor.com/article/detail/14839135/","http://news.livedoor.com/article/detail/14839195/","http://news.livedoor.com/article/detail/14839229/","http://news.livedoor.com/article/detail/14819625/","http://news.livedoor.com/article/detail/14836952/","http://news.livedoor.com/article/detail/14828284/","http://news.livedoor.com/article/detail/14827796/","http://news.livedoor.com/article/detail/14822616/","http://news.livedoor.com/article/detail/14778172/","http://news.livedoor.com/article/detail/14759605/"]

#記事読み込み
texts = []
#各URL
for url in target_url:
    #テキスト取得
    r = requests.get(url)   
    soup = BeautifulSoup(r.text, 'lxml')
    
    sentBox = []
    sentPart = []
    #テキストの中のpタグの繰り返し処理
    for p in soup.find_all('p'):
        #Noneを除外
        if p.string != None:
            sentBox.append(p.string)
    #リストを文字列に変換
    sentPart = "".join(sentBox)
    texts.append(sentPart)

#形態素解析準備
from janome.tokenizer import Tokenizer
t = Tokenizer()
words = []

#ストップワード読み込み
import codecs
file = codecs.open('stopwords.txt', 'r', 'utf-8')
lines = file.read()
stopwords = lines.split("\n")
stoplist = ['ため','ごと','とおり','それ','これ','これら',"ころ",'よう','こと','もの','の','さまざま','ほか','ん',
            '高','費',"つもり", '.', '℃',"われわれ",'百','千','万','億','円','等','用','月','日','年','その他','化','比','力',"自分",'的','当社','所','後','前',"1","2","3","4","5","6","7","8","9",","]
#ストップワードの統合
for sw in stoplist:
    stopwords.append(sw)

#名詞の場合+ストップワード以外の場合リストに追加
for i, line in enumerate(texts):
    word_vector = []
    tokens = t.tokenize(line)

    for token in tokens:
        if token.part_of_speech[:2] == "名詞":
            word_vector += [token.base_form]

    fixedList = [w for w in word_vector if not w in stopwords]
    
    words += [fixedList]


#辞書作成
dictionary = corpora.Dictionary(words)
dictionary.filter_extremes(no_below=2, no_above=0.5)
#コーパス作成
corpus = [dictionary.doc2bow(text) for text in words]

#LDA
estimatedTopics = 10
ldaModel = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=estimatedTopics, id2word=dictionary)
for i in range(estimatedTopics):
    print('トピック:', i, '__', ldaModel.print_topic(i))
