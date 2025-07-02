# Etapa de build
FROM golang:1.21.6 AS builder
WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . ./
RUN go build -o app

FROM debian:bookworm-slim
WORKDIR /app

COPY --from=builder /app/app .

EXPOSE 8081
CMD ["./app"]
