LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.marc21.xml

src/hansteen.json: src/places.json src/agents.json scripts/authorize.py
	LC_ALL=$(LOCALE) python scripts/authorize.py

build/hansteen.marc21.xml: src/hansteen.json scripts/json2marc.py
	LC_ALL=$(LOCALE) python scripts/json2marc.py src/hansteen.json > build/hansteen.marc21.xml

clean:
	rm -f build/*
