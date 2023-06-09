"""
I den är scriptet importerar jag data om lägenheter med 3 rum från hemnet
varför just lägenheter med 3 rum är för att jag skulle vilja flytta till en 
sådan lägenhet här i Stockholm
"""
# Importetar nödvändiga biblotek
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

for kommun, kod in Stockholm.items():

    # De egenskaper som vi web scrapar fram
    bostäder = {'Gata': [], 'Område': [], 'Kommun': [], 'Storlek': [],
                'Slutpris': [], 'Datum': [], 'Månadskostnad': [], 'Hiss': [],
                'Nyproduktion': [], 'Balkong': [], 'Uteplats': []}

    # Vi får tillgång till att söka igenom 50 sidor
    for page in range(50):

        # URL:en som vi skickar för att söka efter bostäder
        url = f"https://www.hemnet.se/salda/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D={kod}&page={page}&rooms_max=3.5&rooms_min=3"

        # Vi använder User-Agent header för att undvika blockering från servern
        headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        # Skickar en GET request till URL:en och hämtar HTML-innehållet från sidan
        searchTree = requests.get(url, headers=headers)
        searchSoup = BeautifulSoup(searchTree.content, 'html.parser')

        # Extraherar alla element som innehåller gatunamn från HTML-innehållet
        gata = searchSoup.find_all(
            'h2', {'class': "sold-property-listing__heading qa-selling-price-title"})

        # Extraherar på liknade sätt
        område = searchSoup.find_all('div', {'class': None})

        storlek = searchSoup.find_all(
            'div', {'class': "sold-property-listing__size"})

        slutpris = searchSoup.find_all(
            'div', {'class': "sold-property-listing__subheading"})

        månadskostnad = searchSoup.find_all(
            'div', {'class': "sold-property-listing__fee"})

        datum = searchSoup.find_all(
            'div', {'class': "sold-property-listing__sold-date"})

        # Varje sida innehåller 50 stycken bostäder som vi mattar in
        for i in range(len(gata)):
            bostäder['Gata'].append(gata[i].text.replace('\n', '').strip())
            info = område[i + 1].text.replace('\n', '')

            Komma = info.find(',')
            Mellanrum = info.find(' ')
            bostäder['Område'].append(info[Mellanrum:Komma].strip())
            bostäder['Kommun'].append(info[Komma + 1:].strip())
            children = storlek[i].findChildren('div')
            yta = children[0].text
            M_två = yta.find('m')
            bostäder['Storlek'].append(yta[:M_två].replace('\n', '').strip())
            if len(children) == 2:
                bostäder['Månadskostnad'].append(children[1].text.replace('\n', '')
                                                 .replace('kr/mån', '').strip())
            else:
                bostäder['Månadskostnad'].append(None)

            bostäder['Slutpris'].append(slutpris[i*2 + 1].text.replace('\n', '')
                                        .replace('Slutpris', '').replace('kr', '').strip())
            bostäder['Datum'].append(datum[i].text.replace(
                '\n', '').replace('Såld', '').strip())
            try:
                dummy = storlek[i].next_sibling.next_sibling.text.replace(
                    '\n', '').strip()
            except AttributeError:
                dummy = ''

            # Lägger till våra dummy variabler
            if 'Hiss' in dummy:
                bostäder['Hiss'].append(1)
            else:
                bostäder['Hiss'].append(0)

            if 'Balkong' in dummy:
                bostäder['Balkong'].append(1)
            else:
                bostäder['Balkong'].append(0)

            if 'Uteplats' in dummy:
                bostäder['Uteplats'].append(1)
            else:
                bostäder['Uteplats'].append(0)

            if 'Nyproduktion' in dummy:
                bostäder['Nyproduktion'].append(1)
            else:
                bostäder['Nyproduktion'].append(0)

        if len(gata) != 50:
            break

    # Gör om det till en pandas dataframe
    df = pd.DataFrame(bostäder)

    # Skriver in komunen i ett excelblad
    with pd.ExcelWriter(r"C:\Users\erikk\OneDrive\Dokument\Kaggle\HemnetData.xlsx", engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=kommun)
