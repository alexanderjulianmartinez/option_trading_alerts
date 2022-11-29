.PHONY: clean

clean:
	rm -f MANIFEST
	rm -rf build dist

.PHONY: test

test:
	tox

requirements:
	pip install -r requirements.txt