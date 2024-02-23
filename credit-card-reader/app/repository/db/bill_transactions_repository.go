package db

import (
	"github.com/gin-gonic/gin"
	"github.com/msantosfelipe/credit-card-reader/config"
	"github.com/msantosfelipe/credit-card-reader/domain"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type repository struct {
	dbClient *mongo.Client
}

func NewRepository(dbClient *mongo.Client) domain.BillTransactionsRepository {
	return &repository{dbClient: dbClient}
}

func (repo *repository) getCollection(bank string) *mongo.Collection {
	return repo.dbClient.Database(config.ENV.DbName).Collection(bank)
}

func (repo *repository) QueryRecentBill(ctx *gin.Context, bank string) (*domain.Bill, error) {
	options := options.FindOne().SetSort(bson.D{{Key: "file_date", Value: -1}})

	var result domain.Bill
	err := repo.getCollection(bank).FindOne(ctx, bson.M{}, options).Decode(&result)
	if err != nil {
		return nil, err
	}

	return &result, nil
}
