reset_db: 
	python3 -m app.db.reset_db

run: 
	uvicorn app.main:app --reload

test: 
	PYTHONPATH=. pytest

test_verbose: 
	PYTHONPATH=. pytest -v

db-size: 
	psql -U taskuser -d taskdb -h localhost -c "SELECT COUNT(*) FROM tasks;"

packages: 
	pip freeze > requirements.txt


