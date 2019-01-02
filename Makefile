LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.marc21.xml

src/hansteen.json: src/person_autoriteter.json scripts/authorize.py
	LC_ALL=$(LOCALE) python scripts/authorize.py

build/hansteen.marc21.xml: src/hansteen.json src/person_autoriteter.json scripts/json2marc.py
	LC_ALL=$(LOCALE) python scripts/json2marc.py src/hansteen.json > build/hansteen.marc21.xml

clean:
	rm -f build/*
