LOCALE:="no_NO"
.PHONY: all
all: build/hansteen.json

build/filer_brev.json: src/filer.csv src/filer_oversettelse.csv linkfiles.py
	LC_ALL=$(LOCALE) python linkfiles.py > build/filer_brev.json

build/hansteen.json: build/filer_brev.json src/*.csv csv2json.py
	LC_ALL=$(LOCALE) python csv2json.py > build/hansteen.json

clean:
	rm -f build/*
