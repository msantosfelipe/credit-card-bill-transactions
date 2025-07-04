# Credit card bill uploader

Read credit card bills and store data in database

## Banks supported
- C6 (CSV files)
- XP (CSV files)

## Integrations
- Firebase Storage
- Mongo Atlas

## Instalation
- Activate venv `python3 -m venv venv-credit-card-uploader` and `source venv-credit-card-uploader/bin/activate`

- Install dependencies `pip3 install -r requirements.txt`

- After using deactivate venv `deactivate`

## Run
- Upload new files:
    - First time running:
        - Run `mkdir data/creds` and `mkdir data/tmp_files`
        - Create a bucket on Firebase and generate .json credentials file and put it in `data/creds`
        - Run `cp data/samples/categories.json data/`
  - (If not running database) Run `docker compose up -d`
  - Configure venv (see Makefile) and run `make run-uploader`


# ollama minstral
- Install:  `curl -fsSL https://ollama.com/install.sh | sh`
- Run Mistral: `ollama run mistral`
