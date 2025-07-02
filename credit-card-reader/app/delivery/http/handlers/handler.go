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

	router.GET("/recent", handler.GetRecentBills)
	router.GET("/bills", handler.GetBillsByDate)
	router.GET("/installments", handler.getInstallmentTransactions)
}

func (handler *handler) GetRecentBills(ctx *gin.Context) {
	bills, err := handler.us.GetRecentBills()
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, bills)
}

func (handler *handler) GetBillsByDate(ctx *gin.Context) {
	dateInit := ctx.Query("dateInit")
	dateEnd := ctx.Query("dateEnd")

	if dateInit == "" || dateEnd == "" {
		ctx.JSON(http.StatusBadRequest, gin.H{"error": "dateInit and dateEnd query parameters are required (YYYY-mm format)"})
		return
	}

	bills, err := handler.us.GetBillsByDate(dateInit, dateEnd)
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, bills)
}

func (handler *handler) getInstallmentTransactions(ctx *gin.Context) {
	installments, err := handler.us.GetInstallmentTransactions()
	if err != nil {
		println(err.Error())
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query MongoDB"})
		return
	}
	ctx.JSON(http.StatusOK, installments)
}
