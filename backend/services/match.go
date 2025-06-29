package services

import (
	"meetmoment-backend/models"

	"gorm.io/gorm"
)

type MatchService struct {
	db        *gorm.DB
	aiService *AIService
}

// NewMatchService 创建匹配服务
func NewMatchService(db *gorm.DB, aiService *AIService) *MatchService {
	return &MatchService{
		db:        db,
		aiService: aiService,
	}
}

// GetRecommendations 获取推荐用户
func (s *MatchService) GetRecommendations(userID uint, limit int) ([]models.UserProfile, error) {
	var users []models.User
	
	// 简单的推荐逻辑：排除自己和已操作的用户
	subQuery := s.db.Model(&models.Match{}).
		Select("target_user_id").
		Where("user_id = ?", userID)

	if err := s.db.Preload("Photos").Preload("Interests").
		Where("id != ? AND id NOT IN (?)", userID, subQuery).
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

// LikeUser 喜欢用户
func (s *MatchService) LikeUser(userID uint, targetUserID uint) (bool, error) {
	// 记录喜欢操作
	match := models.Match{
		UserID:       userID,
		TargetUserID: targetUserID,
		Action:       "like",
		IsMatched:    false,
	}

	if err := s.db.Create(&match).Error; err != nil {
		return false, err
	}

	// 检查是否互相喜欢
	var reverseMatch models.Match
	if err := s.db.Where("user_id = ? AND target_user_id = ? AND action = 'like'", 
		targetUserID, userID).First(&reverseMatch).Error; err == nil {
		// 互相喜欢，创建匹配
		s.db.Model(&match).Update("is_matched", true)
		s.db.Model(&reverseMatch).Update("is_matched", true)
		return true, nil
	}

	return false, nil
}

// PassUser 跳过用户
func (s *MatchService) PassUser(userID uint, targetUserID uint) error {
	match := models.Match{
		UserID:       userID,
		TargetUserID: targetUserID,
		Action:       "pass",
		IsMatched:    false,
	}

	return s.db.Create(&match).Error
}

// GetMatches 获取匹配列表
func (s *MatchService) GetMatches(userID uint) ([]models.UserProfile, error) {
	var users []models.User
	
	// 获取互相匹配的用户
	if err := s.db.Preload("Photos").Preload("Interests").
		Joins("JOIN matches ON users.id = matches.target_user_id").
		Where("matches.user_id = ? AND matches.is_matched = true", userID).
		Find(&users).Error; err != nil {
		return nil, err
	}

	var profiles []models.UserProfile
	for _, user := range users {
		profiles = append(profiles, user.ToProfile())
	}

	return profiles, nil
} 