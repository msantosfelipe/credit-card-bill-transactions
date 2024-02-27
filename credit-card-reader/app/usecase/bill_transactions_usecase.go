package usecase

import (
	"context"
	"time"

	"github.com/msantosfelipe/credit-card-reader/domain"
)

type usecase struct {
	repository domain.BillTransactionsRepository
}

func NewUsecase(repository domain.BillTransactionsRepository) domain.BillTransactionsUsecase {
	return &usecase{repository: repository}
}

func (us *usecase) GetRecentBill(bank string) (*domain.Bill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	return us.repository.QueryRecentBill(ctx, bank)
}

func (us *usecase) GetInstallmentTransactions(bank string) (*domain.Bill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	recentBill, err := us.repository.QueryRecentBill(ctx, bank)
	if err != nil {
		return nil, err
	}

	installments := domain.Bill{
		FileDate: recentBill.FileDate,
	}
	for _, i := range recentBill.Data {
		if i.Installment != "Única" {
			installments.Data = append(installments.Data, i)
		}
	}

	return &installments, nil
}

func (us *usecase) GetTransactionsByCategory(bank string) (*domain.CategoriesBill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	recentBill, err := us.repository.QueryRecentBill(ctx, bank)
	if err != nil {
		return nil, err
	}

	categories := domain.CategoriesBill{
		FileDate: recentBill.FileDate,
	}
	for _, i := range recentBill.Data {
		exists, idx := categoryExists(i.Category, categories.Data)
		if exists {
			categories.Data[idx].Transactions = append(categories.Data[idx].Transactions, i)
			categories.Data[idx].Amount += float32(i.AmountBRL)
		} else {
			categories.Data = append(categories.Data, domain.CategoryBill{
				Category:     i.Category,
				Amount:       float32(i.AmountBRL),
				Transactions: []domain.Transaction{i},
			})
		}
	}

	return &categories, err
}

func (us *usecase) GetTransactionsByTag(bank string) (*domain.CategoriesBill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	recentBill, err := us.repository.QueryRecentBill(ctx, bank)
	if err != nil {
		return nil, err
	}

	tags := domain.CategoriesBill{
		FileDate: recentBill.FileDate,
	}
	for _, i := range recentBill.Data {
		exists, idx := tagExists(i.Tag, tags.Data)
		if exists {
			tags.Data[idx].Transactions = append(tags.Data[idx].Transactions, i)
			tags.Data[idx].Amount += float32(i.AmountBRL)
		} else {
			tags.Data = append(tags.Data, domain.CategoryBill{
				Tag:          i.Tag,
				Amount:       float32(i.AmountBRL),
				Transactions: []domain.Transaction{i},
			})
		}
	}

	return &tags, err
}

func categoryExists(category string, data []domain.CategoryBill) (bool, int) {
	for idx, i := range data {
		if i.Category == category {
			return true, idx
		}
	}
	return false, 0
}

func tagExists(tag string, data []domain.CategoryBill) (bool, int) {
	for idx, i := range data {
		if i.Tag == tag {
			return true, idx
		}
	}
	return false, 0
}
