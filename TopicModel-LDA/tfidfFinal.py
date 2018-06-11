# coding: UTF-8
import gensim
from gensim.summarization import keywords
from gensim import corpora, models, similarities
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
from bs4 import BeautifulSoup
import pprint

#辞書作成
dictionary = gensim.corpora.Dictionary.load_from_text('dict.txt')

#コーパス作成
corpus = corpora.MmCorpus('cop.mm')

#LDA
estimatedTopics = 10
ldaModel = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=estimatedTopics, id2word=dictionary)
for i in range(estimatedTopics):
    print('トピック:', i, '__', ldaModel.print_topic(i))
