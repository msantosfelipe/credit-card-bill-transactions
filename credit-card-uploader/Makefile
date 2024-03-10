start-db:
	docker-compose up -d

stop-db:
	docker-compose stop

import:
	python3 src/process_import.py

tag:
	python3 src/process_tag.py

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

# Insert tags in DB
insert-tags:
	docker cp src/tags.json credit_card_reader_mongo:/tags.json && \
	docker exec -it credit_card_reader_mongo mongo credit_card_reader_mongo --eval 'db.tags.drop()' && \
	docker exec -it credit_card_reader_mongo mongoimport --db credit_card_reader_mongo --collection tags --file /tags.json --jsonArray