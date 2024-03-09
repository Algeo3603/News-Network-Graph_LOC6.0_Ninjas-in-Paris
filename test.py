import requests
import os
from dotenv import load_dotenv
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

GEMINI_API = os.getenv('GEMINI_API')
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro')


load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news_articles(keywords, financial_domains="financial-websites.com",language="en"):
  """
  Fetches news articles related to the provided keywords and saves descriptions to text files.

  Args:
    keywords: User-entered keywords or phrases related to the financial event.
    financial_domains (optional): Comma-separated list of financial website domains (default: financial-websites.com).
  """
  # Replace with your actual News API key
  api_key = NEWS_API_KEY
  base_url = "https://newsapi.org/v2/everything"

  # Construct the URL with user-entered keywords
  url = f"{base_url}?apiKey={api_key}&q={keywords}&sortBy=publishedAt&domain={financial_domains}&language={language}"

  # Make the API request
  response = requests.get(url)
  response.raise_for_status()  # Raise an error if API request fails

  # Parse the JSON response
  data = response.json()

  # Iterate through articles and save descriptions to text files
  k=1
  corpus = ""
  for article in data["articles"]:

    k=k+1
    title = str(article["title"])
    description = str(article["description"])
    corpus += title
    corpus += description

    # Create a unique filename to avoid overwrites
    filename = f"{k}.txt"

    # Save the description to a text file
    # with open(filename, "w", encoding="utf-8") as outfile:
    #   outfile.write(title)
    #   outfile.write("\n")
    #   outfile.write(description)
    if (k % 10 == 0):
      # print(corpus)
      response = model.generate_content(f"only display the names of top 5 most relevant entities and the label of their sentiment in the form of a list format [entity, sentiment] from the following news articles that relate to the effects of {keywords}. {corpus}")
      print(response)
      corpus = ""

  print(f"Successfully saved descriptions for {len(data['articles'])} articles.")


def see_url(keywords, financial_domains="financial-websites.com"):
  """
  Fetches news articles related to the provided keywords and saves descriptions to text files.

  Args:
    keywords: User-entered keywords or phrases related to the financial event.
    financial_domains (optional): Comma-separated list of financial website domains (default: financial-websites.com).
  """
  # Replace with your actual News API key
  api_key = "d19f7ff3b47f412e877621a4c5aee083"
  base_url = "https://newsapi.org/v2/everything"

  # Construct the URL with user-entered keywords
  url = f"{base_url}?apiKey={api_key}&q={keywords}&sortBy=publishedAt&domain={financial_domains}"
  print(url)

def delete_text_files():
  """
  Deletes all text files (*.txt) within a specified directory.

  Args:
    directory: The path to the directory containing the text files.
  """
  for filename in os.listdir(r"C:\Users\Adit\Desktop\news"):
    if filename.endswith(".txt"):
    #   file_path = os.path.join(directory, filename)
      os.remove(filename)


if __name__ == "__main__":
  # Get user input for keywords
  keywords = input("Enter keywords related to the financial event: ")

  # Call the function to fetch and save articles
  get_news_articles(keywords)
#   see_url(keywords)
#   delete_text_files()
