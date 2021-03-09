import csv
import os
import requests
import re

# spletne strani iz katerih bomo jemali podatke
linki = {
"url1" : "https://www.worldometers.info/geography/alphabetical-list-of-countries/",
"url2" : "https://en.wikipedia.org/wiki/List_of_countries_by_median_age",
"url3" : "https://en.wikipedia.org/wiki/List_of_countries_by_central_bank_interest_rates",
"url4" : "https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate",
"url5" : "https://en.wikipedia.org/wiki/Education_Index",
"url6" : "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users",
"url7" : "https://en.wikipedia.org/wiki/List_of_countries_by_forest_area",
"url8" : "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_military_and_paramilitary_personnel"
}

# mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"
# ime datoteke v katero bomo shranili glavno stran
imena = {
"filename1" : "glavni",
"filename2" : "starost",
"filename3" : "obrestna_mera",
"filename4" : "debelost",
"filename5" : "izobrazba",
"filename6" : "internet",
"filename7" : "gozd",
"filename8" : "vojska"
}
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = "drzave.csv"

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


#######################################################################################################
# Izluscimo podatke za vsako kategorijo
#######################################################################################################

## Glavno - prebivalstvo in gostota
def prebivalstvo_in_gostota(page_content):
    pattern = re.compile('<tr> <td>.*?</td> <td style="font-weight: bold; font-size:15px">(.*?)</td> <td style="font-weight: bold; text-align:right"><a href="/world-population/.*?/">(.*?)</a></td> <td style="text-align:right">(.*?)</td> <td style="text-align:right">(.*?)</td> </tr>')
    result = re.findall(pattern, page_content)
    return result 

## Starost
def starost(page_content):
    pattern = re.compile(r'<tr>\n<td align="left"><span class="datasortkey" data-sort-value="(.*?)".*?</span></td>\n<td>.*?</td>\n<td>.*?</td>\n<td>(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)\n</td></tr>')
    result = re.findall(pattern, page_content)
    return result

## Obrestna mera
def obrestna_mera(page_content):
    pattern = re.compile(r'<tr>\n<td align="left">.*? title=".*?">(.*?)</a></td>\n<td>(.*?)</td>.*?</tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

## Debelost
def debelost(page_content):
    pattern = re.compile(r'<tr>.*? title=".*?">(.*?)</a>\n</td>\n<td>.*?\n</td>\n<td>(.*?)\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

## Izobrazba
def izobrazba(page_content):
    pattern = re.compile(r'<tr>\n<td>\d*?</td>\n<td( data-sort-value|><img alt=).*?</td>.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>.*?</tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return [match[1:] for match in result]

## Internet
def internet(page_content):
    pattern = re.compile(r'<tr>.*? title=".*?">(.*?)</a></td>\n<td>(.*?)</td>.*?</tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

## Gozd
def gozd(page_content):
    pattern = re.compile(r'<tr>.*? title=".*?">(.*?)</a></td>\n.*?\n.*?\n.*?\n<td style="text-align: right;">(.*?)\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

## Vojska
def vojska(page_content):
    pattern = re.compile(r'<tr .*? title=".*?">(Armenia)</a><sup id="cite_ref-7" class="reference"><a href="#cite_note-7">&#91;7&#93;</a></sup><sup id="cite_ref-8" class="reference"><a href="#cite_note-8">&#91;Note 1&#93;</a></sup><sup id="cite_ref-9" class="reference"><a href="#cite_note-9">&#91;Note 2&#93;</a></sup>\n</td>\n<td style="text-align:right;">44,800\n</td>\n<td style="text-align:right;">210,000\n</td>\n<td style="text-align:right;">4,300\n</td>\n<td style="text-align:right;">259,100\n</td>\n<td style="text-align:right;">85.3\n</td>\n<td style="text-align:right;">(14.7)\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

############################################################################################################################
# Izvedemo program
############################################################################################################################


def main(redownload=True, reparse=True):
    """Funkcija izvede celotno pridobivanje podatkov
    1. shrani vse spletne strani
    2. shrani stran od vsake pasme
    3. podatke, ki jih potrebujemo uredi v slovar
    4. podatke shrani v csv tabelo"""

    #naložimo spletne strani za vsako kategorijo
    #for i in range(1, 9):
    #    save_frontpage(linki["url" + str(i)], directory, imena["filename" + str(i)])
    #    html_data = read_file_to_string(directory, imena["filename" + str(i)])


#if __name__ == '__main__':
#    main()



html_data = read_file_to_string(directory, "vojska")
links = vojska(html_data)
print(links)

