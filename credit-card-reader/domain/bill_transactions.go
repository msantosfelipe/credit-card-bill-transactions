package domain

import (
	"context"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Structs definitions

type Bill struct {
	ID       primitive.ObjectID `bson:"_id"`
	FileDate string             `bson:"file_date"`
	Bank     string             `bson:"bank"`
	Data     []Transaction      `bson:"data"`
}

type Transaction struct {
	PurchaseDate string  `bson:"purchase_date"`
	CardHolder   string  `bson:"card_holder"`
	CardDigits   string  `bson:"card_digits"`
	Description  string  `bson:"description"`
	Amount       float64 `bson:"amount"`
	Installment  string  `bson:"installment"`
	Category     string  `bson:"category"`
}

type Installment struct {
	FileDate string                   `bson:"file_date"`
	Bank     string                   `bson:"bank"`
	Data     []InstallmentTransaction `bson:"data"`
}

type InstallmentTransaction struct {
	Description string  `bson:"description"`
	Amount      float64 `bson:"amount"`
	Installment string  `bson:"installment"`
	Category    string  `bson:"category"`
}

// Usecase definitions

type BillTransactionsUsecase interface {
	GetInstallmentTransactions() ([]Installment, error)
}

// Repository definitions

type BillTransactionsRepository interface {
	QueryLatestBillsByBank(ctx context.Context) ([]Bill, error)
}
