import requests 
from bs4 import BeautifulSoup
import re

from lib.db import db

# some really scuffed code to get all the data from the wiki. Unoptimized, only run once.

url = "https://dragon-village-collection.fandom.com/wiki/Dragons"
r = requests.get(url) 
soup = BeautifulSoup(r.content, 'html.parser')

allDragons = [a['href'] for a in soup.select('.wikia-gallery-item .lightbox-caption a')]
allDragons = allDragons[:len(allDragons)-9]

# Making a GET request 
perr = requests.get("https://dragon-village-collection.fandom.com/wiki/Personalities") 
persoup = BeautifulSoup(perr.content, 'html.parser')
percatlist = persoup.find_all('table')
for tr in percatlist[0].find_all('tr'):
	if tr.find_all('td'):
		pername = tr.find_all('td')[1].find('a').text.strip()
		req = tr.find_all('td')[2].text.strip() + " " + tr.find_all('td')[3].text.strip()
		db.execute('INSERT OR IGNORE INTO Personalities(personality, tier, requirements) VALUES(?,?,?)', pername, "Basic", req)
for tr in percatlist[1].find_all('tr'):
	if tr.find_all('td'):
		pername = tr.find_all('td')[1].find('a').text.strip()
		req = tr.find_all('td')[2].text.strip()
		db.execute('INSERT OR IGNORE INTO Personalities(personality, tier, requirements) VALUES(?,?,?)', pername, "Special", req)
for tr in percatlist[2].find_all('tr'):
	if tr.find_all('td'):
		pername = tr.find_all('td')[1].find('a').text.strip()
		req = tr.find_all('td')[2].text.strip()
		db.execute('INSERT OR IGNORE INTO Personalities(personality, tier, requirements) VALUES(?,?,?)', pername, "Exclusive", req)


for dragonUrl in allDragons:
	dragonUrl = "https://dragon-village-collection.fandom.com" + dragonUrl
	dragonr = requests.get(dragonUrl)
	dragonSoup = BeautifulSoup(dragonr.content, 'html.parser')
	infoBox = dragonSoup.find(role='region')

	dragonSpecies = infoBox.find(attrs={"data-source": "title"}).text.strip()
	eggText = infoBox.find('h2', class_="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background").text.strip()
	whereBox = infoBox.find(attrs={"data-source": "whereFound"})
	whereFound = whereBox.find('div', class_="pi-data-value pi-font").text.strip()

	if infoBox.find(attrs={"data-source": "exploreArea"}):
		whereFound = infoBox.find(attrs={"data-source": "exploreArea"}).find('div', class_="pi-data-value pi-font").text.strip()

	price = -1
	if infoBox.find(attrs={"data-source": "price"}):
		price = infoBox.find(attrs={"data-source": "price"}).find('div', class_="pi-data-value pi-font").text.strip()

	personalityList = [a.text.strip() for a in infoBox.find_all('caption', class_="pi-header pi-secondary-font pi-secondary-background pi-item-spacing")]

	personality1 = personalityList[0].replace('Personality: ', '')
	agility1 = infoBox.find_all(attrs={"data-source": "agility1"})[1].text.strip()
	strength1 = infoBox.find_all(attrs={"data-source": "strength1"})[1].text.strip()
	focus1 = infoBox.find_all(attrs={"data-source": "focus1"})[1].text.strip()
	intellect1 = infoBox.find_all(attrs={"data-source": "intellect1"})[1].text.strip()

	personality2 = personalityList[1].replace('Personality: ', '')
	agility2 = infoBox.find_all(attrs={"data-source": "agility2"})[1].text.strip()
	strength2 = infoBox.find_all(attrs={"data-source": "strength2"})[1].text.strip()
	focus2 = infoBox.find_all(attrs={"data-source": "focus2"})[1].text.strip()
	intellect2 = infoBox.find_all(attrs={"data-source": "intellect2"})[1].text.strip()

	db.execute('INSERT OR IGNORE INTO BookDragons(species, eggLine, location, price) VALUES(?,?,?,?)', dragonSpecies, eggText, whereFound, price)
	db.execute('INSERT OR IGNORE INTO dragonBaseStats(species, personality, agility, strength, focus, intellect) VALUES(?,?,?,?,?,?)', dragonSpecies, personality1, agility1, strength1, focus1, intellect1)
	db.execute('INSERT OR IGNORE INTO dragonBaseStats(species, personality, agility, strength, focus, intellect) VALUES(?,?,?,?,?,?)', dragonSpecies, personality2, agility2, strength2, focus2, intellect2)
db.commit()
