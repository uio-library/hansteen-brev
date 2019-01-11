# Christopher Hansteen's correspondence

This repo contains metadata for 707 scientific letters received by
[Christopher Hansteen](https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/).
The letters themselves are stored in [Observatoriet](https://no.wikipedia.org/wiki/Observatoriet) in Oslo.
Digitized representations are available at https://uio-library.github.io/hansteen-brev/ 
and in [Oria Digital Collections](https://bibsys-almaprimo.hosted.exlibrisgroup.com/primo-explore/collectionDiscovery?vid=UIO&lang=en_US).

## History

### 1877 Registration

The scientific correspondence after Hansteen was handed of to 
[Observatoriet i Oslo](https://no.wikipedia.org/wiki/Observatoriet) 
after Hansteen's death in 1873.
In February 1877 Harald Hansteen created a catalogue of 1591 scientific letters
([Fortegnelse over Videnskabelige Breve]((https://www.ub.uio.no/fag/naturvitenskap-teknologi/astro/hansteen/brev/fortegnelse.html)).
The material was transferred to the library of
[Institute of Theoretical Astrophysics](https://no.wikipedia.org/wiki/Institutt_for_teoretisk_astrofysikk)
when the new building was conceived in 1934.

### 2004/2005 digitization project

In 2004/2005 707 letters were digitized by Museumsprosjektet (later split into EDD og MUV)
in collaboration with the University Library,
and metadata was registered in an Oracle database.
The digitization was brought to a stop halfways because of lack of funding
and the completed part was never published as intended.

### 2018 conversion and cleanup

As part of a project piloting Alma Digital for storing digitized and born-digital material,
this collection was cleaned up and converted.

The folder `initial_conversion` contains a copy of the Oracle database tables and the
scripts used to convert it to a new JSON representation, which is now kept in `src/hansteen.json`
as the master representation of the metadata.

There is a separate README.md in the initial_conversion folder with some details about
the issues encountered during the initial conversion.

The structure of the JSON representation is so that it can easily be converted to other formats.

As a start, the script `scripts/json2marc.py` converts the JSON representation to MARC21,
as used in Alma Digital.

The scanned images are not included in this repo because of the size, but will be archived in Alma D,
and are also archived at ub-prod01-imgs.

    rsync -avz --progress files/* imgs:/www/htdocs/arkiv/hansteen/files/

## Metadata structure

The collection members have the following metadata structure:

    id: Identifier unique to the collection
    alma_id: The MMS id of the linked Alma record (UIO)
    alma_representation_id: The ID of the linked Alma digital representation (UIO)
    urn: Globally unique and persistent identifier
    descriptive: object
        date: 
        date_comment:
        places: object indexed by role (TODO)
        agents: object indexed by role
        comment:
    administrative: object
        described_by:
        described_at:
        updated_at:
        collection:
    structure: list
        filename:
        label:
        filesize:
        mimetype:
        sha1: checksum


## Stats

### Antall brev etter avsender

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
Erman, A. | 19
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
Erman, senior | 6
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
