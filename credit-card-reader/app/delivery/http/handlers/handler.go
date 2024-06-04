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
	router.GET("/bills", handler.getAllBills)
	router.GET("/installments", handler.getInstallmentTransactions)
	router.GET("/categories", handler.getTransactionsByCategory)
	router.GET("/tags", handler.getTransactionsByTag)
	router.GET("/report/tag", handler.getReportByTag)
}

func (handler *handler) getRecentBill(ctx *gin.Context) {
	// TODO add month parameter

	recentBill, err := handler.us.GetRecentBill("c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, recentBill)
}

func (handler *handler) getAllBills(ctx *gin.Context) {
	bills, err := handler.us.GetAllBills([]string{"c6"})
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, bills)
}

func (handler *handler) getInstallmentTransactions(ctx *gin.Context) {
	transactions, err := handler.us.GetInstallmentTransactions("c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, transactions)
}

func (handler *handler) getTransactionsByCategory(ctx *gin.Context) {
	categories, err := handler.us.GetTransactionsByCategory("c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, categories)
}

func (handler *handler) getTransactionsByTag(ctx *gin.Context) {
	categories, err := handler.us.GetTransactionsByTag("c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, categories)
}

func (handler *handler) getReportByTag(ctx *gin.Context) {
	reports, err := handler.us.GetReportByTag("c6")
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, reports)
}
