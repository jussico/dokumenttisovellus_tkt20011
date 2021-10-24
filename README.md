# DokumenttiSovellus
* Sovelluksessa hallitaan dokumenttitietokantaa
* Käyttäjien, Dokumenttien, Dokumenttien muistiinpanojen, Avainsanojen lisäys ja muokkaus.
* Kaikki dokumenttien muistiinpanojen muutokset tallennetaan historiaan.

## Sovelluksen tila:
* Sovellus toimii eikä ole tiedossa olevia virheitä.
* Käyttöoikeudet tarkistetaan joka paikassa.
* Syötteet validoidaan.
* CSRF-haavoittuvuus on huomioitu kaikissa formeissa.
* Käyttöliittymässä on ihan basic html eikä graafiseen suunnitteluun ole panostettu.

## Käyttöohje
### Yleistä
* kolme erityyppistä käyttäjää normaali/admin/superuser
* superuser voi luoda käyttäjiä ja muokata kaikkia käyttäjiä. superuser on myös admin.
* admin pääsee asetusvalikkoon ja voi muokata normaalikäyttäjiä.
* admin voi lisätä dokumentteja ja muistiinpanoja dokumentteihin.
* normaalikäyttäjä voi selata dokumentteja ja muokata muistiinpanoja.
### Käyttö
* sovellukseen kirjaudutaan sisään jonka jälkeen tullaan päänäkymään jossa listattu sovellukseen tallennetut dokumentit.
* admin ja superuser -käyttäjillä näkyy myös Settings-linkki josta
pääsee muokkaamaan käyttäjätietoja.
* Pääsivulta admin/superuser voi muokata listan oikeasta reunasta
dokumenttien oleellisimpia tietoja.
* Kaikki käyttäjät voivat avata dokumentin päänäkymän vasemman reunan linkeistä ( id, nimi ).
* Dokumenttinäkymässä näkyy ensin päätiedot sitten avainsanat ja linkki josta niitä pääsee muokkaamaan.
* Avainsanojen alla on lista dokumenttiin liitettyjä muistiinpanoja, joita pääsee muokkaamaan otsikon linkistäê
* Mustiinpanon muokkaussivulla on myös linkki muokkaushistoriaan joka avautuu omalle sivulleen.
* ( tämän projektin puitteissa ei toteutettu itse tiedostojen lisäämistä, eiköhän tässäkin ollut riittämiin. )

## Testaus Herokussa:

https://prelude-to-document-app.herokuapp.com/

* superuser: amiga/amiga
* admin: atari/atari
* normaalit: sega/sega, amstrad/amstrad
