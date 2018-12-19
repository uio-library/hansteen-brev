LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.json build/hansteen.marc21.xml

src/filer_brev.json: src/filer.csv src/filer_oversettelse.csv scripts/linkfiles.py
	LC_ALL=$(LOCALE) python scripts/linkfiles.py > src/filer_brev.json

build/hansteen.json: src/filer_brev.json src/*.csv scripts/csv2json.py
	LC_ALL=$(LOCALE) python scripts/csv2json.py src > build/hansteen.json

build/hansteen.marc21.xml: build/hansteen.json aut/person_autoriteter.json scripts/json2marc.py
	LC_ALL=$(LOCALE) python scripts/json2marc.py -a aut/person_autoriteter.json build/hansteen.json > build/hansteen.marc21.xml

clean:
	rm -f build/* src/filer_brev.json
