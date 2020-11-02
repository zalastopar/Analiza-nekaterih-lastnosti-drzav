import os
import requests
import re
#from BeautifulSoup import BeautifulSoup

#spletne strani iz katerih bomo jemali podatke
glavni_url_1 = "https://www.petfinder.com/cat-breeds/?page=" #do page 7
glavni_url_2 = "https://wamiz.co.uk/cat/breeds"
#mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"
# ime datoteke v katero bomo shranili glavno stran
filename = "pasme_mack_"
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

def save_string_to_file(text, directory, filename, i):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    filename = filename + str(i)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def url_from_file(filename):
    """Funkcija vrne seznam vseh internetnih povezav do posamezne pasme"""
    pattern = re.compile('<a href=(.*?) class="contentCard-wrap">', re.DOTALL)
    return re.findall(pattern, filename)
    


def data_from_first_url(url, directory, filename):
    for i in range(1, 8):
        url = url + str(i)
        print(url)
        text = download_url_to_string(url)
        save_string_to_file(text, directory, filename, i)
        url = url[:-1]
        filename = filename + str(i)
        print(filename)
        links = url_from_file(filename)
        print(links)
        filename = filename[:-1]
        

data_from_first_url(glavni_url_1, directory, filename)




