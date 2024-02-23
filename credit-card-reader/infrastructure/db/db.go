package db

import (
	"context"

	"github.com/msantosfelipe/credit-card-reader/config"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func InitDb(ctx context.Context) *mongo.Client {
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(config.ENV.DbUri))
	if err != nil {
		panic("failed to connect do database")
	}

	return client
}
