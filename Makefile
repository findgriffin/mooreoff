
build: style types test

install:
	pip3 install -r requirements.txt

style:
	flake8

types:
	mypy .

test:
	coverage run --source mooreoff -m unittest discover
	coverage html
	coverage report --fail-under=90

deploy:	build git-clean
	git push
	
git-clean:
	git diff-index --quiet HEAD
	test -z "$(git status --porcelain)"

run:
	./run.py

profile:
	./run.py --profile

clean:
	rm -rf **/__pycache__
	rm -rf **/*.pyc
