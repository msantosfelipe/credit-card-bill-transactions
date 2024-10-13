DB_NAME=credit_card_reader_mongo
CONTAINER_NAME=credit_card_reader_mongo

upload: drop-collections insert-tags
	python3 src/process_upload.py

upload-samples: drop-collections insert-sample-tags
	python3 src/process_upload.py --sample

tag: drop-collections insert-tags
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
	docker cp src/tags.json $(CONTAINER_NAME):/tags.json && \
	docker exec -it $(CONTAINER_NAME) mongo $(DB_NAME) --eval 'db.tags.drop()' && \
	docker exec -it $(CONTAINER_NAME) mongoimport --db $(DB_NAME) --collection tags --file /tags.json --jsonArray

insert-sample-tags:
	docker cp samples/tags.json $(CONTAINER_NAME):/tags.json && \
	docker exec -it $(CONTAINER_NAME) mongo $(DB_NAME) --eval 'db.tags.drop()' && \
	docker exec -it $(CONTAINER_NAME) mongoimport --db $(DB_NAME) --collection tags --file /tags.json --jsonArray

drop-collections:
	docker exec -it $(CONTAINER_NAME) mongo $(DB_NAME) --eval 'db.getCollectionNames().forEach(function(c) { db[c].drop(); })'
