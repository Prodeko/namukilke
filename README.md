# Namukilke

Python 3.6.7 | Django 2.1.0

Pyörii palvelimella virtuaaliympäristön sisällä `source venv/bin/activate`.

Käytetään tabletilla ja kiltiskoneella kiltiksen wlanin yli.

Toistaiseksi tuotekuvien hallintaan ei ole admin käyttöliittymää. Esim. uuden tuotteen tuotekuvan lisääminen vaatii kuvan lisäämisen palvelimelle kansioon `namu/static/img`, johon Namusetä tarvinnee Webbitiimin apua.

## Todo-lista
Päivitetty 7.12.2018
- [ ] Zoomauksen fiksaaminen deposit-sivulla (auto zoom-out tai disable zoom)
- [ ] Feedback form tuotetoiveita varten etusivulle tai ostamissivulle (Google form tai Django form)
- [ ] Tuotelistauksen järjestäminen käyttäjäkohtaisesti suosituimmat tuotteet ensin
- [ ] Statistiikkasivu (namu.prodeko.org/stats) josta voi seurata hävikkiä sekä käyttäjä- ja tuotekohtaisia tilastoja
- [ ] Admin käyttöliittymä tuotekuvien lisäämiseen palvelimelle
- [ ] Ostaminen AJAX post jotta helpompi ostaa useita tuotteita
- [ ] Timeout uloskirjautuminen esim. 1min epäaktiivisuuden jälkeen
- [ ] Tuotenimien ja varastosaldon rivitys tuotelistauksessa. Esim. max pituus nimelle tai korttien koon kasvattaminen.
- [ ] Ostoilmoituksen modalin koon ja tekstin rivittämisen korjaaminen
