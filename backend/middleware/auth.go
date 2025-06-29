package middleware

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

// JWTClaims JWT声明结构
type JWTClaims struct {
	UserID   uint   `json:"user_id"`
	Phone    string `json:"phone"`
	Nickname string `json:"nickname"`
	jwt.RegisteredClaims
}

// AuthRequired 认证中间件
func AuthRequired(jwtSecret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// 从请求头获取token
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "未授权",
				"message": "缺少Authorization头",
			})
			c.Abort()
			return
		}

		// 检查Bearer格式
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "未授权",
				"message": "无效的token格式",
			})
			c.Abort()
			return
		}

		// 解析token
		token, err := jwt.ParseWithClaims(tokenString, &JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
			return []byte(jwtSecret), nil
		})

		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "未授权",
				"message": "无效的token",
			})
			c.Abort()
			return
		}

		// 验证token
		if claims, ok := token.Claims.(*JWTClaims); ok && token.Valid {
			// 将用户信息存储到上下文中
			c.Set("user_id", claims.UserID)
			c.Set("phone", claims.Phone)
			c.Set("nickname", claims.Nickname)
			c.Next()
		} else {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error":   "未授权",
				"message": "token验证失败",
			})
			c.Abort()
			return
		}
	}
}

// GetUserID 从上下文获取用户ID
func GetUserID(c *gin.Context) uint {
	userID, exists := c.Get("user_id")
	if !exists {
		return 0
	}
	return userID.(uint)
}

// GetUserPhone 从上下文获取用户手机号
func GetUserPhone(c *gin.Context) string {
	phone, exists := c.Get("phone")
	if !exists {
		return ""
	}
	return phone.(string)
}

// GetUserNickname 从上下文获取用户昵称
func GetUserNickname(c *gin.Context) string {
	nickname, exists := c.Get("nickname")
	if !exists {
		return ""
	}
	return nickname.(string)
} 