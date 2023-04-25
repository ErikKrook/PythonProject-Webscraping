"""
I den här filen web scrapar jag transfermarkt efter önskat fotbollslag och 
gör om det till en pandas dataframe
"""


# Importera nödvändiga bibliotek
import requests
from bs4 import BeautifulSoup
import pandas as pd 

# Fråga användaren efter namnet på laget som hen vill söka efter
Enter_input = input('Skriv in det lag du vill se spelarturppen på: ')

# Byt ut mellanslag med + i sökfrasen
word = Enter_input.replace(' ', '+')

# Konstruera URL för sökresultatet
url = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=" + word

# Sätt HTTP-headers för att undvika blockering från servern
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Skicka en GET-förfrågan för sökresultatet och skapa ett BeautifulSoup-objekt för att analysera HTML-koden
searchTree = requests.get(url, headers=headers)
searchSoup = BeautifulSoup(searchTree.content, 'html.parser')

# Hitta alla klubb-namn i sökresultatet
clubs = searchSoup.find_all('td', {'class' : "zentriert suche-vereinswappen"})

# Begränsa antalet klubbar som visas till högst 7
klubbar = min(len(clubs), 7)

# Skriv ut klubbarna som användaren kan välja mellan
for i in range(klubbar):
    club = clubs[i].next_sibling.find('a').text
    print(f"{i} : {club}")

# Fråga användaren efter vilket lag hen vill se spelartruppen för
lag = int(input("Skriv in siffran på det laget du vill välja: "))

# Hämta HTML-koden för valt lag
valt_lag = clubs[lag].next_sibling
href = valt_lag.find('a').get('href')
page = 'https://www.transfermarkt.com' + href
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

# Skapa tomma listor för spelare, ålder och position
PlayersList = []
AgeList = []
PositionList = []

# Hitta alla spelare och deras ålder och position
Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
Pos_Land_Ålder = pageSoup.find_all("td", {"class": "zentriert"})

antal_spelare = len(Players)

# Fyll listorna med spelarinformation
for i in range(0, antal_spelare * 3, 3):
    PositionList.append(Pos_Land_Ålder[i].get('title'))
    AgeList.append(Pos_Land_Ålder[i + 1].text)
    PlayersList.append(Players[i//3].get('title'))

# Skapa en Pandas DataFrame med spelarinformationen
SpelarInfo = {'Spelare': PlayersList, "Födelsedag": AgeList, "Position": PositionList}
              

Trupp = pd.DataFrame.from_dict(SpelarInfo)

print(Trupp)
              
              