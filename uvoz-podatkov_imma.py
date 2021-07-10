import csv
import os
import requests
import re
from bs4 import BeautifulSoup
import time

# spletne strani iz katerih bomo jemali podatke
link = 'https://opensea.io/assets/0xdb55584e5104505a6b38776ee4dcba7dd6bb25fe/'

# mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"

# ime datoteke v katero bomo shranili glavno stran
ime = 'Visitor'

# ime CSV datoteke v katero bomo shranili podatke
csv_filename = "immadegen.csv"

#######################################################################################################
# Shranimo podatke iz spletnih strani
#######################################################################################################

def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})
    except requests.exceptions.ConnectionError:  
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Prislo je do napake pri povezovanju")
        return None
    #status code nam pove, kaksen je bil odgovor
    if page_content.status_code == requests.codes.ok:
        return page_content.text
        pass
    # nadaljujemo s kodo če je prišlo do napake
    print("Težava pri vsebini strani")
    return None

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""

    html = download_url_to_string(page)
    if html: #če je vsaj nekaj(ni None)
        save_string_to_file(html, directory, filename)
        return True

    raise NotImplementedError()

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot 
    niz"""
    with open(os.path.join(directory, filename), encoding="utf-8") as f:
        return f.read()


############################################################################################################################
# Izluscimo podatke
############################################################################################################################


# dobimo lastnosti
def dobi_vsebino(page_content):
    """ Funkcija poišče vse lastnosti Visitorja."""
    soup = BeautifulSoup(page_content, 'lxml')
    property = soup.find_all("div", class_= "Property--type")
    value = soup.find_all("div", class_= "Property--value")
    return [property, value]


# dobimo ceno/bid
def oceni(page_content):
    """ Funkcija ugotovi, ali je Visitor na prodaj po fiksni ceni 
    ali je na dražbi ali pa ni naprodaj in poišče ceno kartice. 
    Če Visitor ni na prodaj, mu pripiše ceno 'None'. 
    Na koncu ustvari slovar z ustreznimi podatki."""

    soup = BeautifulSoup(page_content, 'lxml')
    slovar = {}

    # izrazi, s katerimi ugotovimo način ocenjevanja vrednosti
    izraz_za_ceno = re.compile(r'Current price', re.DOTALL)
    izraz_za_min_bid = re.compile(r'Minimum bid', re.DOTALL)
    izraz_za_top_bid = re.compile(r'Top bid', re.DOTALL)

    # preverimo, če ima Visitor fiksno ceno
    if bool(re.search(izraz_za_ceno, page_content)):
        cena = soup.find("div", class_= "Overflowreact__OverflowContainer-sc-10mm0lu-0 fqMVjm Price--amount")
        slovar['Type'] = 'Buy'
        slovar['Price'] = cena.text
        return slovar

    # preverimo, če je na dražbi
    elif bool(re.search(izraz_za_min_bid, page_content)):
        bid = soup.find("div", class_= "Overflowreact__OverflowContainer-sc-10mm0lu-0 fqMVjm Price--amount")
        slovar['Type'] = 'Min bid'
        slovar['Price'] = bid.text
        return slovar

    # preverimo, če je na dražbi in ima ponudbo
    elif bool(re.search(izraz_za_top_bid, page_content)):
        bid = soup.find("div", class_= "Overflowreact__OverflowContainer-sc-10mm0lu-0 fqMVjm Price--amount")
        slovar['Type'] = 'Top bid'
        slovar['Price'] = bid.text
        return slovar

    # vsi ostali pa niso na prodaj
    else: 
        slovar['Type'] = 'Not for sale'
        slovar['Price'] = None
        return slovar










############################################################################################################################
# Urejanje podatkov
############################################################################################################################


def naredi_slovar(marsovec, property, value):
    slovar = {}
    slovar['Name'] = marsovec
    for (p, v) in zip(property, value):
        slovar[p] = v
    return slovar



def izluscimo_text(marsovec, sez):
    property = [el.text for el in sez[0]]
    value = [el.text for el in sez[1]]
    slovar = naredi_slovar(marsovec, property, value)
    return slovar



############################################################################################################################
# Obdelane podatke shranimo v csv datoteko
############################################################################################################################

############################################################################################################################
# Izvedemo program
############################################################################################################################


def main(redownload=True, reparse=True):
    """Funkcija izvede celotno pridobivanje podatkov
    1. shrani vse spletne strani
    2. poisce ustrezne podatke
    3. podatke, ki jih potrebujemo uredi v slovar
    4. podatke shrani v csv tabelo"""

    slovarji = []

    for i in range(6249, 10000):
        time.sleep(0.1)
        # naložimo spletne strani za vsako kategorijo
        save_frontpage(link + str(i), directory, ime + str(i))
        html_data = read_file_to_string(directory, ime + str(i))
        vsebina = dobi_vsebino(html_data)
        slovar = izluscimo_text(ime + str(i), vsebina)
        slo = oceni(html_data)
        slovar.update(slo)
        slovarji.append(slovar)
        


    print(slovarji)






if __name__ == '__main__':
    main()


