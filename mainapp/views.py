from django.shortcuts import render
import pandas as pd
from gensim.models import Word2Vec
import nltk
import numpy as np

data = pd.read_csv('D:\\Python\\4\\synonyms\\mainapp\\synonym.csv')

def index(request):
    soilemder = []
    sozder = []
    texts = np.array(data['text'])
    for i in range(len(texts)):
        soilemder.append(nltk.sent_tokenize(texts[i]))
        sozder.append([nltk.word_tokenize(soilem) for soilem in soilemder[i]])

    word2vec = []
    for i in range(len(texts)):
        word2vec.append(Word2Vec(sozder[i], min_count=1, alpha=10))

    s = []
    synonyms = []
    text = ''
    error = ''
    if request.method == "POST":
        text = str(request.POST['search'])

        for i in range(len(texts)):
            if text in word2vec[i].wv.index_to_key:
                s = word2vec[i].wv.most_similar(text, topn=len(texts[0].split()))

                break

        if s:
            for i in s:
                synonyms.append(i[0])
        else:
            error = 'Сіз іздеген сөздің синонимі табылмады!'
    context = {'synonyms': synonyms, 'error': error, 'text': text}
    return render(request, 'mainapp/index.html', context)

