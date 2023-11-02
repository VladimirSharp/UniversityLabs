from bs4 import BeautifulSoup
import requests

def linkBuilder(partUrlToArticles):
    return globalHabrLink + partUrlToArticles

globalHabrLink = "https://habr.com"
searchText = "Методы миграции с монолитных приложений на микросервисы"
headers = {'Content-Type': 'text/html; charset=utf-8'}

for i in range(3):
    habrUrlForSearchArticles = f"https://habr.com/ru/search/page{i+1}/?q={searchText}&target_type=posts&order=relevance"
    print(habrUrlForSearchArticles)

    response = requests.get(habrUrlForSearchArticles, headers)
    bs = BeautifulSoup(response.text, "html.parser")
    nameList = bs.findAll('h2', {'class': 'tm-title tm-title_h2'})

    with open('output.txt', 'w' if i == 0 else 'a', encoding='utf-8') as file:
        for name in nameList:
            link = name.find('a').attrs['href']
            file.write("Заголовок: " + name.get_text() + ". Ссылка: " + linkBuilder(link) + '\n')

with open('output.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        print(line)



# <h2 class="tm-title tm-title_h2">
#     <a href="/ru/companies/skillbox/articles/729854/" class="tm-title__link" data-test-id="article-snippet-title-link" data-article-link="true">
#         <span>���������� ������������ �������������. �������� ����� �� ������� �����</span>
#     </a>
# </h2>