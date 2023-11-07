
from outputParserData import cloud
from parserHabrArticle import *
from parserHarbSearchPages import getShortInfoAboutHarbArticles


articles = getShortInfoAboutHarbArticles(countOfPageNeedParse=1)
articles = [parseArticle_GetArticleContent(info.link) for info in articles]

concatedArticlesText = ' '.join([text.contentBody for text in articles])

names = parseArticle_GetKeyPerson(concatedArticlesText).keys()
keywords = parseArticle_GetKeyWords(concatedArticlesText, 20)

print('Ключевые персонажи:')
print(', '.join(names))

print('\nКлючение слова:')
[print('Слово: \"' + keyword[0] + '\", было использованно: '+ str(keyword[1]) + ' раз') for keyword in keywords]

cloud([keyword[0] for keyword in keywords])