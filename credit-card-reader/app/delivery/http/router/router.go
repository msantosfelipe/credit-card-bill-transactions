package router

import (
	"github.com/gin-gonic/gin"
	"github.com/msantosfelipe/credit-card-reader/app/delivery/http/handlers"
	"github.com/msantosfelipe/credit-card-reader/config"
	"github.com/msantosfelipe/credit-card-reader/domain"
)

func InitHttpRouters(
	us domain.BillTransactionsUsecase,
) {
	engine := gin.New()
	apiRouter := engine.Group(config.ENV.ApiBasePath)

	handlers.NewHandler(apiRouter, us)

	engine.Run(":" + config.ENV.ApiPort)
}
