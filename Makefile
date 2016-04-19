
deps: install
	#no-op for now

install: init install-db
	@virtualenv flask
	@flask/bin/pip install flask
	@flask/bin/pip install flask-httpauth
	chmod ug+x app.py
	#composer install

run:
	./app.py



init:
	@git pull



install-db:
	createdb ca
	psql ca < sql/account_table.sql
	psql ca < sql/chat_table.sql

clean:
	dropdb ca
	rm -rf flask/

test:
	vendor/bin/phpunit