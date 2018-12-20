# Notes fromt the 2018 cleanup & conversion

Run `make clean && make` to re-do the conversion.

1. `linkfiles.py` links files with letters, storing the results in `filer_brev.json`.
2. `csv2json.py` reads the tables from`src/*.csv` and creates a simpler JSON structure
   that is stored in `build/hansteen.json`.

## Cleanup

### Establishing `tilvekstnr` as a unique identifier

The column `tilvekstnr` was *mostly* unique, but with a few exceptions.

Tilvekstnr | Foto_kort_id | Filnavn | Action taken
---|---|---|---
`Boeck120443` | 7 | Boeck120443s1.tif | Delete. This is the same letter as 8 and there is no difference in the description.
| 8 | Boeck120443s1_2.tif | No change needed.
`Duexxxxxx` | 243 | Duexxxxxxs1.tif<br>Duexxxxxxs2.tif<br>Duexxxxxxs3.tif<br>Duexxxxxxs4.tif | Rename to `Duexxxxxx_1`
| 244 | Duexxxxxxs1_2.tif<br>Duexxxxxxs2_2.tif<br>Duexxxxxxs3_2.tif<br>Duexxxxxxs4_2.tif<br>Duexxxxxxv1s1.tif<br>Duexxxxxxv1s2.tif | Rename to `Duexxxxxx_2`
| 249 | Duexxxxxxs1_3.tif<br>Duexxxxxxs2_3.tif<br>Duexxxxxxs3_3.tif | Rename to `Duexxxxxx_3`
`Ermanxxxxxx` | 266 | Ermannxxxxxxs1.tif<br>Ermannxxxxxxs2.tif<br>Ermannxxxxxxs3.tif<br>Ermannxxxxxxs4.tif | Rename to `Ermanxxxxxx_1`
| 278 | Ermanxxxxf.tif<br>Ermanxxxxs1.tif<br>Ermanxxxxs2.tif<br>Ermanxxxxs3.tif<br>Ermanxxxxs4.tif | Rename to `Ermanxxxxxx_2`
| 280 | Ermanxxxxxxf_2.tif<br>Ermanxxxxxxs1_2.tif<br>Ermanxxxxxxs2_2.tif<br>Ermanxxxxxxs3.tif | Rename to `Ermanxxxxxx_3`
| 282 | Ermansenxxxxxxs1.tif | Rename to `Ermanxxxxxx_4`
| 283 | Ermanxxxxxxf_3.tif<br>Ermanxxxxxxs1_3.tif<br>Ermanxxxxxxs2_3.tif<br>Ermanxxxxxxs3_2.tif<br>Ermanxxxxxxs4.tif<br>Ermanxxxxxxs5.tif  | Rename to `Ermanxxxxxx_5`
`Sommer011033` | 612 | Sommerfeldta011033s1.tif<br>Sommerfeldta011033s2.tif<br>Sommerfeldta011033s3.tif | Rename to `Sommer011033_1`
| 613 | Sommerfeldtb011033f.tif<br>Sommerfeldtb011033s1.tif<br>Sommerfeldtb011033s2.tif | Rename to `Sommer011033_2` 
`Svanbe220551` | 641 | Svanberg220551f.tif<br>Svanberg220551s1.tif<br>Svanberg220551s2.tif<br>Svanberg220551s3.tif | Rename to `Svanbe220551_1`
| 642 | Svanberg220551bf.tif<br>Svanberg220551bs1.tif<br>Svanberg220551bs2.tif<br>Svanberg220551bs3.tif | Rename to `Svanbe220551_2`
`Baeyer010964` | 691 | Baeyer010964b.tif<br>Baeyer010964f.tif<br>Baeyer010964s1.tif | Delete. This is the same letter as 691 and there is no difference in the description.
| 739 | Baeyer010964b_2.tif<br>Baeyer010964f_2.tif<br>Baeyer010964s1_2.tif | No change needed.

This process reduced the number of records from 717 to 715.

### Establishing filenames based on the `tilvekstnr`

The files had filenames whose base were *similar* to the `tilvekstnr`, but it seems like they had been entered manually since they could vary quite a bit, sometimes an abbreviated
version, sometimes an elongated version, sometimes a typo in the name, and so on.
Since there is no need to have this degree of freedom, the filenames were normalized based on the `tilvekstnr`, taking care that no files were overwritten or lost in the renaming process.
The new filenames are similar to the old ones, but are much more consistent.

### Cleaning up invalid dates



### TIFF-files with multiple pages

A few tiff files contained multiple pages.

Original filename | Page | Action taken
---|---|---
`Perthes-Besser290854s1.tif` | `Perthes-Besser290854s1-0.tif` | Deleting as duplicate of `Perthes-Besser290854f.tif`
 | `Perthes-Besser290854s1-1.tif` | Extracting as `Perthes-Besser290854s1.tif`
Perthes-Besser300861s1.tif | Perthes-Besser300861s1-0.tif | Deleting as color sample
 | Perthes-Besser300861s1-1.tif | Extracting as Perthes-Besser300861s1.tif
Perthes-Besser300861v1s1.tif | Perthes-Besser300861v1s1-0.tif | Deleting as color sample
| Perthes-Besser300861v1s1-1.tif | Deleting as duplicate of Perthes-Besser300861s1.tif
| Perthes-Besser300861v1s1-2.tif | Extracting as Perthes-Besser300861v1.tif

### Filename normalization

From | To
----|----
AAastrand010159 | AAstrand010159
Akrell180144sf.tif | Akrell180144f.tif
Berzeulius080844sf.tif | Berzeulius080844f.tif
Bohr310718s2s1.tif | Bohr310718s2d1.tif
Bohr310718s2s2.tif | Bohr310718s2d2.tif
Droysonvls1.tif | Droysonvs1.tif
Droysonvls2.tif | Droysonvs2.tif
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


### Merging of letters and their attachments

Attachments sometimes contained their own records, othertimes not.
The standalone cases were merged with their parent letters so that attachments never have their own record.

* `AAstrand010960v` merged into `AAstrand010960`
* `AAstrand010164v` merged into `AAstrand010164`
* `Banks140919v` merged into `Banks140919`
* `AAstrand12065v1` and `AAstrand12065v2` merged into `AAstrand120659`
* `AAstrand190961v` merged into `AAstrand190961`
* `AAstrand25066v1` and `AAstrand25066v2` merged into `AAstrand250660`

This process reduced the number of records from 715 to 707.
