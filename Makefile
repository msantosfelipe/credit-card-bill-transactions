db:
	docker compose up -d

db-stop:
	docker compose stop

import:
	cd credit-card-uploader/ && make import

reader:
	cd credit-card-reader/ && go run .