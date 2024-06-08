# Credit card bill updater

Read credit card bills and store data in MongoDB

Mongo URI: mongodb://localhost:27017/credit_card_reader_mongo

## Banks supported
- C6 (CSV files)

## Instalation
- Start database container, see ../README.md

- Activate venv `source credit-card-uploader-venv/bin/activate`

- Install dependencies `pip3 install -r requirements.txt`

- If you change tags, re-run `make upload` to update all data

- After using deactivate venv `deactivate`

## Run
- Upload new files `make upload`