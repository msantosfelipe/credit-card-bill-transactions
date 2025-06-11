up:
	cd credit-card-bill-uploader && docker compose up -d

down:
	cd credit-card-bill-uploader && docker compose stop

reader:
	cd credit-card-reader/ && go run .

viewer:
	cd credit-card-viewer/ && npm start