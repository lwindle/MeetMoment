package services

import (
	"errors"
	"meetmoment-backend/models"

	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

type UserService struct {
	db  *gorm.DB
	rdb *redis.Client
}

// NewUserService 创建用户服务
func NewUserService(db *gorm.DB, rdb *redis.Client) *UserService {
	return &UserService{
		db:  db,
		rdb: rdb,
	}
}

// GetProfile 获取用户资料
func (s *UserService) GetProfile(userID uint) (*models.UserProfile, error) {
	var user models.User
	if err := s.db.Preload("Photos").Preload("Interests").First(&user, userID).Error; err != nil {
		return nil, errors.New("用户不存在")
	}

	profile := user.ToProfile()
	return &profile, nil
}

// UpdateProfile 更新用户资料
func (s *UserService) UpdateProfile(userID uint, updates map[string]interface{}) error {
	return s.db.Model(&models.User{}).Where("id = ?", userID).Updates(updates).Error
}

// GetRecommendations 获取推荐用户
func (s *UserService) GetRecommendations(userID uint, limit int) ([]models.UserProfile, error) {
	var users []models.User
	
	// 简单的推荐逻辑：排除自己和已匹配的用户
	if err := s.db.Preload("Photos").Preload("Interests").
		Where("id != ?", userID).
		Limit(limit).
		Find(&users).Error; err != nil {
		return nil, err
	}

	var profiles []models.UserProfile
	for _, user := range users {
		profiles = append(profiles, user.ToProfile())
	}

	return profiles, nil
} 