import requests 
from bs4 import BeautifulSoup
import re
  

url = ""

# Making a GET request 
r = requests.get(url) 
  
soup = BeautifulSoup(r.content, 'html.parser')

pageTitle = soup.title.text.strip()
dragonNickname = soup.find('div', class_='dragonNickname').text.strip()
dragonBreed = soup.find('div', class_='dragonBreedName').text.strip()
username = soup.find('div', class_='nickText').text.strip()
viewCount = soup.find('div', class_='viewText').text.strip()
imageRes = re.sub('\.png', '', re.sub('https://res\.dvc\.land/dvc-web/res/dragon/.../', '', soup.find("meta", property="og:image")["content"].strip()))

dragonInfo = imageRes.split("_")
dragonForm = dragonInfo[1]
dragonGender = dragonInfo[2]
dragonGrowth = dragonInfo[3]
dragonColor = dragonInfo[4]

