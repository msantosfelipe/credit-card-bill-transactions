package router

import (
	"time"

	"github.com/gin-contrib/cors"
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

	apiRouter.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	handlers.NewHandler(apiRouter, us)

	engine.Run(":" + config.ENV.ApiPort)
}
