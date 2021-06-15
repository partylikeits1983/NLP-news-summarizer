import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

from urllib.request import Request, urlopen
from transformers import pipeline
from transformers import AutoTokenizer

# specific beautiful soup code for cointelegraph to avoid catpcha
# scrapes all links from site and writes them to txt file
parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen("https://cointelegraph.com")
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

page = soup.find_all('a', href=True)

os.remove("/home/ubuntu/Desktop/links.txt")

for link in page:

    a = link['href']
    print(a)

    with open('/home/ubuntu/Desktop/links.txt', 'a') as the_file:
        the_file.write(a + '\n')

# add cointelegraph.com to beginning of all links - specific for cointelegraph
filepath = "/home/ubuntu/Desktop/links.txt"
with open(filepath) as fp:
    lines = fp.read().splitlines()
with open(filepath, "w") as fp:
    for line in lines:
        print('https://cointelegraph.com' + line, file=fp)


# delete all non new article links in links.txt file
# creates new txt file newslinks
open('/home/ubuntu/Desktop/newslinks.txt','w').writelines(line for line in open('/home/ubuntu/Desktop/links.txt') if 'news' in line)



uniquelines = set(open('/home/ubuntu/Desktop/newslinks.txt').readlines())

open('/home/ubuntu/Desktop/newslinks.txt', 'w').writelines(set(uniquelines))


tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
path = "/home/ubuntu/Desktop/articles/"
links_txt = open("/home/ubuntu/Desktop/newslinks.txt", "r")

for aline in links_txt:
    values = aline.split()

    url = values[0]

    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, "html.parser")

    title = soup.findAll("h1")

    for header in title:
        titletext = str(header.get_text())
        #print(titletext)

    titletext = titletext.strip()

    file = titletext

    file = file.replace("'", "")
    file = file.replace(" ", "")


    containers = soup.findAll("p")

    articlestr = ''
    for body in containers:
        bodytext = str(body.get_text())

        articlestr += bodytext

    #print(articlestr)

    articletxt = open(path + titletext + '.txt', 'w')
    articletxt.write(articlestr)
    articletxt.close()

    path1 = "/home/ubuntu/Desktop/articles/summaries/"

    # start summarization
    summarization = pipeline("summarization")
    summary_text = summarization(articlestr, truncation=True, max_length=1024)[0]['summary_text']

    # start sentiment analysis  - @dev - entire article or summary?
    sentiment_analysis = pipeline("sentiment-analysis")
    result = sentiment_analysis(articlestr, truncation=True, max_length=1024)[0]
    sentiment = "Label:" + " " + str(result['label'])
    sentimentscore = "Confidence Score:" + " " + str(result['score'])

    summarytext = open(path1 + file + "summaries" + '.txt', 'w')
    summarytext.write(summary_text + '\n' + sentiment + '\n' + sentimentscore + '\n' + url)
    summarytext.close()
    print(summary_text)
