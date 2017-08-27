install:
	pip install -r requirements.txt

test:
	pytest tests

clean-build:
	rm -rf build 
	rm -rf dist 
	rm -rf python_ultimate_guitar.egg-info

docs-open:
	cd docs;make clean;make html;open _build/html/index.html