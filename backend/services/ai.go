package services

import (
	"context"
	"fmt"
	"math/rand"
	"strings"
	"time"
)

type AIService struct {
	apiKey string
}

// AIResponse AI响应结构
type AIResponse struct {
	Content      string        `json:"content"`
	Model        string        `json:"model"`
	ResponseTime time.Duration `json:"response_time"`
	Tokens       int           `json:"tokens"`
}

// TagsRequest 标签生成请求
type TagsRequest struct {
	Content string `json:"content"`
	UserID  uint   `json:"user_id"`
}

// TagsResponse 标签生成响应
type TagsResponse struct {
	Tags      []string `json:"tags"`
	Confidence float64 `json:"confidence"`
}

// ConversationRequest 对话请求
type ConversationRequest struct {
	Message   string            `json:"message"`
	UserID    uint              `json:"user_id"`
	Context   map[string]string `json:"context"`
	Persona   string            `json:"persona"` // AI角色设定
}

// ProfileAnalysisRequest 资料分析请求
type ProfileAnalysisRequest struct {
	UserID     uint     `json:"user_id"`
	Bio        string   `json:"bio"`
	Interests  []string `json:"interests"`
	Photos     []string `json:"photos"`
	Age        int      `json:"age"`
	Occupation string   `json:"occupation"`
}

// ProfileAnalysisResponse 资料分析响应
type ProfileAnalysisResponse struct {
	Score         int      `json:"score"`
	Completeness  float64  `json:"completeness"`
	Attractiveness float64 `json:"attractiveness"`
	Suggestions   []string `json:"suggestions"`
	Strengths     []string `json:"strengths"`
	Keywords      []string `json:"keywords"`
}

// NewAIService 创建AI服务
func NewAIService(apiKey string) *AIService {
	return &AIService{
		apiKey: apiKey,
	}
}

// GenerateTags 生成兴趣标签
func (s *AIService) GenerateTags(ctx context.Context, req *TagsRequest) (*TagsResponse, error) {
	start := time.Now()
	
	// 模拟AI处理延迟
	time.Sleep(time.Millisecond * time.Duration(800+rand.Intn(700)))

	// 简单的关键词提取（实际应该调用AI API）
	tags := s.extractTags(req.Content)
	
	// 计算置信度
	confidence := s.calculateTagConfidence(req.Content, tags)

	fmt.Printf("[AI Service] Generated tags for user %d in %v\n", req.UserID, time.Since(start))

	return &TagsResponse{
		Tags:       tags,
		Confidence: confidence,
	}, nil
}

// Conversation AI对话
func (s *AIService) Conversation(ctx context.Context, req *ConversationRequest) (*AIResponse, error) {
	start := time.Now()
	
	// 模拟AI处理延迟
	time.Sleep(time.Millisecond * time.Duration(1000+rand.Intn(1500)))

	// 生成AI回复（实际应该调用AI API）
	response := s.generateResponse(req.Message, req.Persona, req.Context)
	
	responseTime := time.Since(start)
	
	fmt.Printf("[AI Service] Generated response for user %d in %v\n", req.UserID, responseTime)

	return &AIResponse{
		Content:      response,
		Model:        "gpt-3.5-turbo", // 模拟模型名称
		ResponseTime: responseTime,
		Tokens:       len(response) / 4, // 简单估算token数量
	}, nil
}

// AnalyzeProfile 分析用户资料
func (s *AIService) AnalyzeProfile(ctx context.Context, req *ProfileAnalysisRequest) (*ProfileAnalysisResponse, error) {
	start := time.Now()
	
	// 模拟AI处理延迟
	time.Sleep(time.Millisecond * time.Duration(1500+rand.Intn(1000)))

	// 分析资料完整度
	completeness := s.calculateCompleteness(req)
	
	// 分析吸引力评分
	attractiveness := s.calculateAttractiveness(req)
	
	// 综合评分
	score := int((completeness + attractiveness) / 2)
	
	// 生成建议
	suggestions := s.generateSuggestions(req, completeness, attractiveness)
	
	// 分析优势
	strengths := s.analyzeStrengths(req)
	
	// 提取关键词
	keywords := s.extractProfileKeywords(req)

	fmt.Printf("[AI Service] Analyzed profile for user %d in %v\n", req.UserID, time.Since(start))

	return &ProfileAnalysisResponse{
		Score:          score,
		Completeness:   completeness,
		Attractiveness: attractiveness,
		Suggestions:    suggestions,
		Strengths:      strengths,
		Keywords:       keywords,
	}, nil
}

