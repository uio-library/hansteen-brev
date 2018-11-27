# Hansteens vitenskapelige korrespondanse

## Kilde

Dette repoet inneholder metadata fra 717 brev i brevsamlingen etter
[Christopher Hansteen](https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/).

Den vitenskapelige korrespondansen etter Hansten ble gitt til
[Observatoriet i Oslo](https://no.wikipedia.org/wiki/Observatoriet) etter Hansteens død i 1873.
I februar 1877 ble i alt 1591 "Videnskabelige Breve" registrert i
[en fortegnelse](https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/brev/fortegnelse.html)
av Harald Hansteen.
Materialet ble overført til
[Institutt for teoretisk astrofysikk](https://no.wikipedia.org/wiki/Institutt_for_teoretisk_astrofysikk)
da instituttet sto ferdig i 1934, og innlemmet i instituttets bibliotek og arkiv.

I 2004/2005 ble 717 brev digitalisert av Museumsprosjektet (senere splittet i EDD og MUV)
i samarbeid med Universitetsbiblioteket, og metadata ble registrert i en Oracle-database.
Mappa `src` i dette repoet er en dump fra denne Oracle-databasen.
Enkelte av tabellene (som "tema" og "sjanger") og tabellfeltene er aldri tatt i bruk,
men er inkludert for kompletthets skyld.

Selve bildefilene er ikke inkludert i dette repoet pg.a. størrelsen, men blir arkivert i Alma-D
(lenke kommer).

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
