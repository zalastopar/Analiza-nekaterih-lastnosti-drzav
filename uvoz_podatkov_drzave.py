import csv
import os
import requests
import re
from bs4 import BeautifulSoup

# spletne strani iz katerih bomo jemali podatke
linki = {
"url1" : "https://www.worldometers.info/geography/alphabetical-list-of-countries/",
"url2" : "https://en.wikipedia.org/wiki/List_of_countries_by_median_age",
"url3" : "https://en.wikipedia.org/wiki/List_of_countries_by_food_energy_intake",
"url4" : "https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate",
"url5" : "https://en.wikipedia.org/wiki/Education_Index",
"url6" : "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users",
"url7" : "https://statisticstimes.com/economy/countries-by-projected-gdp-capita.php",
"url8" : "https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption",
"url9" : "https://www.atlasbig.com/en-us/countries-mcdonalds-shops"
}

# mapa, v katero bomo shranili podatke
directory = "zajeti_podatki"
# ime datoteke v katero bomo shranili glavno stran
imena = {
"filename1" : "glavni",
"filename2" : "starost",
"filename3" : "vnos_kalorij",
"filename4" : "debelost",
"filename5" : "izobrazba",
"filename6" : "internet",
"filename7" : "bdp",
"filename8" : "energija",
"filename9" : "mcdonalds"

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

def spremeni_v_float(el):
    if ',' in el:
        return float(el.replace(',', ''))
    elif '-' in el:
        return None
    elif el == '':
        return None
    else:
        return float(el)

def ustvari_slovar(sez, kategorije):
    """ Funkcija iz seznama tuplov ustvari seznam slovarjev, 
    tako da vsak slovar pripada eni drzavi.
    """
    drzave = []
    for el in sez:
        slovar = {}
        slovar['drzava'] = el[0]
        i = 1
        for k in kategorije:
            slovar[k] = spremeni_v_float(el[i])
            i += 1
        drzave.append(slovar)
    return drzave

def izlusci_stevilo(el):
    i = len(el) - 1
    nov = ''
    while i >= 0:
        if el[i] in '1234567890,.':
            nov = el[i] + nov
            i = i - 1
        else:
            i = -1
    return nov



## Glavno - prebivalstvo in gostota - (country, population, land area)
def glavni(page_content):
    pattern = re.compile('<tr> <td>.*?</td> <td style="font-weight: bold; font-size:15px">(.*?)</td> <td style="font-weight: bold; text-align:right"><a href="/world-population/.*?/">(.*?)</a></td> <td style="text-align:right">(.*?)</td> <td style="text-align:right">(.*?)</td> </tr>')
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['prebivalstvo', 'povrsina [km^2]'])

    return novo 

## Starost - (country, 2020 combined, male, female)
def starost(page_content):
    pattern = re.compile(r'<tr>\n<th scope="row"><span class="datasortkey" .*?title=".*?">(.*?)</a>.*?\n.*?\n.*?\n.*?\n<td>(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)\n</td></tr>', re.DOTALL)

    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['povprecna starost', 'starost moski', 'starost zenske'])

    return novo

