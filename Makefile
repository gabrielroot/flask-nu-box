pep8:
	# stop the build if there are Python syntax errors or undefined names
	python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

	python -m isort . --check-only

up: 
	docker-compose up

down:
	docker-compose down

clean:
	@echo "Execute cleaning ..."
	- find -iname "*.pyc" -delete 2>/dev/null
	- find -iname ".coverage" -delete 2>/dev/null
	- find -iname "coverage.xml" -delete 2>/dev/null
	- find -iname "*.swp" -delete 2>/dev/null

fix-import: clean
	python -m isort .

test:
	python -m pytest -v -W ignore --cov=nuBox --cov-report=term-missing
