package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/msantosfelipe/credit-card-reader/domain"
)

type handler struct {
	us domain.BillTransactionsUsecase
}

func NewHandler(router *gin.RouterGroup, us domain.BillTransactionsUsecase) {
	handler := handler{
		us: us,
	}

	router.GET("/installments", handler.getInstallmentTransactions)
}

func (handler *handler) getInstallmentTransactions(ctx *gin.Context) {
	transactions, err := handler.us.GetInstallmentTransactions()
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, transactions)
}
