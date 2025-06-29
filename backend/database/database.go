package database

import (
	"context"
	"log"

	"github.com/redis/go-redis/v9"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// InitPostgreSQL 初始化PostgreSQL数据库连接 (Supabase)
func InitPostgreSQL(databaseURL string) (*gorm.DB, error) {
	db, err := gorm.Open(postgres.Open(databaseURL), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Warn),
	})
	if err != nil {
		return nil, err
	}

	// 注释掉自动迁移，因为表已经通过SQL脚本手动创建
	// err = db.AutoMigrate(
	//	&models.User{},
	//	&models.UserPhoto{},
	//	&models.UserInterest{},
	//	&models.Match{},
	//	&models.Conversation{},
	//	&models.Message{},
	//	&models.Circle{},
	//	&models.CircleMember{},
	//	&models.CirclePost{},
	//	&models.AIConversation{},
	// )
	// if err != nil {
	//	return nil, err
	// }

	log.Println("Supabase PostgreSQL connection established and migrated successfully")
	return db, nil
}

// InitRedis 初始化Redis连接
func InitRedis(redisURL string) *redis.Client {
	opt, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Printf("Warning: Failed to parse Redis URL: %v", err)
		return nil
	}

	rdb := redis.NewClient(opt)

	// 测试连接
	ctx := context.Background()
	_, err = rdb.Ping(ctx).Result()
	if err != nil {
		log.Printf("Warning: Failed to connect to Redis: %v", err)
		return nil
	}

	log.Println("Redis connection established successfully")
	return rdb
} 