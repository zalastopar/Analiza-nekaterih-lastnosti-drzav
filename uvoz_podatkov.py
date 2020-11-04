import csv
import os
import requests
import re
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup

#spletne strani iz katerih bomo jemali podatke
glavni_url = "https://wamiz.co.uk/cat/breeds"
pomozni_url = "https://wamiz.co.uk"
#mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"
directory2 = "pasme_html"
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

#iz številskih podatkov, ki imajo okoli besedilo želimo samo število
def izlusci_stevilo(dictionary):
    """Funkcija iz vrednosti slovarja, ki so besedne in številske vzame samo številke"""

    pattern = re.compile('\d+')
    for key, value in dictionary.items():
        for el in value:
            stevilke = re.findall(pattern, el)
            if len(stevilke) != 0:
                dictionary[key] = stevilke
    return dictionary

def get_cats_files(links, directory):
    """Funkciija za vsako pasmo shrani spletno stran pasme in jo poimenuje
     kot vrsta pasme"""
    
    for url in links:
        ime = re.compile('\d/(.*)', re.DOTALL)
        ime = re.search(ime, url).group(1)
        url = pomozni_url + url
        save_frontpage(url, directory, ime)
        html_data = read_file_to_string(directory, ime)

def how_many_points(tacke, lastnosti):
    """Funkcija prevede število slikic tačk na točke 1 do 3, ki si jih mucek pri posamezni lastnosti zasluži."""

    tacke = [tacke[x:x+3] for x in range(0, len(tacke),3)]
    lastnosti_in_ocene = {}
    for ocena in tacke:
        lastnosti_in_ocene[lastnosti[0]]= ocena.count("yellow")
        del lastnosti[0]
        
    return lastnosti_in_ocene

def make_dict_from_list_of_tuples(list):
    """Funkcija iz seznama tuplov naredi slovar"""

    dictionary = {}
    for el in list:
        if len(el) > 2:
            dictionary[el[0] + " " + el[1][-2:]] = el[1].split(", ")
            dictionary[el[2] + " " + el[3][-2:]] = el[3].split(", ")
        else: 
            dictionary[el[0]] = el[1].split(", ")
        
    return dictionary

#izbrskaj želene podatke in jih uredi v slovar
def get_data_from_file(directory, filename):
    """Funkcija bo iz datoteke za pasmo pobrala potrebne podatke in jih spravila v slovar"""

    html_data = read_file_to_string(directory, filename)

    #želimo podatke iz kvadratka
    kvadratek = re.compile('<li class="breed-list-item">\s*([^"]*) :\s*<span>\s*(.*?)\s*</span>')
    znacilnosti_iz_kvadratka = re.findall(kvadratek, html_data)
    dict_kv = make_dict_from_list_of_tuples(znacilnosti_iz_kvadratka)
    dict_kv = izlusci_stevilo(dict_kv)

    #želimo podatke iz dveh tabel
    tabela = re.compile('<table class="breed-specification-table--detail">\s*<tr>\s*<td>\s*([^"]*)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*</tr>\s*\s*<tr>\s*<td>\s*([^"]*)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*</tr>\s*</table>')
    znacilnosti_iz_tabel = re.findall(tabela, html_data)
    dict_tab = make_dict_from_list_of_tuples(znacilnosti_iz_tabel)
    dict_tab = izlusci_stevilo(dict_tab)

    #želimo ocene lastnosti
    #dobimo podatek ali je tačka rumena ali siva
    tacke = re.compile('(yellow|grey)-paw')
    tacke_ocene = re.findall(tacke, html_data)
    #dobimo ven lastnosti, ki so ocenjene s tačkami
    lastnosti = re.compile('<div class="breed-details-heading">\s*<h3 class="breed-heading-title">\s*(.*?)\s*</h3>')
    seznam_lastnosti = re.findall(lastnosti, html_data)
    dict_ocene = how_many_points(tacke_ocene, seznam_lastnosti)

    #združimo slovarje
    dict_kv.update(dict_tab)
    dict_kv.update(dict_ocene)

    return dict_kv

def list_of_cats(directory):
    """Funkcija bo dobila slovar za vsako mačko in jih spravila v seznam"""

    cat_list = []

    for filename in os.listdir(directory):
        dictionary = {}
        dictionary["Breed"] = filename
        dictionary.update(get_data_from_file(directory, filename))
        cat_list += [dictionary]
    return cat_list


##########################################################################################################################
# Obdelane podatke shranimo v csv datoteko
##########################################################################################################################

#seznam slovarjev želimo shraniti kot csv
def save_as_csv(filename, lis):
    colnames = [*lis[0]]
    colnames = [col.replace('Abyssinian Cat', 'Breed') for col in colnames]
    
    with open(filename, 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = colnames) 
        writer.writeheader() 
        writer.writerows(lis) 




#morš preimoenovat slovar ... tm kjer je pasma and dogs etc. dej breed povsod





def data_from_first_url(url, directory, directory2, filename, csv_filename):
    save_frontpage(url, directory, filename)
    html_data = read_file_to_string(directory, filename)
    links = link_from_file(html_data)
    get_cats_files(links, directory2)
    lists = list_of_cats(directory2)
    save_as_csv(csv_filename, lists)





data_from_first_url(glavni_url, directory, directory2, filename, csv_filename)
#print(list_of_cats(directory2))    
#print(get_data_from_file(directory2, "bengal"))
#save_as_csv()
