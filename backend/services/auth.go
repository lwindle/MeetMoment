package services

import (
	"errors"
	"time"
	"meetmoment-backend/models"
	"meetmoment-backend/middleware"

	"github.com/golang-jwt/jwt/v5"
	"github.com/redis/go-redis/v9"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

type AuthService struct {
	db        *gorm.DB
	rdb       *redis.Client
	jwtSecret string
}

// RegisterRequest 注册请求结构
type RegisterRequest struct {
	Phone         string   `json:"phone" binding:"required"`
	Password      string   `json:"password" binding:"required,min=6"`
	Nickname      string   `json:"nickname" binding:"required"`
	Gender        int      `json:"gender"`
	Age           int      `json:"age" binding:"required,min=18,max=60"`
	City          string   `json:"city" binding:"required"`
	Occupation    string   `json:"occupation" binding:"required"`
	Bio           string   `json:"bio"`
	EmotionStatus string   `json:"emotion_status"`
	Interests     []string `json:"interests"`
}

// LoginRequest 登录请求结构
type LoginRequest struct {
	Phone    string `json:"phone" binding:"required"`
	Password string `json:"password" binding:"required"`
}

// AuthResponse 认证响应结构
type AuthResponse struct {
	Token      string             `json:"token"`
	RefreshToken string           `json:"refresh_token"`
	User       models.UserProfile `json:"user"`
	ExpiresIn  int64              `json:"expires_in"`
}

// NewAuthService 创建认证服务
func NewAuthService(db *gorm.DB, rdb *redis.Client, jwtSecret string) *AuthService {
	return &AuthService{
		db:        db,
		rdb:       rdb,
		jwtSecret: jwtSecret,
	}
}

// Register 用户注册
func (s *AuthService) Register(req *RegisterRequest) (*AuthResponse, error) {
	// 检查手机号是否已存在
	var existingUser models.User
	if err := s.db.Where("phone = ?", req.Phone).First(&existingUser).Error; err == nil {
		return nil, errors.New("手机号已被注册")
	}

	// 密码加密
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, errors.New("密码加密失败")
	}

	// 创建用户
	user := models.User{
		Phone:         req.Phone,
		Password:      string(hashedPassword),
		Nickname:      req.Nickname,
		Gender:        req.Gender,
		Age:           req.Age,
		City:          req.City,
		Occupation:    req.Occupation,
		Bio:           req.Bio,
		EmotionStatus: req.EmotionStatus,
		Verified:      false,
		IsOnline:      true,
		AIScore:       60, // 初始AI评分
		ProfileComplete: s.calculateProfileCompleteness(req),
	}

	if err := s.db.Create(&user).Error; err != nil {
		return nil, errors.New("用户创建失败")
	}

	// 创建用户兴趣标签
	for _, interest := range req.Interests {
		userInterest := models.UserInterest{
			UserID:      user.ID,
			Tag:         interest,
			AIGenerated: true,
		}
		s.db.Create(&userInterest)
	}

	// 生成JWT token
	token, refreshToken, expiresIn, err := s.generateTokens(user.ID, user.Phone, user.Nickname)
	if err != nil {
		return nil, errors.New("token生成失败")
	}

	// 加载完整用户信息
	s.db.Preload("Photos").Preload("Interests").First(&user, user.ID)

	return &AuthResponse{
		Token:        token,
		RefreshToken: refreshToken,
		User:         user.ToProfile(),
		ExpiresIn:    expiresIn,
	}, nil
}

// Login 用户登录
func (s *AuthService) Login(req *LoginRequest) (*AuthResponse, error) {
	var user models.User
	if err := s.db.Where("phone = ?", req.Phone).First(&user).Error; err != nil {
		return nil, errors.New("用户不存在")
	}

	// 验证密码
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		return nil, errors.New("密码错误")
	}

	// 更新在线状态
	now := time.Now()
	s.db.Model(&user).Updates(models.User{
		IsOnline:       true,
		LastActiveTime: &now,
	})

	// 生成JWT token
	token, refreshToken, expiresIn, err := s.generateTokens(user.ID, user.Phone, user.Nickname)
	if err != nil {
		return nil, errors.New("token生成失败")
	}

	// 加载完整用户信息
	s.db.Preload("Photos").Preload("Interests").First(&user, user.ID)

	return &AuthResponse{
		Token:        token,
		RefreshToken: refreshToken,
		User:         user.ToProfile(),
		ExpiresIn:    expiresIn,
	}, nil
}

