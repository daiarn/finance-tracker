makemigrations:
	@docker-compose run --rm web python ./manage.py makemigrations

migrate:
	@docker-compose run --rm web python ./manage.py migrate

cli:
	@docker-compose run --rm web bash
