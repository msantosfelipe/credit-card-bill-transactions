package domain

import (
	"context"
)

// Structs definitions

type Bill struct {
	FileDate string        `json:"month" bson:"file_date,omitempty"`
	Data     []Transaction `json:"data" bson:"data,omitempty"`
}

type Installment struct {
	FileDate string        `json:"month" bson:"file_date,omitempty"`
	Amount   float64       `json:"amount"`
	Data     []Transaction `json:"data" bson:"data,omitempty"`
}

type Transaction struct {
	PurchaseDate string  `json:"purchase_date,omitempty" bson:"Data de Compra,omitempty"`
	Cardholder   string  `json:"cardholder,omitempty" bson:"Nome no Cartão,omitempty"`
	CardDigits   int     `json:"card_digits,omitempty" bson:"Final do Cartão,omitempty"`
	Category     string  `json:"category,omitempty" bson:"Categoria,omitempty"`
	Tag          string  `json:"tag,omitempty" bson:"tag,omitempty"`
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
	Category     string        `json:"category,omitempty"`
	Tag          string        `json:"tag,omitempty"`
	Amount       float64       `json:"amount"`
	Transactions []Transaction `json:"transactions"`
}

type ReportByTag struct {
	Tag    string   `json:"tag"`
	Report []Report `json:"report"`
}

type Report struct {
	FileDate string  `json:"date"`
	Amount   float64 `json:"amount"`
}

// Usecase definitions
type BillTransactionsUsecase interface {
	GetRecentBill(bank string) (*Bill, error)
	GetInstallmentTransactions(bank string) (*Installment, error)
	GetTransactionsByCategory(bank string) (*CategoriesBill, error)
	GetTransactionsByTag(bank string) (*CategoriesBill, error)
	GetReportByTag(bank string) ([]ReportByTag, error)
}

// Repository definitions
type BillTransactionsRepository interface {
	QueryRecentBill(ctx context.Context, bank string, returnPayment bool) (*Bill, error)
	QueryAllBills(ctx context.Context, bank string) ([]Bill, error)
}
