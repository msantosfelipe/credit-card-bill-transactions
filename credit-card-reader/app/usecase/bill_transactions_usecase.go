package usecase

import (
	"context"
	"time"

	"github.com/msantosfelipe/credit-card-reader/config"
	"github.com/msantosfelipe/credit-card-reader/domain"
)

type usecase struct {
	repository domain.BillTransactionsRepository
}

func NewUsecase(repository domain.BillTransactionsRepository) domain.BillTransactionsUsecase {
	return &usecase{repository: repository}
}

func (us *usecase) GetRecentBills() ([]domain.Bill, error) {
	ctx, cancel := context.WithTimeout(context.Background(), config.GetContextTimeout())
	defer cancel()

	latestBills, err := us.repository.QueryLatestBillsByBank(ctx)
	if err != nil {
		return nil, err
	}

	validBills := []domain.Bill{}
	for _, bill := range latestBills {
		if isWithinLast3Months(bill.FileDate) {
			validBills = append(validBills, bill)
		}
	}

	return validBills, nil
}

func (us *usecase) GetInstallmentTransactions() ([]domain.Installment, error) {
	ctx, cancel := context.WithTimeout(context.Background(), config.GetContextTimeout())
	defer cancel()

	latestBills, err := us.repository.QueryLatestBillsByBank(ctx)
	if err != nil {
		return nil, err
	}

	installments := []domain.Installment{}
	for _, bill := range latestBills {
		if !isWithinLast3Months(bill.FileDate) {
			continue
		}

		installmentTransaction := []domain.InstallmentTransaction{}
		for _, transaction := range bill.Data {
			if isInstallment(transaction) {
				installmentTransaction = append(installmentTransaction, domain.InstallmentTransaction{
					Description: transaction.Description,
					Amount:      transaction.Amount,
					Installment: transaction.Installment,
					Category:    transaction.Category,
				})
			}
		}

		if len(installmentTransaction) > 0 {
			installments = append(installments, domain.Installment{
				FileDate: bill.FileDate,
				Bank:     bill.Bank,
				Data:     installmentTransaction,
			})
		}
	}

	return installments, nil
}

func isInstallment(transaction domain.Transaction) bool {
	return transaction.Installment != "-"
}

func isWithinLast3Months(fileDate string) bool {
	parsedDate, err := time.Parse("2006-01", fileDate)
	if err != nil {
		return false
	}

	limitDate := time.Now().AddDate(0, -3, 0)
	return !parsedDate.Before(limitDate)
}
