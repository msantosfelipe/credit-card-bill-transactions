db:
	cd credit-card-uploader/ && make start-db

db-stop:
	cd credit-card-uploader/ && make stop-db

import:
	cd credit-card-uploader/ && make import

reader:
	cd credit-card-reader/ && go run .