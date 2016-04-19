
deps: init
	#composer install

run:
	./app.py

install: init install-db
	git pull
	virtualenv flask
	flask/bin/pip install flask
	flask/bin/pip install flask-httpauth
	chmod ug+x app.py
	#composer install

init:
	#pull latest from github as necessary
	git pull



install-db:
	createdb ca
	psql ca < account_table.sql
	psql ca < chat_table.sql

clean:
	dropdb ca
	rm -rf flask/

test:
	vendor/bin/phpunit