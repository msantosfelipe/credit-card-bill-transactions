package domain

import (
	"context"
)

// Structs definitions

type Bill struct {
	FileDate string        `json:"file_date" bson:"file_date"`
	Bank     string        `json:"bank" bson:"bank"`
	Data     []Transaction `json:"data" bson:"data"`
}

type Transaction struct {
	PurchaseDate string  `json:"purchase_date" bson:"purchase_date"`
	CardHolder   string  `json:"card_holder" bson:"card_holder"`
	CardDigits   string  `json:"card_digits" bson:"card_digits"`
	Description  string  `json:"description" bson:"description"`
	Amount       float64 `json:"amount" bson:"amount"`
	Installment  string  `json:"installment" bson:"installment"`
	Category     string  `json:"category" bson:"category"`
}

type Installment struct {
	FileDate string                   `json:"file_date" bson:"file_date"`
	Bank     string                   `json:"bank" bson:"bank"`
	Data     []InstallmentTransaction `json:"data" bson:"data"`
}

type InstallmentTransaction struct {
	Description string  `json:"description" bson:"description"`
	Amount      float64 `json:"amount" bson:"amount"`
	Installment string  `json:"installment" bson:"installment"`
	Category    string  `json:"category" bson:"category"`
}

type CategoryGroup struct {
	FileDate string                `json:"file_date"`
	Category string                `json:"category"`
	Data     []CategoryTransaction `json:"data"`
}

type CategoryTransaction struct {
	Bank        string  `json:"bank"`
	Description string  `json:"description"`
	Amount      float64 `json:"amount"`
	Installment string  `json:"installment"`
}

// Usecase definitions

type BillTransactionsUsecase interface {
	GetRecentBills() ([]Bill, error)
	GetBillsByDate(dateInit, dateEnd string) ([]Bill, error)
	GetBillsByDateAndCategory(dateInit, dateEnd string) ([]CategoryGroup, error)
	GetInstallmentTransactions() ([]Installment, error)
}

// Repository definitions

type BillTransactionsRepository interface {
	QueryBillsByDate(ctx context.Context, dateInit, dateEnd string) ([]Bill, error)
	QueryLatestBillsByBank(ctx context.Context) ([]Bill, error)
}
