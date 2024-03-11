from serpapi import GoogleSearch
from newspaper import Article
import nltk
nltk.download('punkt')

params = {
  "api_key": "",
  "engine": "google",
  "q": "yee",
  "location": "Maharashtra, India",
  "google_domain": "google.com",
  "gl": "us",
  "hl": "en",
  "tbm": "nws",
  "start": "0",
  "num": "20"
}

def serp(q):
    
  params['q'] = q

  search = GoogleSearch(params)
  results = search.get_dict()
  links = [result['link'] for result in results.get('news_results', [])]

  # Printing the links
  # for link in links:
  #     print(link)

  from newspaper import Article
  import nltk
  nltk.download('punkt')

  articles = []
  condense=""

  for link in links:
      try:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        condense += article.summary + "\n"
      except:
        pass
  return condense    
      
  
