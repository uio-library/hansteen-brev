LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.marc21.xml

build/hansteen.marc21.xml: src/hansteen.json src/person_autoriteter.json scripts/json2marc.py
	LC_ALL=$(LOCALE) python scripts/json2marc.py -a src/person_autoriteter.json src/hansteen.json > build/hansteen.marc21.xml

clean:
	rm -f build/*
