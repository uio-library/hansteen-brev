# Christopher Hansteens korrespondanse

## Kilde

Dette repoet inneholder metadata for 715 brev mottatt av
[Christopher Hansteen](https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/),
som oppbevares i [Observatoriet](https://no.wikipedia.org/wiki/Observatoriet).

Den vitenskapelige korrespondansen etter Hansten ble gitt til
[Observatoriet i Oslo](https://no.wikipedia.org/wiki/Observatoriet) etter Hansteens død i 1873.
I februar 1877 ble i alt 1591 "Videnskabelige Breve" registrert i
[en fortegnelse](https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/brev/fortegnelse.html)
av Harald Hansteen.
Materialet ble overført til
[Institutt for teoretisk astrofysikk](https://no.wikipedia.org/wiki/Institutt_for_teoretisk_astrofysikk)
da instituttet sto ferdig i 1934, og innlemmet i instituttets bibliotek og arkiv.

I 2004/2005 ble <s>717</s> (715 etter duplikatfjerning) brev digitalisert av Museumsprosjektet (senere splittet i EDD og MUV)
i samarbeid med Universitetsbiblioteket, og metadata ble registrert i en Oracle-database.
Mappa `src` i dette repoet er en dump fra denne Oracle-databasen.
Enkelte av tabellene (som "tema" og "sjanger") og tabellfeltene er aldri tatt i bruk,
men er inkludert for kompletthets skyld.

Selve bildefilene er ikke inkludert i dette repoet pg.a. størrelsen, men blir arkivert i Alma-D
(lenke kommer). De er også kopiert til ub-prod01-imgs:

    rsync -avz --progress files/* imgs:/www/htdocs/arkiv/hansteen/files/

## Konvertering

Repoet inneholder script for å konvertere CSV-tabellene til en JSON-representasjon
og til en MARC21XML-utgave.
Kjør `make clean && make` om du vil gjøre konverteringen på nytt:

1. `scripts/linkfiles.py` kobler filnavn med brev. Informasjonen lagres i `filer_brev.json`.
2. `scripts/csv2json.py` leser inn tabellene fra `src/*.csv` og lager en
   forenklet JSON-struktur som lagres som `build/hansteen.json`.
3. `scripts/json2marc.py` leser inn `build/hansteen.json`, kombinerer dette med
   navneautoriteter fra `aut/person_autoriteter.json` og lager en MARC21-utgave
   som lagres som `build/hansteen.marc21.xml`.


## Duplikate tilvekstnumre

Tabellen `foto_kort.csv` inneholder en rad per brev.
Kolonnnen `tilvekstnr` er stort sett unik, men med følgende unntak:

Tilvekstnr | Foto_kort_id | Filnavn | Konklusjon
---|---|---|---
`Boeck120443` | 7 | Boeck120443s1.tif | Forkastes. Samme brev som 8 og ingen forskjell i klassifikasjon.
| 8 | Boeck120443s1_2.tif | Ingen endring
`Duexxxxxx` | 243 | Duexxxxxxs1.tif<br>Duexxxxxxs2.tif<br>Duexxxxxxs3.tif<br>Duexxxxxxs4.tif | Endres til `Duexxxxxx_1`
| 244 | Duexxxxxxs1_2.tif<br>Duexxxxxxs2_2.tif<br>Duexxxxxxs3_2.tif<br>Duexxxxxxs4_2.tif<br>Duexxxxxxv1s1.tif<br>Duexxxxxxv1s2.tif | Endres til `Duexxxxxx_2`
| 249 | Duexxxxxxs1_3.tif<br>Duexxxxxxs2_3.tif<br>Duexxxxxxs3_3.tif | Endres til `Duexxxxxx_3`
`Ermanxxxxxx` | 266 | Ermannxxxxxxs1.tif<br>Ermannxxxxxxs2.tif<br>Ermannxxxxxxs3.tif<br>Ermannxxxxxxs4.tif | Endres til `Ermanxxxxxx_1`
| 278 | Ermanxxxxf.tif<br>Ermanxxxxs1.tif<br>Ermanxxxxs2.tif<br>Ermanxxxxs3.tif<br>Ermanxxxxs4.tif | Endres til `Ermanxxxxxx_2`
| 280 | Ermanxxxxxxf_2.tif<br>Ermanxxxxxxs1_2.tif<br>Ermanxxxxxxs2_2.tif<br>Ermanxxxxxxs3.tif | Endres til `Ermanxxxxxx_3`
| 282 | Ermansenxxxxxxs1.tif | Endres til `Ermanxxxxxx_4`
| 283 | Ermanxxxxxxf_3.tif<br>Ermanxxxxxxs1_3.tif<br>Ermanxxxxxxs2_3.tif<br>Ermanxxxxxxs3_2.tif<br>Ermanxxxxxxs4.tif<br>Ermanxxxxxxs5.tif  | Endres til `Ermanxxxxxx_5`
`Sommer011033` | 612 | Sommerfeldta011033s1.tif<br>Sommerfeldta011033s2.tif<br>Sommerfeldta011033s3.tif | Endres til `Sommer011033_1`
| 613 | Sommerfeldtb011033f.tif<br>Sommerfeldtb011033s1.tif<br>Sommerfeldtb011033s2.tif | Endres til `Sommer011033_2` 
`Svanbe220551` | 641 | Svanberg220551f.tif<br>Svanberg220551s1.tif<br>Svanberg220551s2.tif<br>Svanberg220551s3.tif | Endres til `Svanbe220551_1`
| 642 | Svanberg220551bf.tif<br>Svanberg220551bs1.tif<br>Svanberg220551bs2.tif<br>Svanberg220551bs3.tif | Endres til `Svanbe220551_2`
`Baeyer010964` | 691 | Baeyer010964b.tif<br>Baeyer010964f.tif<br>Baeyer010964s1.tif | Forkastes. Samme brev som 691 og ingen forskjell i klassifikasjon.
| 739 | Baeyer010964b_2.tif<br>Baeyer010964f_2.tif<br>Baeyer010964s1_2.tif | Ingen endring


## TIFF-filer med flere sider

Tre av tiff-filene inneholdt flere sider:

Originalt filnavn | Side | Konklusjon
---|---|---
`Perthes-Besser290854s1.tif` | `Perthes-Besser290854s1-0.tif` | duplikat av `Perthes-Besser290854f.tif`, slettes
 | `Perthes-Besser290854s1-1.tif` | → `Perthes-Besser290854s1.tif`
Perthes-Besser300861s1.tif | Perthes-Besser300861s1-0.tif | fargeprøve, slettes
 | Perthes-Besser300861s1-1.tif | → Perthes-Besser300861s1.tif
Perthes-Besser300861v1s1.tif | Perthes-Besser300861v1s1-0.tif | fargeprøve, slettes
| Perthes-Besser300861v1s1-1.tif | duplikat av Perthes-Besser300861s1.tif, slettes
Perthes-Besser300861v1s1-2.tif | → Perthes-Besser300861v1.tif
```

## Standardisering av filnavn

Fra | Til
---|---
Akrell180144sf.tif | Akrell180144f.tif
Berzeulius080844sf.tif | Berzeulius080844f.tif
Bohr310718s2s1.tif | Bohr310718s2d1.tif
Bohr310718s2s2.tif | Bohr310718s2d2.tif
Droysonvls1.tif Droysonvs1.tif
Droysonvls2.tif Droysonvs2.tif
erman111261s1.tif | Erman111261s1.tif
Forchhammr160362s1.tif | Forchhammer160362s1.tif
Forchhammr160362s2.tif | Forchhammer160362s2.tif
Gurhans220142s1d1 | Guthans220142s1d1
Guthns190254s1.tif | Guthans190254s1.tif
Schuma090127s1.tif | Schumacher090127s1.tif
Schumcher060332s1.tif | Schumacher060332s1.tif
sebald140354 | Sebald140354s1.tif
Brewter110324s1.tif | Brewster110324s1.tif
Brimont110457s1.tif | Brimont110857s1.tif


---



## Antall brev etter avsender

3 brev har ukjent avsender.

Avsender | Antall brev
------|--------
Schumacher, S. H. | 89
Sabine | 58
Åstrand, J. J. | 41
Perthes-Besser & Maucke | 35
Berzelius, J. | 26
Airz, G. B. | 19
Due, Chr. | 18
Erman, A. | 18
Forchhammer | 17
Sebald, W. | 16
Struve, W. | 15
Due, Fr. | 14
Boeck, Chr. | 13
Buys-Ballot | 13
Cronstrand, Simon Anders | 11
Bohr | 11
Svanberg, G. | 11
Goldschmidt | 11
Forbes, J. | 10
Argelander, Friedrich Wilhelm August | 7
Erman, senior | 7
Schmidt, J. W. | 6
Fiandt, A. | 6
Schweigger | 6
Brewster, David | 5
Deichmann, J. | 5
Segelcke, Lorents | 5
Erichsen, O. W. | 5
Schubert, F. W. | 5
Geelmuyden | 5
Galton, F. | 4
Guthans | 4
Bache, A. D. | 4
Daniele | 4
Sibbern, G. | 4
Brandes, H. W. | 4
Ertel | 4
Falckmann | 3
Sandels, Johan A. | 3
Sievers | 3
Bugge | 3
Diricks | 3
Ferry | 3
d'Abbadie, Antoine Thomson | 3
Barlow, Peter | 3
Frisch, C. F. | 3
Farraday, M. | 3
Scheerer, Th. | 3
Fries, E. | 3
Baeyer | 3
Evensen, M. | 2
Gaimard | 2
Sommerfeldt, H. | 2
Degen, C. F. | 2
Stjerneld | 2
Beaufort, J. | 2
Arnold & Dent | 2
Focke, W. | 2
Flügel, J. G. | 2
Banks, Joseph | 2
Andresen | 2
Akrell, C. | 2
Beaufoy, Henry | 2
Bond, G. P. | 2
Bretteville | 2
Suchtelen | 2
Cappelen, Jørgen W. | 2
Agardh, John Mortimer | 2
Christie, J. K. | 2
Foss, H. | 2
Stevenson, W. | 2
Galle, G. | 2
Sterky, G. | 2
Broch, Ole Jacob | 2
Grosch, C. H. | 2
Strecker, Adolph | 2
Schramm, Hugo | 1
Dartoud | 1
Scharling, E. A. | 1
Gasse, H. v. | 1
Edlund, E. | 1
Brauer, C. A. | 1
Flod, H.R. | 1
Fleming, W. | 1
Stark | 1
Brimmont | 1
Droyson | 1
Gutkæs | 1
Gørbitz, J. | 1
Barth, J. A. | 1
de Boigne, Paul | 1
Bloomfield | 1
Gribeth, L. | 1
Berghaus | 1
Greve | 1
Daurlov | 1
Donner | 1
Crowe, J. R. | 1
Busch | 1
Fitz Roy, R. | 1
Arago, Dominique François Jean | 1
Frapolli | 1
Farin, G. | 1
Gasmann | 1
Dirckingck-Holmfeldt | 1
Bergsager, A. O. | 1
Anderson, Sam. | 1
Grey | 1
Steinheil, C. A. | 1
Friess, G. | 1
Glasenapp | 1
Rosseland, s | 1
Sharswood, William | 1
Gibson, Milner | 1
Autenrieth, A. | 1
Stewart, Balfour | 1
Daubru | 1
Constable, W. | 1
Furrbye | 1
Graham, J. | 1
Anderson, N. J. | 1
Sæland, Sem | 1
Dahl | 1
Skaar, G. W. | 1
Dahl, Johan | 1
Delambre | 1
Det kong. Frederiks universitetet | 1
Engelhart | 1
Fuss | 1
Balfur | 1
Fearnley, H. | 1
Sterks Eaton, Henry | 1
Silveira | 1
Gyldendalske Boghandling | 1
Steffens | 1
Fehr's, L. Enke | 1
Fogtmann, N. | 1
Fabrie, A. | 1
Ångström, Anders Jonas | 1
Dublin Sirkulære | 1
Dove, H. W. | 1
Gjessing | 1
Sefström, W. G. | 1
Sundriet | 1
Scott, Robert H. | 1
Seehusen, O.J. | 1
Barrat, J. | 1
Foerster, W. | 1
Brosset, L. | 1
Anker, Carsten | 1
Englund, W. | 1
Böcker | 1
Graah | 1
Bystrøm, Th. | 1
Feldtmann, J. | 1
Fuhr | 1
Smith, Chr. | 1
Esendorp | 1
Griesebach | 1
Everlöf | 1
Gauss | 1
Cutterbuck, R. | 1
Schmidt, C. S. | 1
Bergh, C. F. | 1
Fåhræus A. C. | 1
Greiner, G. | 1
