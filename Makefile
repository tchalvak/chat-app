
-include CONFIG

deps: install
	#Just run full install until something else is needed

install: init install-db
	@virtualenv flask
	@flask/bin/pip install flask
	@flask/bin/pip install flask-httpauth
	@flask/bin/pip install pytest
	pip install uwsgi
	chmod ug+x app.py
	#composer install

run:
	./app/app.py



init:
	@git pull



install-db:
	createdb $(DB)
	psql $(DB) < sql/account_table.sql
	psql $(DB) < sql/chat_table.sql

clean:
	dropdb $(DB)
	rm -rf flask/

test:
	python3 -m pytest tests/