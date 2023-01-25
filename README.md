# Namukilke :candy: :apple:

## Lokaaliajo

1. Luo virtualenv `python3 -m venv venv` ja käynnistä se `sourcec venv/bin/activate`
2. Aja `pip3 install -r requirements.txt` ja `source .env`.
3. Luo tietokanta ajamalla `python3 manage.py migrate`.
4. Luo kantaan tekaistua dataa ajamalla `python3 manage.py createtestdata`.
5. Käynnistä sen jälkeen namukilke ajamalla `python3 manage.py runserver`.

Mikäli devkanta täytyy jostain syystä resetoida, se tapahtuu poistamalla tiedosto `namukilke/db.sqlite3` ja toistamalla kohdat 3 ja 4.

## Yleistä

Namukilke pyörii Azuressa App Servicenä. Käytetään tabletilla ja kiltiskoneella kiltiksen wlanin yli. Tuotteiden kuvat saa ladattua admin näkymästä.

## Todo-lista

Päivitetty 12.02.2020

- [ ] React frontti?
- [x] Zoomauksen fiksaaminen deposit-sivulla (auto zoom-out tai disable zoom)
- [ ] Feedback form tuotetoiveita varten etusivulle tai ostamissivulle (Google form tai Django form)
- [x] Tuotelistauksen järjestäminen käyttäjäkohtaisesti suosituimmat tuotteet ensin
- [x] Statistiikkasivu (namu.prodeko.org/stats)
- [ ] Statistiikkasivun jatkokehitys: hävikki, käyttäjä- ja tuotekohtaiset tilastot
- [x] Admin käyttöliittymä tuotekuvien lisäämiseen palvelimelle
- [ ] Ostaminen AJAX post jotta helpompi ostaa useita tuotteita
- [ ] Timeout uloskirjautuminen esim. 1min epäaktiivisuuden jälkeen
- [ ] Tuotenimien ja varastosaldon rivitys tuotelistauksessa. Esim. max pituus nimelle tai korttien koon kasvattaminen.
- [ ] Ostoilmoituksen modalin koon ja tekstin rivittämisen korjaaminen
