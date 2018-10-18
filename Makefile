install:
	pip install -r requirements.txt

test:
	pytest --no-print-logs -p no:cacheprovider tests/$(path)
