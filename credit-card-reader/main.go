// main.go
package main

import (
	"context"
	"time"

	"github.com/msantosfelipe/credit-card-reader/app/delivery/http/router"
	repository "github.com/msantosfelipe/credit-card-reader/app/repository/db"
	"github.com/msantosfelipe/credit-card-reader/app/usecase"
	"github.com/msantosfelipe/credit-card-reader/infrastructure/db"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	dbClient := db.InitDb(ctx)
	defer dbClient.Disconnect(ctx)

	// init dependencies
	repo := repository.NewRepository(dbClient)
	us := usecase.NewUsecase(repo)

	router.InitHttpRouters(us)
}
