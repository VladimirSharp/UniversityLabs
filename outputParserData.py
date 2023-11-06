from wordcloud import WordCloud
import matplotlib.pyplot as plt


def cloud(words):
    text_raw = " ".join(words)
    wordcloud = WordCloud().generate(text_raw)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