## Vnos kalorij - (country, average daily kcal)
def vnos_kalorij(page_content):
    pattern = re.compile(r'<tr>.*? title=".*?">(.*?)</a>\n</td>\n<td style="text-align:right;">(.*?)\n</td>.*?\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['povprecni vnos kcal'])

    return novo

## Debelost - (country, obesity rate %)
def debelost(page_content):
    pattern = re.compile(r'<tr>\n.*? title=".*?">(.*?)</a>\n</td>\n<td>\d*\n</td>\n<td>(.*?)\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['% prekomero tezkih'])

    return novo

## Izobrazba - (country, education index)  ###############
def izobrazba(page_content):
    pattern = re.compile(r'<tr>\n<td>\d*</td>\n<td align="left">.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>.*?\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['indeks izobrazbe 2015'])

    return novo

## Internet - (country, internet users, percent of population)
#    pattern = re.compile(r'<tr>\n<td>\d*</td>\n<td>.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>(.*?)%</td>\n<td>.*?</td>\n<td>.*?\n</td></tr>', re.DOTALL)

def internet(page_content): #######################3
    pattern = re.compile(r'<tr>\n<td>\d*</td>\n<td>.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>.*?%</td>\n<td>.*?</td>\n<td>.*?\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['st uporabnikov interneta'])
    print(novo)
    return novo

## BDP - (country, 2020 gdp)
def bdp(page_content):
    pattern = re.compile(r'<tr><td class="name">(.*?)</td><td class="data">(.*?)</td>.*?</tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['bdp 2020'])
    print(novo)
    return novo

## Energija - (country, energy consumption)
def energija(page_content):
    pattern = re.compile(r'<tr>\n<td>\d*?</td>.*? title=".*?">(.*?)</a></td>\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n<td>(.*?)\n</td></tr>', re.DOTALL)
    result = [(el[0], izlusci_stevilo(el[1])) for el in re.findall(pattern, page_content)]
    novo = ustvari_slovar(result, ['poraba energije [vat]'])
    return novo

## McDonald's restavracije ########
def mcdonalds(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    table = soup.find_all('table')[0]
    result = []
    for row in table.find_all('tr')[1:]:
        sez = []
        for i in row.find_all(text=True):
            sez.append(i.strip())
        result.append((sez[4], sez[7], sez[9]))
    novo = ustvari_slovar(result, ['st restavracij', 'st restavracij na 100k ljudi'])
    return novo



############################################################################################################################
# Urejanje podatkov
############################################################################################################################

def zdruzi(sez1, sez2, nova):
    ''' Funkcija dva seznama slovarjev rekurzivno zdruzi, tako da eni drzavi pripada en slovar.    '''
    sez1 = sorted(sez1, key=lambda k: k['drzava'])
    sez2 = sorted(sez2, key=lambda k: k['drzava'])
    if sez1 == []:
        return nova + sez2
    elif sez2 == []:
        return nova + sez1
    elif sez1[0]['drzava'] == sez2[0]['drzava']:
        return zdruzi(sez1[1:], sez2[1:], nova + [{**sez1[0], **sez2[0]}])
    elif sez1[0]['drzava'] < sez2[0]['drzava']:
        return zdruzi(sez1[1:], sez2, nova + [sez1[0]])
    else:
        return zdruzi(sez1, sez2[1:], nova + [sez2[0]])

##########################################################################################################################
# Popravki imen
##########################################################################################################################

def poisci_in_izbrisi(imena, sez):
    """ Funkcija za državo, ki ima različne zapise spravljene v seznamu 'imena', 
    ustvari samo en slovar, ga doda v 'sez' in izbrise potrebne slovarje.
    """
    nov = {}
    a = len(sez)
    for i in range(a-1, -1, -1):
        if sez[i]['drzava'] in imena:
            nov = {**nov, **sez[i]}
            sez.remove(sez[i])
    sez.append(nov)


def spremeni_drzave(sez):
    """ Nekatere drzave imajo razlicna poimenovanja. Funkcija jih poenoti."""

    for el in [['Bahamas', 'The Bahamas'], ['Brunei', 'Brunei ', 'Brunei Darussalam'], ['Cabo Verde', 'Cape Verde'], ['Congo (Congo-Brazzaville)', 'Congo', 'Republic of the Congo', 'Congo, Republic of the'], ["C&ocirc;te d'Ivoire", "Cote d'Ivoire", "Côte d'Ivoire", "Ivory Coast"], ['Czech Republic', 'Czechia (Czech Republic)'], ['DR Congo', 'Democratic Republic of the Congo', 'Congo, Democratic Republic of the'], ['Eswatini (Swaziland)', 'Eswatini', 'Eswatini (fmr. "Swaziland")', 'Swaziland'], ['F.S. Micronesia', 'Federated States of Micronesia', 'Micronesia, Federated States of', 'Micronesia'], ['Gambia', 'The Gambia'], ['Myanmar (Burma)', 'Myanmar', 'Myanmar (formerly Burma)'], ['Macedonia', 'North Macedonia'], ['Palestine', 'Palestine State', 'Palestinian Authority'], ['Russia', 'Russian Federation'], ['Syrian Arab Republic', 'Syria'], ['Timor Leste', 'Timor-Leste'], ['United States', 'United States of America'], ['Viet Nam', 'Vietnam'], ['The Netherlands', 'Netherlands'], ['Slovak Republic', 'Slovakia'], ['Taiwan Province of China', 'Taiwan'], ['Pakistan', 'Pakistan\n     '], ['Lebanon', 'Lebanon\n     '], ['Hong Kong', 'Hong Kong SAR'], ['Venezuela', 'Venezuela\n     '], ['Islamic Republic of Iran', 'Iran']]:
        poisci_in_izbrisi(el, sez)
    




##########################################################################################################################
# Obdelane podatke shranimo v csv datoteko
##########################################################################################################################

# seznam slovarjev želimo shraniti kot csv
def save_as_csv(filename, lst):
    colnames = [*lst[4], 'bdp 2020', 'povprecni vnos kcal']
    
    with open(filename, 'w', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = colnames) 
        writer.writeheader() 
        writer.writerows(lst) 





############################################################################################################################
# Izvedemo program
############################################################################################################################


def main(redownload=True, reparse=True):
    """Funkcija izvede celotno pridobivanje podatkov
    1. shrani vse spletne strani
    2. poisce ustrezne podatke
    3. podatke, ki jih potrebujemo uredi v slovar
    4. podatke shrani v csv tabelo"""


    drzave = []
    for i in range(1, 10):
        # naložimo spletne strani za vsako kategorijo
        save_frontpage(linki["url" + str(i)], directory, imena["filename" + str(i)])
        html_data = read_file_to_string(directory, imena["filename" + str(i)])

        # izluscimo potrebne podatke
        umesni = eval(imena["filename" + str(i)])(html_data)

        # sproti sestavljamo slovarje
        drzave = zdruzi(drzave, umesni, [])

    spremeni_drzave(drzave)
    drzave = sorted(drzave, key=lambda k: k['drzava'])


    # shranimo v csv datoteko
    save_as_csv(csv_filename, drzave)


if __name__ == '__main__':
    main()


'''

html_data = read_file_to_string('zajeti_podatki', 'internet')
a = internet(html_data)
print(a)
'''




