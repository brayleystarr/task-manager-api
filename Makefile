# database commands
db-reset: 
	PGPASSWORD=password psql -h localhost -U taskuser -d taskdb -f app/db/reset_db.sql

db-shell: 
	PGPASSWORD=password psql -h localhost -U taskuser -d taskdb

db-view: 
	PGPASSWORD=password psql -h localhost -U taskuser -d taskdb -f app/db/view_db.sql

# FastAPI commands
run-dev: 
	uvicorn app.main:app --reload

run-prod: 
	uvicorn app.main:app 

test: 
	PYTHONPATH=. pytest

test-verbose: 
	PYTHONPATH=. pytest -v

# other commands
update-packages: 
	pip freeze > requirements.txt

	