// extractTags 提取标签（简化版本）
func (s *AIService) extractTags(content string) []string {
	var tags []string
	content = strings.ToLower(content)
	
	tagMap := map[string]string{
		"摄影":   "摄影",
		"拍照":   "摄影", 
		"旅行":   "旅行",
		"旅游":   "旅行",
		"电影":   "影视",
		"看电影": "影视",
		"运动":   "运动健身",
		"健身":   "运动健身",
		"音乐":   "音乐",
		"唱歌":   "音乐",
		"读书":   "阅读",
		"阅读":   "阅读",
		"美食":   "美食",
		"吃":    "美食",
		"游戏":   "游戏",
		"艺术":   "艺术",
		"绘画":   "艺术",
		"咖啡":   "咖啡",
		"宠物":   "宠物",
		"狗":    "宠物",
		"猫":    "宠物",
		"瑜伽":   "瑜伽",
		"舞蹈":   "舞蹈",
		"书法":   "书法",
	}
	
	tagCount := make(map[string]int)
	for keyword, tag := range tagMap {
		if strings.Contains(content, keyword) {
			tagCount[tag]++
		}
	}
	
	// 选择出现频率高的标签
	for tag, count := range tagCount {
		if count > 0 {
			tags = append(tags, tag)
		}
	}
	
	// 如果没有匹配到标签，返回通用标签
	if len(tags) == 0 {
		tags = []string{"生活", "社交", "娱乐"}
	}
	
	return tags
}

// calculateTagConfidence 计算标签置信度
func (s *AIService) calculateTagConfidence(content string, tags []string) float64 {
	if len(content) < 10 {
		return 0.6
	}
	if len(tags) == 0 {
		return 0.3
	}
	return 0.85 + rand.Float64()*0.1 // 0.85-0.95之间
}

// generateResponse 生成AI回复
func (s *AIService) generateResponse(message, persona string, context map[string]string) string {
	message = strings.ToLower(message)
	
	// 根据不同角色生成不同风格的回复
	switch persona {
	case "温柔":
		return s.generateGentleResponse(message)
	case "活泼":
		return s.generateLivelyResponse(message)
	case "智慧":
		return s.generateWiseResponse(message)
	default:
		return s.generateDefaultResponse(message)
	}
}

// generateGentleResponse 生成温柔风格回复
func (s *AIService) generateGentleResponse(message string) string {
	responses := []string{
		"我理解你的感受，想聊聊这个话题吗？",
		"听起来你今天心情不错呢 😊",
		"你说得很有道理，我也是这么想的",
		"这确实是个有趣的观点，你能详细说说吗？",
		"我很好奇你对这件事的看法",
		"你的想法总是那么独特",
	}
	return responses[rand.Intn(len(responses))]
}

// generateLivelyResponse 生成活泼风格回复
func (s *AIService) generateLivelyResponse(message string) string {
	responses := []string{
		"哈哈，你太有趣了！😄",
		"哇，这听起来超酷的！",
		"我也想试试这个！",
		"你总是能找到有趣的话题～",
		"说得对！我们继续聊聊吧！",
		"太棒了，跟你聊天总是很开心！",
	}
	return responses[rand.Intn(len(responses))]
}

// generateWiseResponse 生成智慧风格回复
func (s *AIService) generateWiseResponse(message string) string {
	responses := []string{
		"从不同角度看，这个问题确实值得深思",
		"这让我想到了一个有趣的观点...",
		"根据我的观察，这种情况很常见",
		"我觉得这背后可能有更深层的原因",
		"这是一个很好的问题，值得我们深入探讨",
		"从你的话中我能感受到你的思考深度",
	}
	return responses[rand.Intn(len(responses))]
}

