package handlers

import (
	"context"
	"net/http"
	"strconv"
	"meetmoment-backend/services"
	"meetmoment-backend/middleware"

	"github.com/gin-gonic/gin"
)

type ChatHandler struct {
	chatService *services.ChatService
	aiService   *services.AIService
}

// NewChatHandler 创建聊天处理器
func NewChatHandler(chatService *services.ChatService, aiService *services.AIService) *ChatHandler {
	return &ChatHandler{
		chatService: chatService,
		aiService:   aiService,
	}
}

// GetConversations 获取会话列表
func (h *ChatHandler) GetConversations(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	conversations, err := h.chatService.GetConversations(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "获取失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   conversations,
	})
}

// GetMessages 获取消息列表
func (h *ChatHandler) GetMessages(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	conversationIDStr := c.Param("conversationId")
	conversationID, err := strconv.ParseUint(conversationIDStr, 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "参数错误",
			"message": "会话ID格式错误",
		})
		return
	}

	limit := 50
	offset := 0
	if limitStr := c.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}
	if offsetStr := c.Query("offset"); offsetStr != "" {
		if o, err := strconv.Atoi(offsetStr); err == nil {
			offset = o
		}
	}

	messages, err := h.chatService.GetMessages(uint(conversationID), userID, limit, offset)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "获取失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   messages,
	})
}

// SendMessage 发送消息
func (h *ChatHandler) SendMessage(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var req struct {
		ConversationID uint   `json:"conversation_id" binding:"required"`
		Content        string `json:"content" binding:"required"`
		MessageType    string `json:"message_type"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	if req.MessageType == "" {
		req.MessageType = "text"
	}

	message, err := h.chatService.SendMessage(userID, req.ConversationID, req.Content, req.MessageType)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "发送失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "消息发送成功",
		"data":   message,
	})
}

// HandleWebSocket WebSocket连接处理
func (h *ChatHandler) HandleWebSocket(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "WebSocket功能暂未实现",
	})
}

// GenerateTags AI生成标签
func (h *ChatHandler) GenerateTags(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var req struct {
		Content string `json:"content" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	tagsReq := &services.TagsRequest{
		Content: req.Content,
		UserID:  userID,
	}

	response, err := h.aiService.GenerateTags(context.Background(), tagsReq)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "生成失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   response,
	})
}

// AIConversation AI对话
func (h *ChatHandler) AIConversation(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var req struct {
		Message string            `json:"message" binding:"required"`
		Persona string            `json:"persona"`
		Context map[string]string `json:"context"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	conversationReq := &services.ConversationRequest{
		Message: req.Message,
		UserID:  userID,
		Persona: req.Persona,
		Context: req.Context,
	}

	response, err := h.aiService.Conversation(context.Background(), conversationReq)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "对话生成失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   response,
	})
} 