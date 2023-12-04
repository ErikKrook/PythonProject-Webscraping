"""
I den är scriptet importerar jag data om lägenheter med 3 rum från hemnet
varför just lägenheter med 3 rum är för att jag skulle vilja flytta till en 
sådan lägenhet här i Stockholm
"""
# Importetar nödvändiga biblotek
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
# De områderna som vi ska hämta data ifrån
Stockholm = {'Ekerö': '17896', 'Hanninge': '17928', 'Huddinge': '17936',
             'Älvsjö': '925971&location_ids%5B%5D=925960', 'Hägersten': '925964',
             'Gullmars': '925959', 'Tyresö': '17792', 'Nacka': '17853',
             'HässVällby': '925953', 'Sundbyberg': '18042', 'Bromma': '898740',
             'Södermalm': '898472', 'Kungsholmen': '898748', 'Gärdet': '925958',
             'Vasastan': '925970', 'Östermalm': '473448', 'Norrmalm': '925969',
             'Lidingö': '17846', 'Åkersberga': '940179', 'Vallentuna': '17804',
             'Täby': '17793', 'Sollentuna': '18027', 'Danderyd': '17892',
             'Solna': '18028'}

"""

Stockholm = {'Solna': '18028', 'Sundbyberg': '18042'}

# De egenskaper som vi web scrapar fram

bostad = {'Gata': [], 'Område': [], 'Storlek': [], 'Slutpris': [], 
          'Månadskostnad': [],'Datum': [], 'Hiss': [], 'Nyproduktion': [], 
          'Balkong': [], 'Uteplats': []}

# Ändra rum storlek 
rum_min = 2
rum_max = 4


for kommun, kod in Stockholm.items():

    # Vi får tillgång till att söka igenom 50 sidor
    for page in range(50):

        # URL:en som vi skickar för att söka efter bostäder
        url = f"https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D={kod}&page={page}&rooms_max={rum_max}&rooms_min={rum_min}"
                
        # Vi använder User-Agent header för att undvika blockering från servern
        headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        # Skickar en GET request till URL:en och hämtar HTML-innehållet från sidan
        searchTree = requests.get(url, headers=headers)
        searchSoup = BeautifulSoup(searchTree.content, 'html.parser')

        # Extraherar alla element som innehåller gatunamn från HTML-innehållet
        gata = searchSoup.find_all(
             'div', {'class': "Header_truncate__ebq7a"})

        # # Extraherar på liknade sätt
        område = searchSoup.find_all('div', {'class': "Location_address___eOo4"})

        storlek = searchSoup.find_all(
             'div', {'class': "hcl-flex--container hcl-flex--gap-2"})

        slutpris = searchSoup.find_all(
             'span', {'class': "hcl-text hcl-text--medium"})

        månadskostnad = searchSoup.find_all(
             'span', {'class': "hcl-text"})

        datum = searchSoup.find_all(
            'span', {'class': "hcl-label hcl-label--state hcl-label--sold-at"})
        
        dummy = searchSoup.find_all(
             'div', {'class': "Content_content__lg290"})
                
        
        # Varje sida innehåller 50 stycken bostäder som vi mattar in
        for i in range(len(gata)):
            
            bostad['Gata'].append(gata[i].text)
            bostad['Område'].append(område[i].text)
            bostad['Storlek'].append(storlek[i].text)
            bostad['Slutpris'].append(slutpris[i*2].text)
            bostad['Månadskostnad'].append(månadskostnad[i*3].text)
            bostad['Datum'].append(datum[i].text)
            info = dummy[i].text
            if "Hiss" in info:
                bostad['Hiss'].append(1)
            else:
                bostad['Hiss'].append(0)
                
            if "Nyproduktion" in info:
                bostad['Nyproduktion'].append(1)
            else:
                bostad['Nyproduktion'].append(0)
                
            if "Balkong" in info:
                bostad['Balkong'].append(1)
            else:
                bostad['Balkong'].append(0)
                
            if "Uteplats" in info:
                bostad['Uteplats'].append(1)
            else:
                bostad['Uteplats'].append(0)

# Gör om det till en pandas dataframe
df = pd.DataFrame(bostad)

df[['Område', 'Kommun']] = df['Område'].str.split(',', n=1, expand=True)
df['Rooms'] = df['Storlek'].str.extract(r'(\d+)\s*rum')
df['Storlek'] = df['Storlek'].str.extract(r'([\d,]+)\s*m')

# Remove non-numeric characters from the 'Slutpris' column
df['Slutpris'] = df['Slutpris'].str.replace(r'[^\d]', '', regex=True)

# Convert the column to numeric type
df['Slutpris'] = pd.to_numeric(df['Slutpris'], errors='coerce')

# Remove non-numeric characters from the 'Slutpris' column
df['Månadskostnad'] = df['Månadskostnad'].str.replace(r'[^\d]', '', regex=True)
df['Månadskostnad'] = pd.to_numeric(df['Månadskostnad'], errors='coerce')

df['Datum'] = df['Datum'].str.extract(r'Såld (.*)')

#print(df.head())

# Skriver in dataaframen i en csv fil
df.to_csv(r"Lägg till eran egen sökväg", index=False, sep =';')
