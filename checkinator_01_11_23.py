from bs4 import BeautifulSoup
import requests
import nltk

globalHabrLink = 'https://gist.githubusercontent.com/nzhukov/b66c831ea88b4e5c4a044c952fb3e1ae/raw/7935e52297e2e85933e41d1fd16ed529f1e689f5/A%2520Brief%2520History%2520of%2520the%2520Web.txt'
headers = {'Content-Type': 'text/html; charset=utf-8'}
name_tag_group_map = {
    #Существительное
    "Nouns": ['NN', 'NNP', 'NNPS', 'NNS'],
    #Прилагательное
    "Adjectives": ['JJ', 'JJR', 'JJS'],
    #Глаголы
    "Verbs": ['VB','VBP', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    #Наречия
    "Adverbs": ["RBR", "RBS"],
    #Междометия
    "Interjections": ['IN'],
    #Предлоги
    "Prepositions": ["PRP", "PRPS"],
}

russian_name_tag = {
    "Nouns": 'существительных',
    "Adjectives": 'прилагательный',
    "Verbs": 'глаголов',
    "Adverbs": 'наречий',
    "Interjections": 'междометий',
    "Prepositions": 'предлогов',
}

response = requests.get(globalHabrLink, headers)
bs = BeautifulSoup(response.text, "html.parser")
text = bs.get_text()

tokens = nltk.word_tokenize(text)
pos_lst = nltk.pos_tag(tokens)

resultDict = {}

for el in pos_lst:
  for key in name_tag_group_map.keys():
    if el[1] in name_tag_group_map[key]:
      if resultDict.get(key):
        resultDict[key] += 1
      else:
        resultDict[key] = 1

sorted_dict = sorted(list(resultDict.items())[:5], key=lambda x: x[1], reverse=True)

for part_of_language in sorted_dict:
  print('Количество ' + russian_name_tag[part_of_language[0]] + ' в тексте: ' + str(part_of_language[1]))