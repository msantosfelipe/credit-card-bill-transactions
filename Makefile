up:
	docker compose up -d

down:
	docker compose stop

reader:
	cd credit-card-reader/ && go run .
