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

	router.GET("/bill", handler.getRecentBill)
	router.GET("/installments", handler.getInstallmentTransactions)
	router.GET("/categories", handler.getTransactionsByCategory)
}

func (handler *handler) getRecentBill(ctx *gin.Context) {
	recentBill, err := handler.us.GetRecentBill(ctx, "c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, recentBill)
}

func (handler *handler) getInstallmentTransactions(ctx *gin.Context) {
	transactions, err := handler.us.GetInstallmentTransactions(ctx, "c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, transactions)
}

func (handler *handler) getTransactionsByCategory(ctx *gin.Context) {
	categories, err := handler.us.GetTransactionsByCategory(ctx, "c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, categories)
}
