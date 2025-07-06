package handlers

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"meetmoment-backend/services"
)

type AliyunHandler struct {
	aliyunService *services.AliyunService
}

func NewAliyunHandler() *AliyunHandler {
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	if apiKey == "" {
		return nil
	}
	
	return &AliyunHandler{
		aliyunService: services.NewAliyunService(apiKey),
	}
}

// GenerateImageRequest 生成图片请求
type GenerateImageRequest struct {
	Prompt string `json:"prompt" binding:"required"`
}

// GenerateImageResponse 生成图片响应
type GenerateImageResponse struct {
	ImageURL string `json:"image_url"`
	TaskID   string `json:"task_id"`
}

// GenerateImage 生成图片接口
func (h *AliyunHandler) GenerateImage(c *gin.Context) {
	if h.aliyunService == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"error": "阿里云服务未配置",
		})
		return
	}

	var req GenerateImageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "请求参数错误: " + err.Error(),
		})
		return
	}

	// 创建图像生成任务
	response, err := h.aliyunService.CreateImageTask(req.Prompt)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "创建图像生成任务失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, GenerateImageResponse{
		TaskID: response.Output.TaskID,
	})
}

// QueryTaskRequest 查询任务请求
type QueryTaskRequest struct {
	TaskID string `json:"task_id" binding:"required"`
}

// QueryTask 查询任务状态
func (h *AliyunHandler) QueryTask(c *gin.Context) {
	if h.aliyunService == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"error": "阿里云服务未配置",
		})
		return
	}

	var req QueryTaskRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "请求参数错误: " + err.Error(),
		})
		return
	}

	// 查询任务结果
	result, err := h.aliyunService.QueryTaskResult(req.TaskID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "查询任务失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, result)
}

// GenerateBeautyPortraitRequest 生成美女头像请求
type GenerateBeautyPortraitRequest struct {
	Description string `json:"description" binding:"required"`
}

// GenerateBeautyPortrait 生成美女头像（同步接口）
func (h *AliyunHandler) GenerateBeautyPortrait(c *gin.Context) {
	if h.aliyunService == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"error": "阿里云服务未配置",
		})
		return
	}

	var req GenerateBeautyPortraitRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "请求参数错误: " + err.Error(),
		})
		return
	}

	// 生成美女头像（这是一个同步操作，会等待完成）
	imageURL, err := h.aliyunService.GenerateBeautyPortrait(req.Description)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "生成头像失败: " + err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, GenerateImageResponse{
		ImageURL: imageURL,
	})
} 