package db

import (
	"context"
	"strings"

	"github.com/msantosfelipe/credit-card-reader/config"
	"github.com/msantosfelipe/credit-card-reader/domain"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const C6_PAYMENT = "Pagamento Efetuado"

type repository struct {
	dbClient *mongo.Client
}

func NewRepository(dbClient *mongo.Client) domain.BillTransactionsRepository {
	return &repository{dbClient: dbClient}
}

func (repo *repository) getCollection(bank string) *mongo.Collection {
	return repo.dbClient.Database(config.ENV.DbName).Collection(bank)
}

func (repo *repository) QueryRecentBill(ctx context.Context, bank string) (*domain.Bill, error) {
	sortOptions := options.FindOne().SetSort(bson.D{{Key: "file_date", Value: -1}})

	var result domain.Bill
	err := repo.getCollection(bank).FindOne(ctx, bson.M{}, sortOptions).Decode(&result)
	if err != nil {
		return nil, err
	}

	for i := 0; i < len(result.Data); i++ {
		if strings.TrimSpace(result.Data[i].Description) == C6_PAYMENT {
			result.Data = append(result.Data[:i], result.Data[i+1:]...)
			i--
		}
		result.TotalAmount += result.Data[i].AmountBRL
	}

	return &result, nil
}

func (repo *repository) QueryAllBills(ctx context.Context, bank string) ([]domain.Bill, error) {
	sortOptions := options.Find().SetSort(bson.D{{Key: "file_date", Value: -1}})

	cursor, err := repo.getCollection(bank).Find(ctx, bson.M{}, sortOptions)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var results []domain.Bill
	if err := cursor.All(ctx, &results); err != nil {
		return nil, err
	}

	return results, nil
}

func removePayment(result domain.Bill) *domain.Bill {
	for i := 0; i < len(result.Data); i++ {
		if strings.TrimSpace(result.Data[i].Description) == C6_PAYMENT {
			result.Data = append(result.Data[:i], result.Data[i+1:]...)
			i--
		}
	}
	return &result
}
