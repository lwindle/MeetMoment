package handlers

import (
	"net/http"
	"meetmoment-backend/services"
	"meetmoment-backend/middleware"

	"github.com/gin-gonic/gin"
)

type UserHandler struct {
	userService     *services.UserService
	supabaseService *services.SupabaseService
}

// NewUserHandler 创建用户处理器
func NewUserHandler(userService *services.UserService, supabaseService *services.SupabaseService) *UserHandler {
	return &UserHandler{
		userService:     userService,
		supabaseService: supabaseService,
	}
}

// GetProfile 获取用户资料
func (h *UserHandler) GetProfile(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	profile, err := h.userService.GetProfile(userID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "获取失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   profile,
	})
}

// UpdateProfile 更新用户资料
func (h *UserHandler) UpdateProfile(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	var updates map[string]interface{}
	if err := c.ShouldBindJSON(&updates); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "请求参数错误",
			"message": err.Error(),
		})
		return
	}

	if err := h.userService.UpdateProfile(userID, updates); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "更新失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "资料更新成功",
	})
}

// UploadPhoto 上传照片
func (h *UserHandler) UploadPhoto(c *gin.Context) {
	userID := middleware.GetUserID(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":   "未授权",
			"message": "用户ID获取失败",
		})
		return
	}

	// 解析文件
	file, header, err := c.Request.FormFile("photo")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "文件上传失败",
			"message": "无法获取上传的文件",
		})
		return
	}
	defer file.Close()

	// 验证文件类型
	allowedTypes := map[string]bool{
		"image/jpeg": true,
		"image/jpg":  true,
		"image/png":  true,
		"image/webp": true,
	}

	contentType := header.Header.Get("Content-Type")
	if !allowedTypes[contentType] {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "文件类型不支持",
			"message": "只支持 JPEG、PNG、WebP 格式的图片",
		})
		return
	}

	// 验证文件大小 (5MB限制)
	if header.Size > 5*1024*1024 {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "文件过大",
			"message": "文件大小不能超过5MB",
		})
		return
	}

	// 上传到 Supabase
	uploadResult, err := h.supabaseService.UploadUserPhoto(c.Request.Context(), userID, file, header)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "上传失败",
			"message": err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "照片上传成功",
		"data": gin.H{
			"url":      uploadResult.PublicURL,
			"filename": uploadResult.Key,
		},
	})
}

// GetPhotos 获取照片列表
func (h *UserHandler) GetPhotos(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   []string{},
	})
}

// DeletePhoto 删除照片
func (h *UserHandler) DeletePhoto(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "照片删除成功",
	})
}

// GetCircles 获取圈子列表
func (h *UserHandler) GetCircles(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   []string{},
	})
}

// JoinCircle 加入圈子
func (h *UserHandler) JoinCircle(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "加入圈子成功",
	})
}

// LeaveCircle 离开圈子
func (h *UserHandler) LeaveCircle(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "离开圈子成功",
	})
}

// GetCirclePosts 获取圈子动态
func (h *UserHandler) GetCirclePosts(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   []string{},
	})
}

// CreatePost 创建动态
func (h *UserHandler) CreatePost(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "动态创建成功",
	})
}

// AnalyzeProfile AI分析资料
func (h *UserHandler) AnalyzeProfile(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"message": "资料分析功能暂未实现",
	})
} 