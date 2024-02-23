start-db:
	docker-compose up -d

stop-db:
	docker-compose stop

run-script:
	python3 src/main.py

create-venv:
	python3 -m venv credit-card-uploader-venv

activate:
	source credit-card-uploader-venv/bin/activate

exit-venv:
	deactivate

freeze:
	pip3 freeze > requirements.txt

install:
	pip3 install -r requirements.txt
