from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)


import nltk
from nltk.probability import FreqDist
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
from common import *
import nltk

def remove_words_from_text(text, words):
    querywords = text.replace('«', '').replace('»', '').split()
    return ' '.join([word for word in querywords if word.lower() not in words])

def parseArticle_GetArticleContent(link):
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    response = requests.get(link, headers)
    bs = BeautifulSoup(response.text, "html.parser")
    content = bs.find('article', {'class': 'tm-article-presenter__content tm-article-presenter__content_narrow'})
    tags = [obj.get_text() for obj in content.findAll('a', {'class': 'tm-publication-hub__link'})]  
    header = content.find('h1', {'class': 'tm-title tm-title_h1'}).get_text()
    contentBody = content.find('div', {'id': 'post-content-body'}).get_text()
    return Article(tags = tags, header = header, contentBody = contentBody, link = link)

def parseArticle_GetKeyPerson(text):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)


    doc.tag_ner(ner_tagger)
    # print((doc.spans[0]))
    for span in doc.spans:
        span.normalize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)
    
    return {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}

def parseArticle_GetKeyWords(unpreparedText, countMostPopular = 10):
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(['—', 'это', 'которые'])
    unpreparedText = remove_punctuation(unpreparedText)
    unpreparedText = remove_words_from_text(unpreparedText, russian_stopwords)
    text_tokens = word_tokenize(unpreparedText)
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)
    return fdist.most_common(countMostPopular)

#article = parseArticle_GetArticleContent('https://habr.com/ru/companies/skillbox/articles/729854/')

#print(article.header)
#print(article.tags)
#print(parseArticle_GetKeyPerson(article.contentBody).keys())
#print(parseArticle_GetKeyWords(article.contentBody))
