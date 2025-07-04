package config

import (
	"log"
	"time"

	"github.com/Netflix/go-env"
	"github.com/subosito/gotenv"
)

type Environment struct {
	ApiPort     string `env:"API_PORT"`
	ApiBasePath string `env:"API_BASE_PATH"`
	DbUri       string `env:"DB_URI"`
	DbName      string `env:"DB_NAME"`
}

// ENV - output variable
var ENV Environment

func init() {
	gotenv.Load() // load .env file (if exists)
	if _, err := env.UnmarshalFromEnviron(&ENV); err != nil {
		log.Fatal("Fatal error unmarshalling environment config: ", err)
	}
}

func GetContextTimeout() time.Duration {
	return 5 * time.Second
}
