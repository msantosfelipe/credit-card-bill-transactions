start:
	docker-compose up -d

stop:
	docker-compose stop

run:
	python3 src/main.py

create-venv:
	python3 -m venv credit-card-uploader-venv

activate:
	source credit-card-uploader-venv/bin/activate

exit-venv:
	deactivate

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt
