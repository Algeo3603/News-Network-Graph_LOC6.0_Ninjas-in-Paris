import requests
import os
# from dotenv import load_dotenv
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import pandas as pd
import spacy
from spacy import displacy
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


GEMINI_API = ""
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro')


# load_dotenv()
NEWS_API_KEY = ""

def get_news_articles(keywords, financial_domains="financial-websites.com",language="en"):
  """
  Fetches news articles related to the provided keywords and saves descriptions to text files.

  Args:
    keywords: User-entered keywords or phrases related to the financial event.
    financial_domains (optional): Comma-separated list of financial website domains (default: financial-websites.com).
  """
  jsondata = {
      'source': [],
      'destination': [],
      'sentiment': []
  }

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
      response = model.generate_content(f"strictly only display the names of upto 10 entities such as company names/organizations etc and the label of their sentiment(either positive negative or neutral) in this format: entity, sentiment from the following news articles.  {corpus},i want it strictly in the above mentioned format, do not change it under any circumstance ,if you dont find any entity dont display a message saying the same , just send nothing back and move on to the next prompt")
      # response.resolve()
      # print(response.text)
      try:
        res = response.text.split("\n")
      except:
        pass
      # print(sus)
      for r in res:
        try:
          aspect, senti = r.split(", ")
          if aspect[0] == '-':
            aspect = aspect[1:]
          if '1' <= aspect[0] <= '5':
            aspect = aspect[3:]
          # print(aspect, senti)
          aspect.lstrip().rstrip()
          if aspect not in jsondata['destination']:
            jsondata['source'].append(keywords)
            jsondata['destination'].append(aspect)
            jsondata['sentiment'].append(senti)
        except:
          pass
      corpus = ""

  # print(f"Successfully saved descriptions for {len(data['articles'])} articles.")
  # return jsondata
  data=jsondata
  df = pd.DataFrame(data)
  net = Network(notebook=True)

  for index, row in df.iterrows():
    # Determine node color based on sentiment
    if row['sentiment'] == 'positive':
        node_color = '#00ff00'  # Green for positive sentiment
    elif row['sentiment'] == 'negative':
        node_color = '#ff0000'  # Red for negative sentiment
    else:
        node_color = '#0000ff'  # Blue for neutral sentiment
    
    net.add_node(row['source'], label=row['source'], color='#ffcc00')  # Roadster Release node
    net.add_node(row['destination'], label=row['destination'], color=node_color)  # Company nodes
    net.add_edge(row['source'], row['destination'], value=20)  # Connecting edge with value attribute


    # net.force_atlas_2based()
   
  net.show('graph.html')


def see_url(keywords, financial_domains="finance"):
  """
  Fetches news articles related to the provided keywords and saves descriptions to text files.

  Args:
    keywords: User-entered keywords or phrases related to the financial event.
    financial_domains (optional): Comma-separated list of financial website domains (default: financial-websites.com).
  """
  # Replace with your actual News API key
  api_key = "dcfc10e5cbf140f3ac15cd0c2a5bc047"
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


def get_news_articles2(keywords):
  import appy as ap
  jsondata = {
      'source': [],
      'destination': [],
      'sentiment': []
  }
  text=ap.serp(keywords)
  response = model.generate_content(f"strictly only display the names of upto 10 entities such as company names/organizations etc and the label of their sentiment(either positive negative or neutral) in this format: entity, sentiment from the following news articles.  {text},i want it strictly in the above mentioned format, do not change it under any circumstance ,if you dont find any entity dont display a message saying the same , just send nothing back and move on to the next prompt")
  # print(response.text)
  try:
    res = response.text.split("\n")
  except:
    pass
  # print(sus)
  for r in res:
    try:
      aspect, senti = r.split(", ")
      if aspect[0] == '-':
        aspect = aspect[1:]
      if '1' <= aspect[0] <= '5':
        aspect = aspect[3:]
      # print(aspect, senti)
      aspect.lstrip().rstrip()
      if aspect not in jsondata['destination']:
        jsondata['source'].append(keywords)
        jsondata['destination'].append(aspect)
        jsondata['sentiment'].append(senti)
    except:
      pass

  data=jsondata
  df = pd.DataFrame(data)
  net = Network(notebook=True)

  for index, row in df.iterrows():
    # Determine node color based on sentiment
    if row['sentiment'] == 'positive':
        node_color = '#00ff00'  # Green for positive sentiment
    elif row['sentiment'] == 'negative':
        node_color = '#ff0000'  # Red for negative sentiment
    else:
        node_color = '#0000ff'  # Blue for neutral sentiment
    
    net.add_node(row['source'], label=row['source'], color='#ffcc00')  # Roadster Release node
    net.add_node(row['destination'], label=row['destination'], color=node_color)  # Company nodes
    net.add_edge(row['source'], row['destination'], value=20)  # Connecting edge with value attribute


    # net.force_atlas_2based()
    net.show('graph.html')  












if __name__ == "__main__":
  # Get user input for keywords
  keywords = input("Enter keywords related to the financial event : ")

  # Call the function to fetch and save articles

  get_news_articles2(keywords)


# Add nodes and edges to the network graph
# for index, row in df.iterrows():
#     # Determine node color based on sentiment
#     if row['sentiment'] == 'positive':
#         node_color = '#00ff00'  # Green for positive sentiment
#     elif row['sentiment'] == 'negative':
#         node_color = '#ff0000'  # Red for negative sentiment
#     else:
#         node_color = '#0000ff'  # Blue for neutral sentiment
    
#     net.add_node(row['source'], label=row['source'], color='#ffcc00')  # Roadster Release node
#     net.add_node(row['destination'], label=row['destination'], color=node_color)  # Company nodes
#     net.add_edge(row['source'], row['destination'], value=20)  # Connecting edge with value attribute

# # Set the layout and save the graph
# net.force_atlas_2based()
# net.show(f'{keywords.replace(" ", "_")}.html')
#   see_url(keywords)
#   delete_text_files()
