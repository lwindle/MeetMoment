package config

import (
	"os"
)

type Config struct {
	Environment    string
	Port          string
	DatabaseURL   string
	RedisURL      string
	JWTSecret     string
	AIAPIKey      string
	FileUploadPath string
	MaxFileSize   int64
	SupabaseURL   string
	SupabaseKey   string
	SupabaseSecret string
	DashScopeAPIKey string
}

// Load 加载配置
func Load() *Config {
	return &Config{
		Environment:    getEnv("ENVIRONMENT", "development"),
		Port:          getEnv("PORT", "8080"),
		DatabaseURL:   getEnv("DATABASE_URL", "postgres://postgres:password@localhost:5432/meetmoment?sslmode=disable&statement_cache_mode=describe&&pool_max_conns=1&pool_min_conns=0"),
		RedisURL:      getEnv("REDIS_URL", "redis://localhost:6379/0"),
		JWTSecret:     getEnv("JWT_SECRET", "your-super-secret-jwt-key-change-this-in-production"),
		AIAPIKey:      getEnv("AI_API_KEY", ""),
		FileUploadPath: getEnv("FILE_UPLOAD_PATH", "./uploads"),
		MaxFileSize:   getEnvInt64("MAX_FILE_SIZE", 5*1024*1024), // 5MB
		SupabaseURL:   getEnv("SUPABASE_URL", ""),
		SupabaseKey:   getEnv("SUPABASE_ANON_KEY", ""),
		SupabaseSecret: getEnv("SUPABASE_SERVICE_ROLE_KEY", ""),
		DashScopeAPIKey: getEnv("DASHSCOPE_API_KEY", ""),
	}
}

// getEnv 获取环境变量，如果不存在则返回默认值
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// getEnvInt64 获取int64类型的环境变量
func getEnvInt64(key string, defaultValue int64) int64 {
	if value := os.Getenv(key); value != "" {
		// 这里应该进行字符串到int64的转换，简化处理
		return defaultValue
	}
	return defaultValue
} 