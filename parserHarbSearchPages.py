from bs4 import BeautifulSoup
import requests

from common import Article

def linkBuilder(partUrlToArticles,  globalHabrLink = "https://habr.com"):
    return globalHabrLink + partUrlToArticles

def getShortInfoAboutHarbArticles(searchText = "Методы миграции с монолитных приложений на микросервисы", countOfPageNeedParse = 3):
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    formatedNamesList = []

    for i in range(countOfPageNeedParse):
        habrUrlForSearchArticles = f"https://habr.com/ru/search/page{i+1}/?q={searchText}&target_type=posts&order=relevance"
        # print(habrUrlForSearchArticles)

        response = requests.get(habrUrlForSearchArticles, headers)
        bs = BeautifulSoup(response.text, "html.parser")
        nameList = bs.findAll('h2', {'class': 'tm-title tm-title_h2'})

        for name in nameList:
            link = name.find('a').attrs['href']
            formatedNamesList.append(Article(name = name.get_text(), link = linkBuilder(link)))
    
    return formatedNamesList

def task1():
    shortArticlesInfo = getShortInfoAboutHarbArticles()

    with open('output.txt', 'w', encoding='utf-8') as file:
        for info in shortArticlesInfo:
            file.write("Заголовок: " + info.name + ". Ссылка: " + info.link + '\n')

    with open('output.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            print(line)
