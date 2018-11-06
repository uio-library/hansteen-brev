LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.json build/hansteen.marc21.xml

build/hansteen.json: src/*.csv scripts/csv2json.py
	LC_ALL=$(LOCALE) python scripts/csv2json.py src > build/hansteen.json

build/hansteen.marc21.xml: build/hansteen.json aut/person_autoriteter.json scripts/json2marc.py
	LC_ALL=$(LOCALE) python scripts/json2marc.py aut/person_autoriteter.json build/hansteen.json > build/hansteen.marc21.xml

clean:
	rm -f build/*
