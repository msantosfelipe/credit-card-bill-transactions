package usecase

import (
	"context"
	"math"
	"time"

	"github.com/msantosfelipe/credit-card-reader/domain"
)

type usecase struct {
	repository domain.BillTransactionsRepository
}

func NewUsecase(repository domain.BillTransactionsRepository) domain.BillTransactionsUsecase {
	return &usecase{repository: repository}
}

func (us *usecase) GetAllBills(banks []string) ([]domain.Bills, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	billsAmounts := []domain.Bills{}
	for _, bank := range banks {
		bills, err := us.repository.QueryAllBills(ctx, bank)
		if err != nil {
			return nil, err
		}

		billsAmounts = append(billsAmounts, domain.Bills{
			Bank:  bank,
			Bills: bills,
		})
	}

	return billsAmounts, nil
}

func (us *usecase) GetRecentBill(bank string) (*domain.Bill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	return us.repository.QueryRecentBill(ctx, bank)
}

func (us *usecase) GetInstallmentTransactions(bank string) (*domain.Installment, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	recentBill, err := us.repository.QueryRecentBill(ctx, bank)
	if err != nil {
		return nil, err
	}

	installments := domain.Installment{
		FileDate: recentBill.FileDate,
	}
	amount := float64(0)
	for _, i := range recentBill.Data {
		if isInstallment(i, bank) {
			installments.Data = append(installments.Data, i)
			amount = addWithPrecision(amount, i.AmountBRL)
		}
	}

	installments.Amount = amount
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
			categories.Data[idx].Amount = addWithPrecision(categories.Data[idx].Amount, i.AmountBRL)
		} else {
			categories.Data = append(categories.Data, domain.CategoryBill{
				Category:     i.Category,
				Amount:       float64(i.AmountBRL),
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
		if i.Description == "Estorno Tarifa" {
			continue
		}

		if i.Tag == "" {
			i.Tag = i.Category
		}

		exists, idx := isTagMapped(i.Tag, tags.Data)
		if exists {
			tags.Data[idx].Transactions = append(tags.Data[idx].Transactions, i)
			tags.Data[idx].Amount = addWithPrecision(tags.Data[idx].Amount, i.AmountBRL)

		} else {
			tags.Data = append(tags.Data, domain.CategoryBill{
				Tag:          i.Tag,
				Amount:       float64(i.AmountBRL),
				Transactions: []domain.Transaction{i},
			})
		}
	}

	return &tags, err
}

func (us *usecase) GetReportByTag(bank string) ([]domain.ReportByTag, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	bills, err := us.repository.QueryAllBills(ctx, bank)
	if err != nil {
		return nil, err
	}

	var report []domain.ReportByTag
	for _, b := range bills {
		for _, t := range b.Data {
			if t.Category == "-" {
				continue
			}

			if t.Tag == "" {
				t.Tag = t.Category
			}

			exists, idx := isTagMappedInReport(t.Tag, report)
			if exists {
				monthExists, monthIdx := isMonthMappedInReport(b.FileDate, report[idx].Report)
				if monthExists {
					report[idx].Report[monthIdx].Amount = addWithPrecision(report[idx].Report[monthIdx].Amount, t.AmountBRL)
				} else {
					report[idx].Report = append(report[idx].Report, domain.Report{
						FileDate: b.FileDate,
						Amount:   t.AmountBRL,
					})
				}

			} else {
				report = append(report, domain.ReportByTag{
					Tag: t.Tag,
					Report: []domain.Report{
						{
							FileDate: b.FileDate,
							Amount:   t.AmountBRL,
						},
					},
				})
			}
		}
	}

	return report, err
}

func isMonthMappedInReport(fileDate string, report []domain.Report) (bool, int) {
	for idx, i := range report {
		if i.FileDate == fileDate {
			return true, idx
		}
	}
	return false, 0
}

func isTagMappedInReport(tag string, data []domain.ReportByTag) (bool, int) {
	for idx, i := range data {
		if i.Tag == tag {
			return true, idx
		}
	}
	return false, 0
}

func categoryExists(category string, data []domain.CategoryBill) (bool, int) {
	for idx, i := range data {
		if i.Category == category {
			return true, idx
		}
	}
	return false, 0
}

func isTagMapped(tag string, data []domain.CategoryBill) (bool, int) {
	for idx, i := range data {
		if i.Tag == tag {
			return true, idx
		}
	}
	return false, 0
}

func isInstallment(i domain.Transaction, bank string) bool {
	if bank == "c6" {
		return i.Installment != "Única" && i.Tag != "Subscriptions" && i.Description != "Anuidade Diferenciada"
	} else {
		return i.Installment != "-"
	}
}

func addWithPrecision(a, b float64) float64 {
	result := a + b
	roundedResult := math.Round(result*100) / 100
	return roundedResult
}
