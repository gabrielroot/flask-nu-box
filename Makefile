pep8:
	python -m flake8 .
	python -m isort training --check-only

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
	python -m isort .

test:
	docker exec -it main python -m pytest -v