# DokumenttiSovellus
* Sovelluksessa hallitaan dokumenttitietokantaa
* Käyttäjien, Dokumenttien, Dokumenttien muistiinpanojen, Avainsanojen lisäys ja muokkaus.
* Kaikki dokumenttien muistiinpanojen muutokset tallennetaan historiaan.

## Sovelluksen tila:
* Sovelluksen tietokanta on valmis ja suurin osa toiminnallisuudesta tehty.
* Uusien muistiinpanojen liittäminen dokumentteihin puuttuu.
* Dokumenttien hakeminen avainsanalla puuttuu.
* Syötteen validointeja ei ole tehty eikä virhetilanteita käsitellä vielä siististi.
* Käyttöliittymässä on vähän parannettavaa käytettävyyden suhteen.
* Käyttöoikeuksien tarkistuksia ei ole kaikkialla.
* Virheitä saattaa esiintyä.

## Käyttöohje
### Yleistä
* kolme erityyppistä käyttäjää normaali/admin/superuser
* superuser voi luoda käyttäjiä, admin voi pääsee asetusvalikkoon, normaalikäyttäjällä vähiten oikeuksia.
### Käyttö
* sovellukseen kirjaudutaan sisään jonka jälkeen tullaan päänäkymään jossa listattu sovellukseen tallennetut dokumentit.
* admin ja superuser -käyttäjillä näkyy myös Settings-linkki josta
pääsee muokkaamaan käyttäjätietoja.
* Pääsivulta admin/superuser voi muokata listan oikeasta reunasta
dokumenttien oleellisimpia tietoja.
* Kaikki käyttäjät voivat avata dokumentin päänäkymän vasemman reunan linkeistä ( id, nimi ).
* Dokumenttinäkymässä näkyy ensin päätiedot sitten avainsanat ja linkki josta niitä pääsee muokkaamaan.
* Avainsanojen alla on lista dokumenttiin liitettyjä muistiinpanoja
joita pääsee muokkaamaan otsikon linkistäê
* Mustiinpanon muokkaussivulla on myös linkki muokkaushistoriaan joka avautuu omalle sivulleen.
* ( Tämän projektin puitteissa sovelluksessa ei siis ole tarkoitus pystyä lataamaan itse dokumentteja vaikka tarkoitus on itse myöhemmin jatkaa sovellusta toisella ohjelmointikielellä siihen suuntaan. Senpä takia sovelluksessa on jo paikka tiedostonimelle vaikka sellaista ei pysty tallentamaan.)

## Testaus Herokussa:

https://prelude-to-document-app.herokuapp.com/

* superuser: amiga/amiga
* admin: atari/atari
* normaalit: sega/sega, amstrad/amstrad
