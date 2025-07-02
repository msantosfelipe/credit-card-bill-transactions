up:
	cd credit-card-uploader && docker compose up -d

down:
	cd credit-card-uploader && docker compose stop

reader:
	cd credit-card-reader/ && go run .
