db:
	cd credit-card-uploader/ && make start-db

db-stop:
	cd credit-card-uploader/ && make stop-db

run-script:
	cd credit-card-uploader/ && make run-script

start:
	cd credit-card-reader/ && go run .