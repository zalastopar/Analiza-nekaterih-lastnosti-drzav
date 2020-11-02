import csv
import os
import requests
import re
#from BeautifulSoup import BeautifulSoup

#spletne strani iz katerih bomo jemali podatke
glavni_url = "https://wamiz.co.uk/cat/breeds"
pomozni_url = "https://wamiz.co.uk"
#mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"
directory2 = "pasme"
# ime datoteke v katero bomo shranili glavno stran
filename = "pasme_mack"
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = "pasme_mack"

#######################################################################################################
#pobiramo podatke iz glavni_url_1
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

##########################################################################################################################
# Poiščemo spletne strani za posamezno mačko
#############################################################################################################################

#želimo poiskati linke do pasem
def link_from_file(page_content):
    """Funkcija poišče povezave do posamezne vrste."""

    pattern = re.compile('<a href="([^"]*)" class="listView-item-title--homepageBreed">')
    result = re.findall(pattern, page_content)
    return result


def get_cats_files(links, directory):
    """Funkciija za vsako pasmo shrani spletno stran pasme in jo poimenuje
     kot vrsta pasme"""
    
    for url in links:
        ime = re.compile('\d/(.*)', re.DOTALL)
        ime = re.search(ime, url).group(1)
        url = pomozni_url + url
        save_frontpage(url, directory, ime)
        html_data = read_file_to_string(directory, ime)



def data_from_first_url(url, directory, directory2, filename):
    save_frontpage(url, directory, filename)
    html_data = read_file_to_string(directory, filename)
    links = link_from_file(html_data)
    get_cats_files(links, directory2)
    return links







