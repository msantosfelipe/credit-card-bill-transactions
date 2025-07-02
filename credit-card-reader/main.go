// main.go
package main

import (
	"context"
	"time"

	"github.com/msantosfelipe/credit-card-reader/internal/delivery/http"
	"github.com/msantosfelipe/credit-card-reader/internal/infrastructure/db"
	repository "github.com/msantosfelipe/credit-card-reader/internal/repository/db"
	"github.com/msantosfelipe/credit-card-reader/internal/usecase"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	dbClient := db.InitDb(ctx)
	defer dbClient.Disconnect(ctx)

	// init dependencies
	repo := repository.NewRepository(dbClient)
	us := usecase.NewUsecase(repo)

	http.InitHttpRouters(us)
}
