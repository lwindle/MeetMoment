package services

import (
	"errors"
	"meetmoment-backend/models"

	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

type ChatService struct {
	db  *gorm.DB
	rdb *redis.Client
}

// NewChatService 创建聊天服务
func NewChatService(db *gorm.DB, rdb *redis.Client) *ChatService {
	return &ChatService{
		db:  db,
		rdb: rdb,
	}
}

// GetConversations 获取用户会话列表
func (s *ChatService) GetConversations(userID uint) ([]models.ConversationResponse, error) {
	var conversations []models.Conversation
	
	if err := s.db.Preload("Participants").Preload("LastMessage.Sender").
		Joins("JOIN conversation_participants ON conversations.id = conversation_participants.conversation_id").
		Where("conversation_participants.user_id = ?", userID).
		Find(&conversations).Error; err != nil {
		return nil, err
	}

	var responses []models.ConversationResponse
	for _, conv := range conversations {
		responses = append(responses, conv.ToConversationResponse(0)) // 简化处理，未读数为0
	}

	return responses, nil
}

// GetMessages 获取会话消息
func (s *ChatService) GetMessages(conversationID uint, userID uint, limit int, offset int) ([]models.MessageResponse, error) {
	var messages []models.Message
	
	if err := s.db.Preload("Sender").
		Where("conversation_id = ?", conversationID).
		Order("created_at DESC").
		Limit(limit).
		Offset(offset).
		Find(&messages).Error; err != nil {
		return nil, err
	}

	var responses []models.MessageResponse
	for _, msg := range messages {
		responses = append(responses, msg.ToMessageResponse())
	}

	return responses, nil
}

// SendMessage 发送消息
func (s *ChatService) SendMessage(senderID uint, conversationID uint, content string, messageType string) (*models.MessageResponse, error) {
	message := models.Message{
		ConversationID: conversationID,
		SenderID:       senderID,
		Content:        content,
		MessageType:    messageType,
		IsFromAI:       false,
	}

	if err := s.db.Create(&message).Error; err != nil {
		return nil, errors.New("消息发送失败")
	}

	// 加载完整消息信息
	s.db.Preload("Sender").First(&message, message.ID)

	response := message.ToMessageResponse()
	return &response, nil
} 