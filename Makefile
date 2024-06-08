db:
	docker compose up -d

db-stop:
	docker compose stop

install-requirements:
	cd credit-card-uploader/ && make install

upload:
	cd credit-card-uploader/ && make upload

reader:
	cd credit-card-reader/ && go run .

viewer:
	cd credit-card-viewer/ && npm start