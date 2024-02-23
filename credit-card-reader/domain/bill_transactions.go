package domain

import "github.com/gin-gonic/gin"

// Structs definitions

type Bill struct {
	FileDate string        `json:"month" bson:"file_date,omitempty"`
	Data     []Transaction `json:"data" bson:"data,omitempty"`
}

type Transaction struct {
	PurchaseDate string  `json:"purchase_date,omitempty" bson:"Data de Compra,omitempty"`
	Cardholder   string  `json:"cardholder,omitempty" bson:"Nome no Cartão,omitempty"`
	CardDigits   int     `json:"card_digits,omitempty" bson:"Final do Cartão,omitempty"`
	Category     string  `json:"category,omitempty" bson:"Categoria,omitempty"`
	Description  string  `json:"description,omitempty" bson:"Descrição,omitempty"`
	Installment  string  `json:"installment,omitempty" bson:"Parcela,omitempty"`
	AmountUSD    float64 `json:"amount_usd,omitempty" bson:"Valor (em US$),omitempty"`
	ExchangeRate float64 `json:"exchange_rate,omitempty" bson:"Cotação (em R$),omitempty"`
	AmountBRL    float64 `json:"amount_brl,omitempty" bson:"Valor (em R$),omitempty"`
}

type CategoriesBill struct {
	FileDate string         `json:"month"`
	Data     []CategoryBill `json:"data"`
}

type CategoryBill struct {
	Category     string        `json:"category"`
	Amount       float32       `json:"amount"`
	Transactions []Transaction `json:"transactions"`
}

// Usecase definitions
type BillTransactionsUsecase interface {
	GetRecentBill(ctx *gin.Context, bank string) (*Bill, error)
	GetInstallmentTransactions(ctx *gin.Context, bank string) (*Bill, error)
	GetTransactionsByCategory(ctx *gin.Context, bank string) (*CategoriesBill, error)
}

// Repository definitions
type BillTransactionsRepository interface {
	QueryRecentBill(ctx *gin.Context, bank string) (*Bill, error)
}
