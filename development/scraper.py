import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://kudago.com/msk/events/?date=2021-08-05'
response = requests.get(url)
response

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

soup.find_all('div', class_ = 'feed-container')

parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen("https://kudago.com/msk/events/?date=2021-08-05")
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

page = soup.find_all('a', href=True)


os.remove("/home/ubuntu/Desktop/links.txt") 

for link in page:
    
    a = link['href']
    print(a)
    
    with open('/home/ubuntu/Desktop/links.txt', 'a') as the_file:
        the_file.write(a + '\n')
