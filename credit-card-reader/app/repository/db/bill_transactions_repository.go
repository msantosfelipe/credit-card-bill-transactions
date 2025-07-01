package db

import (
	"context"

	"github.com/msantosfelipe/credit-card-reader/config"
	"github.com/msantosfelipe/credit-card-reader/domain"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

const bills_collection = "bills"

const C6_PAYMENT = "Pagamento Efetuado"
const C6_PAYMENT_INCLUDED = "Inclusao de Pagamento"

type repository struct {
	dbClient *mongo.Client
}

func NewRepository(dbClient *mongo.Client) domain.BillTransactionsRepository {
	return &repository{dbClient: dbClient}
}

func (repo *repository) getCollection(bank string) *mongo.Collection {
	return repo.dbClient.Database(config.ENV.DbName).Collection(bank)
}

func (repo *repository) QueryLatestBillsByBank(ctx context.Context) ([]domain.Bill, error) {
	collection := repo.getCollection(bills_collection)

	pipeline := mongo.Pipeline{
		{{Key: "$sort", Value: bson.D{{Key: "bank", Value: 1}, {Key: "file_date", Value: -1}}}},
		{{Key: "$group", Value: bson.D{
			{Key: "_id", Value: "$bank"},
			{Key: "latest", Value: bson.D{{Key: "$first", Value: "$$ROOT"}}},
		}}},
	}

	cursor, err := collection.Aggregate(ctx, pipeline)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var results []struct {
		Latest domain.Bill `bson:"latest"`
	}

	if err := cursor.All(ctx, &results); err != nil {
		return nil, err
	}

	bills := make([]domain.Bill, len(results))
	for i, r := range results {
		bills[i] = r.Latest
	}

	return bills, nil
}