// generateDefaultResponse 生成默认回复
func (s *AIService) generateDefaultResponse(message string) string {
	responses := []string{
		"这确实是个有趣的话题！",
		"我很同意你的看法",
		"能详细说说吗？我很感兴趣",
		"听起来很不错！",
		"你的经历真的很特别",
		"我们可以继续聊这个话题",
	}
	return responses[rand.Intn(len(responses))]
}

// calculateCompleteness 计算资料完整度
func (s *AIService) calculateCompleteness(req *ProfileAnalysisRequest) float64 {
	score := 0.0
	total := 7.0
	
	if req.Bio != "" && len(req.Bio) > 10 {
		score += 1.0
	}
	if len(req.Interests) > 0 {
		score += 1.0
	}
	if len(req.Photos) > 0 {
		score += 1.0
	}
	if req.Age > 0 {
		score += 1.0
	}
	if req.Occupation != "" {
		score += 1.0
	}
	// 其他字段...
	score += 2.0 // 基础信息
	
	return (score / total) * 100
}

// calculateAttractiveness 计算吸引力评分
func (s *AIService) calculateAttractiveness(req *ProfileAnalysisRequest) float64 {
	score := 60.0 // 基础分
	
	// 根据简介质量加分
	if len(req.Bio) > 50 {
		score += 10.0
	}
	
	// 根据兴趣多样性加分
	if len(req.Interests) >= 3 {
		score += 10.0
	}
	
	// 根据照片数量加分
	if len(req.Photos) >= 3 {
		score += 15.0
	}
	
	// 随机因素
	score += rand.Float64() * 10
	
	if score > 95 {
		score = 95
	}
	
	return score
}

// generateSuggestions 生成建议
func (s *AIService) generateSuggestions(req *ProfileAnalysisRequest, completeness, attractiveness float64) []string {
	var suggestions []string
	
	if len(req.Photos) < 3 {
		suggestions = append(suggestions, "添加2-3张生活照可提升匹配率35%")
	}
	
	if len(req.Bio) < 30 {
		suggestions = append(suggestions, "详细描述你的兴趣爱好能吸引更多同频好友")
	}
	
	if len(req.Interests) < 3 {
		suggestions = append(suggestions, "添加更多兴趣标签有助于精准匹配")
	}
	
	if completeness < 80 {
		suggestions = append(suggestions, "完善个人资料可大幅提升匹配成功率")
	}
	
	return suggestions
}

// analyzeStrengths 分析优势
func (s *AIService) analyzeStrengths(req *ProfileAnalysisRequest) []string {
	var strengths []string
	
	if len(req.Bio) > 50 {
		strengths = append(strengths, "个人简介详细生动")
	}
	
	if len(req.Interests) >= 3 {
		strengths = append(strengths, "兴趣爱好丰富多样")
	}
	
	if len(req.Photos) >= 2 {
		strengths = append(strengths, "照片展示充分")
	}
	
	return strengths
}

// extractProfileKeywords 提取资料关键词
func (s *AIService) extractProfileKeywords(req *ProfileAnalysisRequest) []string {
	var keywords []string
	
	// 从简介中提取关键词
	if req.Bio != "" {
		bioKeywords := s.extractTextKeywords(req.Bio)
		keywords = append(keywords, bioKeywords...)
	}
	
	// 添加兴趣标签
	keywords = append(keywords, req.Interests...)
	
	// 添加职业相关
	if req.Occupation != "" {
		keywords = append(keywords, req.Occupation)
	}
	
	return keywords
}

// extractTextKeywords 从文本提取关键词
func (s *AIService) extractTextKeywords(text string) []string {
	// 简单的关键词提取
	keywords := []string{}
	text = strings.ToLower(text)
	
	keywordMap := map[string]bool{
		"创意": true, "设计": true, "艺术": true, "音乐": true,
		"旅行": true, "摄影": true, "美食": true, "运动": true,
		"阅读": true, "电影": true, "科技": true, "创业": true,
	}
	
	for keyword := range keywordMap {
		if strings.Contains(text, keyword) {
			keywords = append(keywords, keyword)
		}
	}
	
	return keywords
} 