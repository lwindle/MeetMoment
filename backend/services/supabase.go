package services

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"strings"
	"time"
)

type SupabaseService struct {
	url        string
	anonKey    string
	serviceKey string
	httpClient *http.Client
}

// SupabaseStorage 存储响应结构
type SupabaseStorageResponse struct {
	Key       string `json:"Key"`
	PublicURL string `json:"publicURL"`
}

// SupabaseAuthUser Supabase 用户结构
type SupabaseAuthUser struct {
	ID       string `json:"id"`
	Email    string `json:"email"`
	Phone    string `json:"phone"`
	Metadata map[string]interface{} `json:"user_metadata"`
}

// NewSupabaseService 创建 Supabase 服务
func NewSupabaseService(url, anonKey, serviceKey string) *SupabaseService {
	return &SupabaseService{
		url:        url,
		anonKey:    anonKey,
		serviceKey: serviceKey,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}
}

// UploadFile 上传文件到 Supabase Storage
func (s *SupabaseService) UploadFile(ctx context.Context, bucket, fileName string, file io.Reader, contentType string) (*SupabaseStorageResponse, error) {
	// 构建上传 URL
	uploadURL := fmt.Sprintf("%s/storage/v1/object/%s/%s", s.url, bucket, fileName)

	// 创建请求
	req, err := http.NewRequestWithContext(ctx, "POST", uploadURL, file)
	if err != nil {
		return nil, fmt.Errorf("创建上传请求失败: %w", err)
	}

	// 设置请求头
	req.Header.Set("Authorization", "Bearer "+s.serviceKey)
	req.Header.Set("Content-Type", contentType)
	req.Header.Set("apikey", s.anonKey)

	// 发送请求
	resp, err := s.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("上传文件失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("上传失败，状态码: %d, 响应: %s", resp.StatusCode, string(body))
	}

	// 获取公共URL
	publicURL := s.GetPublicURL(bucket, fileName)

	return &SupabaseStorageResponse{
		Key:       fileName,
		PublicURL: publicURL,
	}, nil
}

// GetPublicURL 获取文件的公共访问 URL
func (s *SupabaseService) GetPublicURL(bucket, fileName string) string {
	return fmt.Sprintf("%s/storage/v1/object/public/%s/%s", s.url, bucket, fileName)
}

// DeleteFile 删除文件
func (s *SupabaseService) DeleteFile(ctx context.Context, bucket, fileName string) error {
	deleteURL := fmt.Sprintf("%s/storage/v1/object/%s/%s", s.url, bucket, fileName)

	req, err := http.NewRequestWithContext(ctx, "DELETE", deleteURL, nil)
	if err != nil {
		return fmt.Errorf("创建删除请求失败: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+s.serviceKey)
	req.Header.Set("apikey", s.anonKey)

	resp, err := s.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("删除文件失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("删除失败，状态码: %d, 响应: %s", resp.StatusCode, string(body))
	}

	return nil
}

// CreateBucket 创建存储桶
func (s *SupabaseService) CreateBucket(ctx context.Context, bucketName string, isPublic bool) error {
	createURL := fmt.Sprintf("%s/storage/v1/bucket", s.url)

	payload := map[string]interface{}{
		"id":     bucketName,
		"name":   bucketName,
		"public": isPublic,
	}

	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("序列化请求失败: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", createURL, bytes.NewBuffer(jsonPayload))
	if err != nil {
		return fmt.Errorf("创建请求失败: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+s.serviceKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("apikey", s.anonKey)

	resp, err := s.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("创建存储桶失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("创建存储桶失败，状态码: %d, 响应: %s", resp.StatusCode, string(body))
	}

	return nil
}

// SendRealtimeMessage 发送实时消息
func (s *SupabaseService) SendRealtimeMessage(ctx context.Context, channel, event string, payload interface{}) error {
	// 注意：这是一个简化的实现
	// 在实际应用中，你需要使用 Supabase 的 WebSocket 连接
	realtimeURL := fmt.Sprintf("%s/realtime/v1/channels/%s/messages", s.url, channel)

	message := map[string]interface{}{
		"event":   event,
		"payload": payload,
	}

	jsonPayload, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("序列化实时消息失败: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", realtimeURL, bytes.NewBuffer(jsonPayload))
	if err != nil {
		return fmt.Errorf("创建实时消息请求失败: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+s.serviceKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("apikey", s.anonKey)

	resp, err := s.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("发送实时消息失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("发送实时消息失败，状态码: %d, 响应: %s", resp.StatusCode, string(body))
	}

	return nil
}

// UploadUserPhoto 上传用户照片的便捷方法
func (s *SupabaseService) UploadUserPhoto(ctx context.Context, userID uint, file multipart.File, header *multipart.FileHeader) (*SupabaseStorageResponse, error) {
	// 生成文件名
	fileName := fmt.Sprintf("users/%d/%d_%s", userID, time.Now().Unix(), header.Filename)
	
	// 获取文件类型
	contentType := header.Header.Get("Content-Type")
	if contentType == "" {
		contentType = "application/octet-stream"
	}

	// 上传到 avatars 存储桶
	return s.UploadFile(ctx, "avatars", fileName, file, contentType)
}

// InitializeStorage 初始化存储桶
func (s *SupabaseService) InitializeStorage(ctx context.Context) error {
	buckets := []string{"avatars", "photos", "documents"}
	
	for _, bucket := range buckets {
		if err := s.CreateBucket(ctx, bucket, true); err != nil {
			// 如果存储桶已存在，忽略错误
			if !strings.Contains(err.Error(), "already exists") {
				return fmt.Errorf("创建存储桶 %s 失败: %w", bucket, err)
			}
		}
	}

	return nil
} 