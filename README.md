# Credit card bill reader/uploader

- Work in progress...

### Uploader
Subdirectory ./credit-card-uploader

Python script to upload data

### Reader
Subdirectory ./credit-card-reader

Golang service to read data

## How to run
- Build image: `cd ./credit-card-reader` and `make build-app`
- Start database `make up`
- Upload data to database following [this instructions](https://github.com/msantosfelipe/credit-card-bill-transactions/tree/main/credit-card-uploader#readme)
