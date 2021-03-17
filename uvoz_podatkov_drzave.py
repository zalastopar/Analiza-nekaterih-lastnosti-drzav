import csv
import os
import requests
import re

# spletne strani iz katerih bomo jemali podatke
linki = {
"url1" : "https://www.worldometers.info/geography/alphabetical-list-of-countries/",
"url2" : "https://en.wikipedia.org/wiki/List_of_countries_by_median_age",
"url3" : "https://en.wikipedia.org/wiki/List_of_countries_by_food_energy_intake",
"url4" : "https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate",
"url5" : "https://en.wikipedia.org/wiki/Education_Index",
"url6" : "https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users",
"url7" : "https://en.wikipedia.org/wiki/List_of_countries_with_McDonald%27s_restaurants"
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
"filename7" : "mcdonalds"
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

def ustvari_slovar(sez, kategorije):
    """ Funkcija iz seznama tuplov ustvari seznam slovarjev, tako da vsak slovar pripada eni drzavi.
    """
    drzave = []
    for el in sez:
        slovar = {}
        slovar['drzava'] = el[0]
        i = 1
        for k in kategorije:
            slovar[k] = el[i]
            i += 1
        drzave.append(slovar)
    return drzave



## Glavno - prebivalstvo in gostota - (country, population, land area)
def glavni(page_content):
    pattern = re.compile('<tr> <td>.*?</td> <td style="font-weight: bold; font-size:15px">(.*?)</td> <td style="font-weight: bold; text-align:right"><a href="/world-population/.*?/">(.*?)</a></td> <td style="text-align:right">(.*?)</td> <td style="text-align:right">(.*?)</td> </tr>')
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['prebivalstvo', 'povrsina [km^2]'])
    return novo 

## Starost - (country, 2020 combined, male, female)
def starost(page_content):
    pattern = re.compile(r'<tr>\n<td align="left">.*?<span class="datasortkey" data-sort-value="(.*?)".*?</span>.*?</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)\n</td></tr>')
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

## Izobrazba - (country, education index)
def izobrazba(page_content):
    pattern = re.compile(r'<tr>\n<td>\d*</td>\n<td align="left">.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>.*?\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['indeks izobrazbe'])
    return novo

## Internet - (country, internet users, percent of population)
def internet(page_content):
    pattern = re.compile(r'<tr>\n<td>\d*</td>\n<td>.*?title=".*?">(.*?)</a></td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?</td>\n<td>(.*?)</td>\n<td>.*?</td>\n<td>.*?\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    novo = ustvari_slovar(result, ['st uporabnikov interneta', 'procent uporabnikov interneta'])
    return novo

## McDonald's restavracije ########
def mcdonalds(page_content):
    pattern = re.compile(r'<tr>\n<th>(17)\n</th>\n.*?title=".*?">(Curaçao)</a> <span style="font-size:85%;">(part of <span class="flagicon"><img alt="" src="//upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/23px-Flag_of_the_Netherlands.svg.png" decoding="async" width="23" height="15" class="thumbborder" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/35px-Flag_of_the_Netherlands.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/45px-Flag_of_the_Netherlands.svg.png 2x" data-file-width="900" data-file-height="600" />&#160;</span><a href="/wiki/Netherlands" title="Netherlands">(Netherlands)</a>)</span>\n</td>\n<td>August 16, 1974\n</td>\n<td><a href="/wiki/Willemstad" title="Willemstad">Willemstad</a>\n</td>\n<td>5\n</td>\n<td>(source: McDonald\'s 2013)\n</td>\n<td>32,203\n</td>\n<td>See <a rel="nofollow" class="external text" href="https://web.archive.org/web/20160406091702/http://www.mcdonalds.aw/">McDonald\'s Aruba and Curaçao</a>\n</td></tr>', re.DOTALL)
    result = re.findall(pattern, page_content)
    return result

'''
re.compile(r'<tr>\n<th>1\n(</th>)\n<td><span class="datasortkey" data-sort-value="United States"><span class="flagicon"><img alt="" src="//upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/23px-Flag_of_the_United_States.svg.png" decoding="async" width="23" height="12" class="thumbborder" srcset="//upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/35px-Flag_of_the_United_States.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/46px-Flag_of_the_United_States.svg.png 2x" data-file-width="1235" data-file-height="650" />&#160;</span><a href="/wiki/United_States" title="United States">United States</a></span>\n</td>\n<td data-sort-value="May 15, 1940">May 15, 1940<br />Franchise: April 13, 1955\n</td>\n<td><a href="/wiki/San_Bernardino" class="mw-redirect" title="San Bernardino">San Bernardino</a>, <a href="/wiki/California" title="California">California</a><br /><a href="/wiki/Des_Plaines,_Illinois" title="Des Plaines, Illinois">Des Plaines, Illinois</a> <small>(Franchise)</small>\n</td>\n<td>14,146<sup id="cite_ref-auto1_7-0" class="reference"><a href="#cite_note-auto1-7">&#91;7&#93;</a></sup>\n</td>\n<td>(source: Investopedia November 15, 2018)\n</td>\n<td>23,130\n</td>\n<td>See <a rel="nofollow" class="external text" href="http://www.mcdonalds.com/">McDonald\'s USA</a>\n</td></tr>', re.DOTALL)
'''

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



##########################################################################################################################
# Obdelane podatke shranimo v csv datoteko
##########################################################################################################################

# seznam slovarjev želimo shraniti kot csv
def save_as_csv(filename, list):
    colnames = [*list[1]]
    
    with open(filename, 'w', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = colnames) 
        writer.writeheader() 
        writer.writerows(list) 




############################################################################################################################
# Izvedemo program
############################################################################################################################


def main(redownload=True, reparse=True):
    """Funkcija izvede celotno pridobivanje podatkov
    1. shrani vse spletne strani
    2. shrani stran od vsake pasme
    3. podatke, ki jih potrebujemo uredi v slovar
    4. podatke shrani v csv tabelo"""


    drzave = []
    for i in range(1, 7):
        # naložimo spletne strani za vsako kategorijo
        save_frontpage(linki["url" + str(i)], directory, imena["filename" + str(i)])
        html_data = read_file_to_string(directory, imena["filename" + str(i)])

        # izluscimo potrebne podatke
        umesni = eval(imena["filename" + str(i)])(html_data)

        # sproti sestavljamo slovarje
        drzave = zdruzi(drzave, umesni, [])
    # shranimo v csv datoteko
    save_as_csv(csv_filename, drzave)






if __name__ == '__main__':
    main()



html_data1 = read_file_to_string(directory, "glavni")
glav = glavni(html_data1)

html_data2 = read_file_to_string(directory, "starost")
star = starost(html_data2)

html_data3 = read_file_to_string(directory, "vnos_kalorij")
kcal = vnos_kalorij(html_data3)

html_data4 = read_file_to_string(directory, "debelost")
deb = debelost(html_data4)

html_data5 = read_file_to_string(directory, "izobrazba")
izo = izobrazba(html_data5)

html_data6 = read_file_to_string(directory, "internet")
inter = internet(html_data6)




