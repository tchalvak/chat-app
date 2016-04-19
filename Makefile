
deps:
	composer install

install: install-db
	composer install



install-db:
	createdb ca
	psql ca < account_table.sql
	psql ca < chat_table.sql

clean:
	dropdb ca

test:
	vendor/bin/phpunit