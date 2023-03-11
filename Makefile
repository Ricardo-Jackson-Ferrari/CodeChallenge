## @ system
.PHONY: run
run: ## run the system
	docker-compose up -d --build -V
stop: ## stop the system
	docker-compose down

## @ build
superuser: ## create superuser for django admin access
	docker-compose exec app python manage.py createsuperuser