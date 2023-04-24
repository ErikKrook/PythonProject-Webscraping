# Importera nödvändiga bibliotek
import requests
from bs4 import BeautifulSoup
import pandas as pd 

# Ange url och headrar för webbsidan
url = "https://www.transfermarkt.com/premier-league/gesamtspielplan/wettbewerb/GB1/saison_id/2022"

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Använd requests-biblioteket för att skicka en GET-begäran och hämta webbsidans innehåll.
searchTree = requests.get(url, headers=headers)

# Skapa en BeautifulSoup-objekt för att hämta data från webbsidan
searchSoup = BeautifulSoup(searchTree.content, 'html.parser')

# Skapa en dictionary som ska innehålla matchinformationen
matcher = {'Hemma': [], 'Borta': [], "Resultat": []}

# Hitta alla hemma- och bortalag på webbsidan
hometeams = searchSoup.find_all('td', {'class':"text-right no-border-rechts hauptlink"})
awayteams = searchSoup.find_all('td', {'class':"no-border-links hauptlink"})

# Loopa igenom alla matcherna och hämta hemma- och bortalag samt resultat.
for i in range(380):
    hemma = hometeams[i].text
    borta = awayteams[i].text
    resultat = hometeams[i].nextSibling.nextSibling.nextSibling.nextSibling.text[1:4] #Resultatet
    
    # Kolla om resultatet finns med på sidan. Om det inte finns med så lägg inte till matchen i matchernas dictionary.
    if '-' not in resultat:
        matcher['Hemma'].append(hemma.split(")",1)[1].lstrip()) # Lägg till hemmalag i matchernas dictionary
        matcher['Borta'].append(borta.split("(",1)[0].rstrip()) # Lägg till bortalag i matchernas dictionary
        matcher['Resultat'].append(resultat) # Lägg till matchresultat i matchernas dictionary

# Skapa en pandas dataframe med matchinformationen
df = pd.DataFrame.from_dict(matcher)

# Spara matchinformationen till en CSV-fil på datorn
df.to_csv(r"Lägg till eran sökväg", index=False)
