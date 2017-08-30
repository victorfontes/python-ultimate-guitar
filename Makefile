install:
	pip install -r requirements.txt

test:
	pytest tests

docs-open:
	cd docs;make clean;make html;open _build/html/index.html