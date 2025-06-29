package handlers

import (
	"net/http"
	"strconv"
	"meetmoment-backend/services"
	"meetmoment-backend/middleware"

	"github.com/gin-gonic/gin"
)

type MatchHandler struct {
	matchService *services.MatchService
}

// NewMatchHandler 创建匹配处理器
func NewMatchHandler(matchService *services.MatchService) *MatchHandler {
	return &MatchHandler{
		matchService: matchService,
	}
}

// GetRecommendations 获取推荐用户
func (h *MatchHandler) GetRecommendations(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	limit := 10
	if limitStr := c.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 && l <= 50 {
			limit = l
		}
	}

	recommendations, err := h.matchService.GetRecommendations(userID, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "获取失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   recommendations,
	})
}

// LikeUser 喜欢用户
func (h *MatchHandler) LikeUser(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var req struct {
		TargetUserID uint `json:"target_user_id" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	isMatched, err := h.matchService.LikeUser(userID, req.TargetUserID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "操作失败",
			"message": err.Error(),
		})
		return
	}

	response := gin.H{
		"status": "success",
		"message": "操作成功",
		"data": gin.H{
			"is_matched": isMatched,
		},
	}

	if isMatched {
		response["message"] = "恭喜！你们互相喜欢了"
	}

	c.JSON(http.StatusOK, response)
}

// PassUser 跳过用户
func (h *MatchHandler) PassUser(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var req struct {
		TargetUserID uint `json:"target_user_id" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	if err := h.matchService.PassUser(userID, req.TargetUserID); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "操作失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "已跳过",
	})
}

// GetMatches 获取匹配列表
func (h *MatchHandler) GetMatches(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	matches, err := h.matchService.GetMatches(userID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "获取失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   matches,
	})
} 