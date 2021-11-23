FORCE:

dev_env:
	pip install -r requirements-dev.txt

docs:
	mkdir -p doc
	pydoc -w ./
	mv *.html doc
