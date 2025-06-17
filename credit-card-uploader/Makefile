# run
run-uploader:
	python3 src/main.py

run-uploader-ai:
	python3 src/main.py ai

run-uploader-clean:
	python3 src/main.py clean

run-uploader-refresh:
	python3 src/main.py refresh

run-uploader-refresh-ai:
	python3 src/main.py refresh ai

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
