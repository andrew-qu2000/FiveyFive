FORCE:

dev_env:
	pip install -r requirements-dev.txt

docs:
	mkdir -p doc
	pydoc3 -w ./
	mv *.html doc

tests: FORCE
	python -m unittest tests.test_dynamic
