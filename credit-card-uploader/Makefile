up:
	cd ../ && docker compose up -d

down:
	cd ../ && docker compose down

up-ai:
	ollama run mistral

down-ai:
	ollama down mistral

# run
run-uploader:
	python3 src/main.py ai

run-uploader-not-ai:
	python3 src/main.py

run-uploader-clean:
	python3 src/main.py clean

run-uploader-refresh:
	python3 src/main.py refresh ai

run-uploader-refresh-not-ai:
	python3 src/main.py refresh

# venv
create-venv:
	python3 -m venv venv-credit-card-uploader

activate:
	source venv-credit-card-uploader/bin/activate

exit-venv:
	deactivate

# config
install:
	pip3 install -r requirements.txt

freeze:
	pip3 freeze > requirements.txt
