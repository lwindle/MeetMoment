package models

import (
	"time"

	"gorm.io/gorm"
)

// User 用户模型
type User struct {
	ID               uint           `json:"id" gorm:"primaryKey"`
	Phone            string         `json:"phone" gorm:"uniqueIndex;not null"`
	Password         string         `json:"-" gorm:"not null"`          // 不在JSON中返回密码
	Nickname         string         `json:"nickname" gorm:"not null"`
	Gender           int            `json:"gender"`                     // 0: 男, 1: 女
	Age              int            `json:"age"`
	City             string         `json:"city"`
	Occupation       string         `json:"occupation"`
	Bio              string         `json:"bio" gorm:"type:text"`
	EmotionStatus    string         `json:"emotion_status"`             // single, dating, complicated
	Avatar           string         `json:"avatar"`
	Verified         bool           `json:"verified" gorm:"default:false"`
	IsOnline         bool           `json:"is_online" gorm:"default:false"`
	LastActiveTime   *time.Time     `json:"last_active_time"`
	AIScore          int            `json:"ai_score" gorm:"default:0"`  // AI评分
	ProfileComplete  float64        `json:"profile_complete" gorm:"default:0"` // 资料完整度
	CreatedAt        time.Time      `json:"created_at"`
	UpdatedAt        time.Time      `json:"updated_at"`
	DeletedAt        gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Photos           []UserPhoto    `json:"photos" gorm:"foreignKey:UserID"`
	Interests        []UserInterest `json:"interests" gorm:"foreignKey:UserID"`
	SentMatches      []Match        `json:"sent_matches" gorm:"foreignKey:UserID"`
	ReceivedMatches  []Match        `json:"received_matches" gorm:"foreignKey:TargetUserID"`
	Conversations    []Conversation `json:"conversations" gorm:"many2many:conversation_participants;"`
	CircleMemberships []CircleMember `json:"circle_memberships" gorm:"foreignKey:UserID"`
}

// UserPhoto 用户照片模型
type UserPhoto struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	UserID    uint           `json:"user_id" gorm:"not null;index"`
	URL       string         `json:"url" gorm:"not null"`
	IsPrimary bool           `json:"is_primary" gorm:"default:false"`
	Order     int            `json:"order" gorm:"default:0"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	User User `json:"-" gorm:"foreignKey:UserID"`
}

// UserInterest 用户兴趣标签模型
type UserInterest struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	UserID    uint           `json:"user_id" gorm:"not null;index"`
	Tag       string         `json:"tag" gorm:"not null"`
	AIGenerated bool         `json:"ai_generated" gorm:"default:false"` // 是否AI生成
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	User User `json:"-" gorm:"foreignKey:UserID"`
}

// Match 匹配记录模型
type Match struct {
	ID           uint           `json:"id" gorm:"primaryKey"`
	UserID       uint           `json:"user_id" gorm:"not null;index"`
	TargetUserID uint           `json:"target_user_id" gorm:"not null;index"`
	Action       string         `json:"action" gorm:"not null"` // like, pass, super_like
	IsMatched    bool           `json:"is_matched" gorm:"default:false"`
	CreatedAt    time.Time      `json:"created_at"`
	UpdatedAt    time.Time      `json:"updated_at"`
	DeletedAt    gorm.DeletedAt `json:"-" gorm:"index"`

	User       User `json:"user" gorm:"foreignKey:UserID"`
	TargetUser User `json:"target_user" gorm:"foreignKey:TargetUserID"`
}

// UserProfile 用户资料响应结构（用于API响应）
type UserProfile struct {
	ID            uint          `json:"id"`
	Nickname      string        `json:"nickname"`
	Gender        int           `json:"gender"`
	Age           int           `json:"age"`
	City          string        `json:"city"`
	Occupation    string        `json:"occupation"`
	Bio           string        `json:"bio"`
	EmotionStatus string        `json:"emotion_status"`
	Avatar        string        `json:"avatar"`
	Verified      bool          `json:"verified"`
	IsOnline      bool          `json:"is_online"`
	AIScore       int           `json:"ai_score"`
	ProfileComplete float64     `json:"profile_complete"`
	Photos        []UserPhoto   `json:"photos"`
	Interests     []UserInterest `json:"interests"`
	CreatedAt     time.Time     `json:"created_at"`
}

// ToProfile 转换为UserProfile
func (u *User) ToProfile() UserProfile {
	return UserProfile{
		ID:            u.ID,
		Nickname:      u.Nickname,
		Gender:        u.Gender,
		Age:           u.Age,
		City:          u.City,
		Occupation:    u.Occupation,
		Bio:           u.Bio,
		EmotionStatus: u.EmotionStatus,
		Avatar:        u.Avatar,
		Verified:      u.Verified,
		IsOnline:      u.IsOnline,
		AIScore:       u.AIScore,
		ProfileComplete: u.ProfileComplete,
		Photos:        u.Photos,
		Interests:     u.Interests,
		CreatedAt:     u.CreatedAt,
	}
} 