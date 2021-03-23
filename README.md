# Vpliv razvitosti države na življenje državljanov

Analizirala bom kako razvitost države in izobraženost državljanov vpliva na njihovo življenje. Za merilo razvitosti bom vzela nominalni BDP na prebivalca iz leta 2020. Opazovala bom, kako višina BDP-ja vpliva na starostno strukturo, povprečen dnevni vnos kalorij, izobraženost prebivalcev, delež prebivalsta s prekomerno težo in število uporabnikov interneta.

Podatke bom vzela iz sledečih spletnih strani:

* https://www.worldometers.info/geography/alphabetical-list-of-countries/
* https://en.wikipedia.org/wiki/List_of_countries_by_median_age
* https://en.wikipedia.org/wiki/List_of_countries_by_food_energy_intake
* https://en.wikipedia.org/wiki/List_of_countries_by_obesity_rate
* https://en.wikipedia.org/wiki/Education_Index
* https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users
* https://statisticstimes.com/economy/countries-by-projected-gdp-capita.php
* https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption
* https://en.wikipedia.org/wiki/List_of_countries_with_McDonald%27s_restaurants

Zajela bom podatke o:

* površini držav in številu prebivalcev
* starostni strukturi (mediana starosti prebivalcev, mediana starosti moških, mediana straosti žensk)
* dnevni vnos kalorij (povprečni dnevni vnos kalorij državljanov)
* debelosti prebivalstva (procent državljanov, ki imajo prekomerno težo)
* izobrazbi (izobrazbeni indeks)
* številu uporabnikov interneta
* BDP na prebivalca
* povprečna poraba energije na prebivalca v vatih
* številu McDonald's restavracij

Delovne hipoteze:

* V državah z višjim izbrazbenim indeksom večina državljanov uporablja internet.
* Države z višjim BDP p.p. imajo višje izobrazbene indekse.
* Delež prebivalcev s čezmerno težo je večji v državah z višjim BDP na prebivalca.
* Ali obstaja povezava med starostno strukturo in številom MCDnald's restavracij?
* Višji dnevni vnost kalorij pomeni večji delež prekomerno težkih.

Pobrani podatki so zbrani v csv tabeli 'drzave.csv'. Ena vrstica predstavlja eno državo, v stolpcih pa so število prebivalcev, površina, povprečna starost, povprečna starost moških, povprečna starost žensk, povprečni dnevni vnos kalorij, delež prebivalsta s čezmerno težo, indeks izobrazbe, število uporabnikov interneta, BDP.
