package models

import (
	"time"

	"gorm.io/gorm"
)

// Conversation 会话模型
type Conversation struct {
	ID               uint           `json:"id" gorm:"primaryKey"`
	Type             string         `json:"type" gorm:"not null"` // private, group, ai
	LastMessageID    *uint          `json:"last_message_id"`
	LastMessageTime  *time.Time     `json:"last_message_time"`
	CreatedAt        time.Time      `json:"created_at"`
	UpdatedAt        time.Time      `json:"updated_at"`
	DeletedAt        gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Messages     []Message `json:"messages" gorm:"foreignKey:ConversationID"`
	LastMessage  *Message  `json:"last_message" gorm:"foreignKey:LastMessageID"`
	Participants []User    `json:"participants" gorm:"many2many:conversation_participants;"`
}

// Message 消息模型
type Message struct {
	ID             uint           `json:"id" gorm:"primaryKey"`
	ConversationID uint           `json:"conversation_id" gorm:"not null;index"`
	SenderID       uint           `json:"sender_id" gorm:"not null;index"`
	Content        string         `json:"content" gorm:"type:text;not null"`
	MessageType    string         `json:"message_type" gorm:"not null"` // text, image, file, system
	IsFromAI       bool           `json:"is_from_ai" gorm:"default:false"`
	AIResponseTime *time.Duration `json:"ai_response_time"` // AI响应时间
	ReadBy         string         `json:"read_by" gorm:"type:json"`     // JSON数组，记录已读用户ID
	CreatedAt      time.Time      `json:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at"`
	DeletedAt      gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	Conversation Conversation `json:"-" gorm:"foreignKey:ConversationID"`
	Sender       User         `json:"sender" gorm:"foreignKey:SenderID"`
}

// AIConversation AI对话记录模型
type AIConversation struct {
	ID            uint           `json:"id" gorm:"primaryKey"`
	UserID        uint           `json:"user_id" gorm:"not null;index"`
	ConversationID uint          `json:"conversation_id" gorm:"not null;index"`
	Prompt        string         `json:"prompt" gorm:"type:text"`
	Response      string         `json:"response" gorm:"type:text"`
	AIModel       string         `json:"ai_model"`                    // 使用的AI模型
	ResponseTime  time.Duration  `json:"response_time"`               // AI响应时间
	Tokens        int            `json:"tokens"`                      // 消耗的tokens
	Context       string         `json:"context" gorm:"type:json"`    // 上下文信息
	CreatedAt     time.Time      `json:"created_at"`
	UpdatedAt     time.Time      `json:"updated_at"`
	DeletedAt     gorm.DeletedAt `json:"-" gorm:"index"`

	// 关联关系
	User         User         `json:"-" gorm:"foreignKey:UserID"`
	Conversation Conversation `json:"-" gorm:"foreignKey:ConversationID"`
}

// MessageResponse 消息响应结构
type MessageResponse struct {
	ID             uint      `json:"id"`
	ConversationID uint      `json:"conversation_id"`
	SenderID       uint      `json:"sender_id"`
	Content        string    `json:"content"`
	MessageType    string    `json:"message_type"`
	IsFromAI       bool      `json:"is_from_ai"`
	Sender         UserInfo  `json:"sender"`
	CreatedAt      time.Time `json:"created_at"`
}

// ConversationResponse 会话响应结构
type ConversationResponse struct {
	ID              uint                `json:"id"`
	Type            string              `json:"type"`
	LastMessage     *MessageResponse    `json:"last_message"`
	LastMessageTime *time.Time          `json:"last_message_time"`
	Participants    []UserInfo          `json:"participants"`
	UnreadCount     int                 `json:"unread_count"`
	CreatedAt       time.Time           `json:"created_at"`
}

// UserInfo 用户基本信息结构
type UserInfo struct {
	ID       uint   `json:"id"`
	Nickname string `json:"nickname"`
	Avatar   string `json:"avatar"`
	IsOnline bool   `json:"is_online"`
}

// ToMessageResponse 转换为MessageResponse
func (m *Message) ToMessageResponse() MessageResponse {
	return MessageResponse{
		ID:             m.ID,
		ConversationID: m.ConversationID,
		SenderID:       m.SenderID,
		Content:        m.Content,
		MessageType:    m.MessageType,
		IsFromAI:       m.IsFromAI,
		Sender: UserInfo{
			ID:       m.Sender.ID,
			Nickname: m.Sender.Nickname,
			Avatar:   m.Sender.Avatar,
			IsOnline: m.Sender.IsOnline,
		},
		CreatedAt: m.CreatedAt,
	}
}

// ToConversationResponse 转换为ConversationResponse
func (c *Conversation) ToConversationResponse(unreadCount int) ConversationResponse {
	var lastMessage *MessageResponse
	if c.LastMessage != nil {
		msg := c.LastMessage.ToMessageResponse()
		lastMessage = &msg
	}

	var participants []UserInfo
	for _, participant := range c.Participants {
		participants = append(participants, UserInfo{
			ID:       participant.ID,
			Nickname: participant.Nickname,
			Avatar:   participant.Avatar,
			IsOnline: participant.IsOnline,
		})
	}

	return ConversationResponse{
		ID:              c.ID,
		Type:            c.Type,
		LastMessage:     lastMessage,
		LastMessageTime: c.LastMessageTime,
		Participants:    participants,
		UnreadCount:     unreadCount,
		CreatedAt:       c.CreatedAt,
	}
} 