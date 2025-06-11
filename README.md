# Credit card bill reader/uploader

- Work in progress...

### Uploader
Subdirectory ./credit-card-uploader

Python script to upload data

### Reader
Subdirectory ./credit-card-reader

Golang service to read data

### Viewer
Subdirectory ./credit-card-viewer

React + ChartsJS

Refs:
https://blog.logrocket.com/using-chart-js-react/

## How to run
- Start database `make up`
- Upload data to database following [this instructions](https://github.com/msantosfelipe/credit-card-bill-transactions/tree/main/credit-card-uploader#readme)
- Start API running `make reader`
- Start Web application with `make viewer`