// RefreshToken 刷新token
func (s *AuthService) RefreshToken(refreshToken string) (*AuthResponse, error) {
	// 验证refresh token
	token, err := jwt.ParseWithClaims(refreshToken, &middleware.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(s.jwtSecret), nil
	})

	if err != nil || !token.Valid {
		return nil, errors.New("无效的refresh token")
	}

	claims, ok := token.Claims.(*middleware.JWTClaims)
	if !ok {
		return nil, errors.New("无效的token claims")
	}

	// 获取用户信息
	var user models.User
	if err := s.db.Preload("Photos").Preload("Interests").First(&user, claims.UserID).Error; err != nil {
		return nil, errors.New("用户不存在")
	}

	// 生成新的token
	newToken, newRefreshToken, expiresIn, err := s.generateTokens(user.ID, user.Phone, user.Nickname)
	if err != nil {
		return nil, errors.New("token生成失败")
	}

	return &AuthResponse{
		Token:        newToken,
		RefreshToken: newRefreshToken,
		User:         user.ToProfile(),
		ExpiresIn:    expiresIn,
	}, nil
}

// Logout 用户登出
func (s *AuthService) Logout(userID uint) error {
	// 更新用户离线状态
	now := time.Now()
	return s.db.Model(&models.User{}).Where("id = ?", userID).Updates(models.User{
		IsOnline:       false,
		LastActiveTime: &now,
	}).Error
}

// generateTokens 生成访问token和刷新token
func (s *AuthService) generateTokens(userID uint, phone, nickname string) (string, string, int64, error) {
	now := time.Now()
	expiresIn := int64(24 * 3600) // 24小时

	// 访问token (1小时有效)
	accessClaims := middleware.JWTClaims{
		UserID:   userID,
		Phone:    phone,
		Nickname: nickname,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(now.Add(time.Hour)),
			IssuedAt:  jwt.NewNumericDate(now),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	accessToken := jwt.NewWithClaims(jwt.SigningMethodHS256, accessClaims)
	accessTokenString, err := accessToken.SignedString([]byte(s.jwtSecret))
	if err != nil {
		return "", "", 0, err
	}

	// 刷新token (24小时有效)
	refreshClaims := middleware.JWTClaims{
		UserID:   userID,
		Phone:    phone,
		Nickname: nickname,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(now.Add(24 * time.Hour)),
			IssuedAt:  jwt.NewNumericDate(now),
			NotBefore: jwt.NewNumericDate(now),
		},
	}

	refreshToken := jwt.NewWithClaims(jwt.SigningMethodHS256, refreshClaims)
	refreshTokenString, err := refreshToken.SignedString([]byte(s.jwtSecret))
	if err != nil {
		return "", "", 0, err
	}

	return accessTokenString, refreshTokenString, expiresIn, nil
}

// calculateProfileCompleteness 计算资料完整度
func (s *AuthService) calculateProfileCompleteness(req *RegisterRequest) float64 {
	completeness := 0.0
	total := 8.0

	if req.Phone != "" {
		completeness += 1.0
	}
	if req.Nickname != "" {
		completeness += 1.0
	}
	if req.Age > 0 {
		completeness += 1.0
	}
	if req.City != "" {
		completeness += 1.0
	}
	if req.Occupation != "" {
		completeness += 1.0
	}
	if req.Bio != "" {
		completeness += 1.0
	}
	if req.EmotionStatus != "" {
		completeness += 1.0
	}
	if len(req.Interests) > 0 {
		completeness += 1.0
	}

	return (completeness / total) * 100
} 