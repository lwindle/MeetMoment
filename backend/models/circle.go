package models

import (
	"time"

	"gorm.io/gorm"
)

// Circle 社交圈子模型
type Circle struct {
	ID          uint           `json:"id" gorm:"primaryKey"`
	Name        string         `json:"name" gorm:"not null"`
	Description string         `json:"description" gorm:"type:text"`
	Category    string         `json:"category" gorm:"not null"` // interest, location, profession
	CoverImage  string         `json:"cover_image"`
	IsPublic    bool           `json:"is_public" gorm:"default:true"`
	MemberCount int            `json:"member_count" gorm:"default:0"`
	PostCount   int            `json:"post_count" gorm:"default:0"`
	Tags        string         `json:"tags" gorm:"type:json"` // JSON数组存储标签
	CreatedAt   time.Time      `json:"created_at"`
	UpdatedAt   time.Time      `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Members []CircleMember `json:"members" gorm:"foreignKey:CircleID"`
	Posts   []CirclePost   `json:"posts" gorm:"foreignKey:CircleID"`
}

// CircleMember 圈子成员模型
type CircleMember struct {
	ID       uint           `json:"id" gorm:"primaryKey"`
	CircleID uint           `json:"circle_id" gorm:"not null;index"`
	UserID   uint           `json:"user_id" gorm:"not null;index"`
	Role     string         `json:"role" gorm:"default:member"` // owner, admin, member
	JoinedAt time.Time      `json:"joined_at"`
	CreatedAt time.Time     `json:"created_at"`
	UpdatedAt time.Time     `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Circle Circle `json:"-" gorm:"foreignKey:CircleID"`
	User   User   `json:"user" gorm:"foreignKey:UserID"`
}

// CirclePost 圈子动态模型
type CirclePost struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	CircleID  uint           `json:"circle_id" gorm:"not null;index"`
	UserID    uint           `json:"user_id" gorm:"not null;index"`
	Content   string         `json:"content" gorm:"type:text;not null"`
	Images    string         `json:"images" gorm:"type:json"`    // JSON数组存储图片URL
	LikeCount int            `json:"like_count" gorm:"default:0"`
	CommentCount int         `json:"comment_count" gorm:"default:0"`
	IsFromAI  bool           `json:"is_from_ai" gorm:"default:false"` // 是否AI生成
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Circle   Circle        `json:"-" gorm:"foreignKey:CircleID"`
	User     User          `json:"author" gorm:"foreignKey:UserID"`
	Comments []PostComment `json:"comments" gorm:"foreignKey:PostID"`
	Likes    []PostLike    `json:"likes" gorm:"foreignKey:PostID"`
}

// PostComment 动态评论模型
type PostComment struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	PostID    uint           `json:"post_id" gorm:"not null;index"`
	UserID    uint           `json:"user_id" gorm:"not null;index"`
	Content   string         `json:"content" gorm:"type:text;not null"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Post CirclePost `json:"-" gorm:"foreignKey:PostID"`
	User User       `json:"author" gorm:"foreignKey:UserID"`
}

// PostLike 动态点赞模型
type PostLike struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	PostID    uint           `json:"post_id" gorm:"not null;index"`
	UserID    uint           `json:"user_id" gorm:"not null;index"`
	CreatedAt time.Time      `json:"created_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Post CirclePost `json:"-" gorm:"foreignKey:PostID"`
	User User       `json:"-" gorm:"foreignKey:UserID"`
}

// CircleResponse 圈子响应结构
type CircleResponse struct {
	ID          uint        `json:"id"`
	Name        string      `json:"name"`
	Description string      `json:"description"`
	Category    string      `json:"category"`
	CoverImage  string      `json:"cover_image"`
	IsPublic    bool        `json:"is_public"`
	MemberCount int         `json:"member_count"`
	PostCount   int         `json:"post_count"`
	Tags        []string    `json:"tags"`
	IsJoined    bool        `json:"is_joined"`
	RecentPosts []PostResponse `json:"recent_posts,omitempty"`
	CreatedAt   time.Time   `json:"created_at"`
}

// PostResponse 动态响应结构
type PostResponse struct {
	ID           uint        `json:"id"`
	CircleID     uint        `json:"circle_id"`
	Content      string      `json:"content"`
	Images       []string    `json:"images"`
	LikeCount    int         `json:"like_count"`
	CommentCount int         `json:"comment_count"`
	IsFromAI     bool        `json:"is_from_ai"`
	Author       UserInfo    `json:"author"`
	IsLiked      bool        `json:"is_liked"`
	Comments     []CommentResponse `json:"comments,omitempty"`
	CreatedAt    time.Time   `json:"created_at"`
}

// CommentResponse 评论响应结构
type CommentResponse struct {
	ID        uint      `json:"id"`
	Content   string    `json:"content"`
	Author    UserInfo  `json:"author"`
	CreatedAt time.Time `json:"created_at"`
}

// ToCircleResponse 转换为CircleResponse
func (c *Circle) ToCircleResponse(isJoined bool, recentPosts []PostResponse) CircleResponse {
	var tags []string
	// 这里应该解析JSON字符串到string数组，简化处理
	return CircleResponse{
		ID:          c.ID,
		Name:        c.Name,
		Description: c.Description,
		Category:    c.Category,
		CoverImage:  c.CoverImage,
		IsPublic:    c.IsPublic,
		MemberCount: c.MemberCount,
		PostCount:   c.PostCount,
		Tags:        tags,
		IsJoined:    isJoined,
		RecentPosts: recentPosts,
		CreatedAt:   c.CreatedAt,
	}
}

// ToPostResponse 转换为PostResponse
func (p *CirclePost) ToPostResponse(isLiked bool, comments []CommentResponse) PostResponse {
	var images []string
	// 这里应该解析JSON字符串到string数组，简化处理
	
	return PostResponse{
		ID:           p.ID,
		CircleID:     p.CircleID,
		Content:      p.Content,
		Images:       images,
		LikeCount:    p.LikeCount,
		CommentCount: p.CommentCount,
		IsFromAI:     p.IsFromAI,
		Author: UserInfo{
			ID:       p.User.ID,
			Nickname: p.User.Nickname,
			Avatar:   p.User.Avatar,
			IsOnline: p.User.IsOnline,
		},
		IsLiked:   isLiked,
		Comments:  comments,
		CreatedAt: p.CreatedAt,
	}
}

// ToCommentResponse 转换为CommentResponse
func (c *PostComment) ToCommentResponse() CommentResponse {
	return CommentResponse{
		ID:      c.ID,
		Content: c.Content,
		Author: UserInfo{
			ID:       c.User.ID,
			Nickname: c.User.Nickname,
			Avatar:   c.User.Avatar,
			IsOnline: c.User.IsOnline,
		},
		CreatedAt: c.CreatedAt,
	}
} 