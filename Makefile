
-include CONFIG

deps: install
	#Just run full install until sudo is needed for install

install:
	@git pull --ff-only
	@virtualenv flask
	@flask/bin/pip install flask
	@flask/bin/pip install flask-httpauth
	@flask/bin/pip install python-dateutil
	@flask/bin/pip install pytest
	#pip install uwsgi
	chmod ug+x app/app.py
	echo "python version was python3 during development. You are now running:"
	python3 --version

run:
	echo "python version was python3 during development. You are now running:"
	python3 --version
	./app/app.py

install-db:
	createdb $(DB)
	psql $(DB) < sql/account_table.sql
	psql $(DB) < sql/chat_table.sql

clean:
	dropdb $(DB)
	rm -rf flask/

test:
	python3 -m pytest tests/