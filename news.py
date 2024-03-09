from newspaper import Article
import nltk
nltk.download('punkt')

url = 'https://www.moneycontrol.com/news/trends/chinese-passenger-throws-coins-into-aircraft-engine-delays-flight-by-4-hours-12428321.html'
article = Article(url)

article.download()
article.parse()
article.nlp()

print(article.keywords)
print(article.summary)