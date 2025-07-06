package main

import (
	"context"
	"log"
	"meetmoment-backend/config"
	"meetmoment-backend/database"
	"meetmoment-backend/handlers"
	"meetmoment-backend/middleware"
	"meetmoment-backend/services"

	"github.com/gin-gonic/gin"
)

func main() {
	// 加载配置
	cfg := config.Load()

	// 初始化数据库 (Supabase PostgreSQL)
	db, err := database.InitPostgreSQL(cfg.DatabaseURL)
	if err != nil {
		log.Fatal("Failed to connect to Supabase database:", err)
	}

	// 初始化Redis
	rdb := database.InitRedis(cfg.RedisURL)

	// 初始化Supabase服务
	supabaseService := services.NewSupabaseService(cfg.SupabaseURL, cfg.SupabaseKey, cfg.SupabaseSecret)
	
	// 初始化存储桶
	if err := supabaseService.InitializeStorage(context.Background()); err != nil {
		log.Printf("Warning: Failed to initialize Supabase storage: %v", err)
	}

	// 初始化服务
	authService := services.NewAuthService(db, rdb, cfg.JWTSecret)
	userService := services.NewUserService(db, rdb)
	chatService := services.NewChatService(db, rdb)
	aiService := services.NewAIService(cfg.DashScopeAPIKey)
	matchService := services.NewMatchService(db, aiService)

	// 初始化处理器
	authHandler := handlers.NewAuthHandler(authService)
	userHandler := handlers.NewUserHandler(userService, supabaseService)
	chatHandler := handlers.NewChatHandler(chatService, aiService, db)
	matchHandler := handlers.NewMatchHandler(matchService)
	aliyunHandler := handlers.NewAliyunHandler()

	// 设置Gin模式
	if cfg.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	// 创建路由器
	r := gin.Default()

	// 添加中间件
	r.Use(middleware.CORS())
	r.Use(middleware.Logger())
	r.Use(middleware.Recovery())

	// API路由组
	api := r.Group("/api")
	{
		// 数据库状态检查
		api.GET("/status", func(c *gin.Context) {
			status := "ok"
			dbStatus := "connected"
			if db == nil {
				dbStatus = "disconnected"
				status = "warning"
			}
			c.JSON(200, gin.H{
				"status": status,
				"database": dbStatus,
				"service": "meetmoment-api",
			})
		})

		// 只有在数据库连接正常时才启用这些路由
		if db != nil {
			// 认证路由
			auth := api.Group("/auth")
			{
				auth.POST("/register", authHandler.Register)
				auth.POST("/login", authHandler.Login)
				auth.POST("/refresh", authHandler.RefreshToken)
				auth.POST("/logout", middleware.AuthRequired(cfg.JWTSecret), authHandler.Logout)
			}

			// 用户路由（需要认证）
			user := api.Group("/user")
			user.Use(middleware.AuthRequired(cfg.JWTSecret))
			{
				user.GET("/profile", userHandler.GetProfile)
				user.PUT("/profile", userHandler.UpdateProfile)
				user.POST("/upload-photo", userHandler.UploadPhoto)
				user.GET("/photos", userHandler.GetPhotos)
				user.DELETE("/photos/:id", userHandler.DeletePhoto)
			}

			// 匹配推荐路由
			match := api.Group("/match")
			match.Use(middleware.AuthRequired(cfg.JWTSecret))
			{
				match.GET("/recommendations", matchHandler.GetRecommendations)
				match.POST("/like", matchHandler.LikeUser)
				match.POST("/pass", matchHandler.PassUser)
				match.GET("/matches", matchHandler.GetMatches)
			}

			// 聊天路由
			chat := api.Group("/chat")
			chat.Use(middleware.AuthRequired(cfg.JWTSecret))
			{
				chat.GET("/conversations", chatHandler.GetConversations)
				chat.GET("/messages/:conversationId", chatHandler.GetMessages)
				chat.POST("/send", chatHandler.SendMessage)
				chat.GET("/ws", chatHandler.HandleWebSocket)
			}

			// 社交圈子路由
			circles := api.Group("/circles")
			circles.Use(middleware.AuthRequired(cfg.JWTSecret))
			{
				circles.GET("/", userHandler.GetCircles)
				circles.POST("/join", userHandler.JoinCircle)
				circles.POST("/leave", userHandler.LeaveCircle)
				circles.GET("/:id/posts", userHandler.GetCirclePosts)
				circles.POST("/:id/posts", userHandler.CreatePost)
			}

			// AI服务路由
			ai := api.Group("/ai")
			{
				ai.GET("/users", chatHandler.GetAIUsers) // 获取AI用户列表，无需认证
				ai.Use(middleware.AuthRequired(cfg.JWTSecret))
				ai.POST("/generate-tags", chatHandler.GenerateTags)
				ai.POST("/profile-analysis", userHandler.AnalyzeProfile)
				ai.POST("/conversation", chatHandler.AIConversation)
			}

			// 阿里云服务路由
			if aliyunHandler != nil {
				aliyun := api.Group("/aliyun")
				aliyun.Use(middleware.AuthRequired(cfg.JWTSecret))
				{
					aliyun.POST("/generate-image", aliyunHandler.GenerateImage)
					aliyun.POST("/query-task", aliyunHandler.QueryTask)
					aliyun.POST("/generate-beauty-portrait", aliyunHandler.GenerateBeautyPortrait)
				}
			}
		} else {
			// 数据库未连接时的提示路由
			api.GET("/*any", func(c *gin.Context) {
				c.JSON(503, gin.H{
					"error": "服务暂时不可用",
					"message": "数据库连接失败，请稍后重试",
				})
			})
		}
	}

	// 健康检查
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok", "service": "meetmoment-api"})
	})

	// 启动服务器
	log.Printf("Server starting on port %s", cfg.Port)
	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatal("Failed to start server:", err)
	}
} 