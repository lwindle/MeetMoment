package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// AliyunService 阿里云服务
type AliyunService struct {
	APIKey string
	Client *http.Client
}

// NewAliyunService 创建阿里云服务实例
func NewAliyunService(apiKey string) *AliyunService {
	return &AliyunService{
		APIKey: apiKey,
		Client: &http.Client{
			Timeout: 60 * time.Second,
		},
	}
}

// TextToImageRequest 文生图请求结构
type TextToImageRequest struct {
	Model  string `json:"model"`
	Input  Input  `json:"input"`
	Parameters Parameters `json:"parameters"`
}

type Input struct {
	Prompt         string `json:"prompt"`
	NegativePrompt string `json:"negative_prompt,omitempty"`
}

type Parameters struct {
	Size          string `json:"size"`
	N             int    `json:"n"`
	Seed          int    `json:"seed,omitempty"`
	PromptExtend  bool   `json:"prompt_extend,omitempty"`
	Watermark     bool   `json:"watermark,omitempty"`
}

// TextToImageResponse 文生图响应结构
type TextToImageResponse struct {
	RequestID string `json:"request_id"`
	Output    Output `json:"output"`
	Usage     Usage  `json:"usage"`
}

type Output struct {
	TaskID     string `json:"task_id"`
	TaskStatus string `json:"task_status"`
	Results    []Result `json:"results,omitempty"`
	TaskMetrics TaskMetrics `json:"task_metrics,omitempty"`
}

type Result struct {
	OrigPrompt   string `json:"orig_prompt"`
	ActualPrompt string `json:"actual_prompt"`
	URL          string `json:"url"`
}

type TaskMetrics struct {
	Total     int `json:"TOTAL"`
	Succeeded int `json:"SUCCEEDED"`
	Failed    int `json:"FAILED"`
}

type Usage struct {
	ImageCount int `json:"image_count"`
}

// TaskQueryResponse 任务查询响应
type TaskQueryResponse struct {
	RequestID string `json:"request_id"`
	Output    Output `json:"output"`
	Usage     Usage  `json:"usage"`
}

// CreateImageTask 创建图像生成任务
func (s *AliyunService) CreateImageTask(prompt string) (*TextToImageResponse, error) {
	request := TextToImageRequest{
		Model: "wanx2.1-t2i-turbo", // 使用速度更快的模型
		Input: Input{
			Prompt: prompt,
			NegativePrompt: "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, mutation, watermark, text, signature",
		},
		Parameters: Parameters{
			Size:         "1024*1024",
			N:            1,
			PromptExtend: true,
			Watermark:    false,
		},
	}

	jsonData, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %v", err)
	}

	req.Header.Set("Authorization", "Bearer "+s.APIKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-DashScope-Async", "enable") // 启用异步模式

	resp, err := s.Client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to send request: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %v", err)
	}

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	var response TextToImageResponse
	if err := json.Unmarshal(body, &response); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &response, nil
}

// QueryTaskResult 查询任务结果
func (s *AliyunService) QueryTaskResult(taskID string) (*TaskQueryResponse, error) {
	url := fmt.Sprintf("https://dashscope.aliyuncs.com/api/v1/tasks/%s", taskID)
	
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %v", err)
	}

	req.Header.Set("Authorization", "Bearer "+s.APIKey)

	resp, err := s.Client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to send request: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %v", err)
	}

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	var response TaskQueryResponse
	if err := json.Unmarshal(body, &response); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &response, nil
}

// WaitForTaskCompletion 等待任务完成
func (s *AliyunService) WaitForTaskCompletion(taskID string, maxWaitTime time.Duration) (*TaskQueryResponse, error) {
	startTime := time.Now()
	
	for time.Since(startTime) < maxWaitTime {
		result, err := s.QueryTaskResult(taskID)
		if err != nil {
			return nil, err
		}

		switch result.Output.TaskStatus {
		case "SUCCEEDED":
			return result, nil
		case "FAILED":
			return nil, fmt.Errorf("task failed")
		case "PENDING", "RUNNING":
			// 继续等待
			time.Sleep(10 * time.Second)
		default:
			return nil, fmt.Errorf("unknown task status: %s", result.Output.TaskStatus)
		}
	}

	return nil, fmt.Errorf("task timeout after %v", maxWaitTime)
}

// GenerateBeautyPortrait 生成美女头像
func (s *AliyunService) GenerateBeautyPortrait(description string) (string, error) {
	// 构建详细的提示词
	prompt := fmt.Sprintf(`高清写实美女头像摄影，%s，专业摄影，柔和自然光线，清晰五官，温和表情，现代时尚，高质量，8K分辨率`, description)
	
	// 创建任务
	task, err := s.CreateImageTask(prompt)
	if err != nil {
		return "", fmt.Errorf("failed to create image task: %v", err)
	}

	// 等待任务完成 (最多等待5分钟)
	result, err := s.WaitForTaskCompletion(task.Output.TaskID, 5*time.Minute)
	if err != nil {
		return "", fmt.Errorf("failed to wait for task completion: %v", err)
	}

	if len(result.Output.Results) == 0 {
		return "", fmt.Errorf("no image generated")
	}

	return result.Output.Results[0].URL, nil
} 