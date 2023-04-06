pep8:
	flake8 .
	isort training --check-only

up: 
	docker-compose up

down:
	docker-compose down

clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml

fix-import: clean
	isort . -rc