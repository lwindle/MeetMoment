package services

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"strings"
	"time"
)

type AIService struct {
	apiKey     string
	httpClient *http.Client
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

// 阿里云通义千问API请求结构
type QwenRequest struct {
	Model    string      `json:"model"`
	Messages []QwenMessage `json:"messages"`
	Parameters QwenParameters `json:"parameters,omitempty"`
}

type QwenMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type QwenParameters struct {
	Temperature float64 `json:"temperature,omitempty"`
	TopP        float64 `json:"top_p,omitempty"`
	MaxTokens   int     `json:"max_tokens,omitempty"`
}

// 阿里云通义千问API响应结构
type QwenResponse struct {
	RequestID string       `json:"request_id"`
	Output    QwenOutput   `json:"output"`
	Usage     QwenUsage    `json:"usage"`
}

type QwenOutput struct {
	Text         string `json:"text"`
	FinishReason string `json:"finish_reason"`
	Choices      []QwenChoice `json:"choices"`
}

type QwenChoice struct {
	Message      QwenMessage `json:"message"`
	FinishReason string      `json:"finish_reason"`
}

type QwenUsage struct {
	InputTokens  int `json:"input_tokens"`
	OutputTokens int `json:"output_tokens"`
	TotalTokens  int `json:"total_tokens"`
}

// NewAIService 创建AI服务
func NewAIService(apiKey string) *AIService {
	return &AIService{
		apiKey: apiKey,
		httpClient: &http.Client{
			Timeout: 60 * time.Second,
		},
	}
}

// GenerateTags 生成兴趣标签
func (s *AIService) GenerateTags(ctx context.Context, req *TagsRequest) (*TagsResponse, error) {
	start := time.Now()
	
	// 构建提示词
	prompt := fmt.Sprintf(`请分析以下文本内容，提取出相关的兴趣标签，每个标签用中文表示，最多返回8个标签。
文本内容：%s

请只返回标签列表，用逗号分隔，不要其他解释。`, req.Content)

	// 调用通义千问API
	response, err := s.callQwenAPI(ctx, prompt, "")
	if err != nil {
		// 如果API调用失败，使用本地方法作为备选
		tags := s.extractTags(req.Content)
		confidence := s.calculateTagConfidence(req.Content, tags)
		
		fmt.Printf("[AI Service] Fallback to local tags for user %d in %v\n", req.UserID, time.Since(start))
		
		return &TagsResponse{
			Tags:       tags,
			Confidence: confidence,
		}, nil
	}

	// 解析AI返回的标签
	tags := s.parseTagsFromResponse(response.Content)
	confidence := 0.9 // AI生成的标签置信度较高

	fmt.Printf("[AI Service] Generated tags for user %d in %v\n", req.UserID, time.Since(start))

	return &TagsResponse{
		Tags:       tags,
		Confidence: confidence,
	}, nil
}

// Conversation AI对话
func (s *AIService) Conversation(ctx context.Context, req *ConversationRequest) (*AIResponse, error) {
	start := time.Now()
	
	// 根据角色设定构建系统提示词
	systemPrompt := s.buildSystemPrompt(req.Persona, req.Context)
	
	// 调用通义千问API
	response, err := s.callQwenAPI(ctx, req.Message, systemPrompt)
	if err != nil {
		// 如果API调用失败，使用本地方法作为备选
		content := s.generateResponse(req.Message, req.Persona, req.Context)
		responseTime := time.Since(start)
		
		fmt.Printf("[AI Service] Fallback to local response for user %d in %v\n", req.UserID, responseTime)
		
		return &AIResponse{
			Content:      content,
			Model:        "local-fallback",
			ResponseTime: responseTime,
			Tokens:       len(content) / 4,
		}, nil
	}

	responseTime := time.Since(start)
	
	fmt.Printf("[AI Service] Generated response for user %d in %v\n", req.UserID, responseTime)

	return response, nil
}

// callQwenAPI 调用阿里云通义千问API
func (s *AIService) callQwenAPI(ctx context.Context, userMessage, systemPrompt string) (*AIResponse, error) {
	start := time.Now()
	
	fmt.Printf("[AI Service] Calling Qwen API with message: %s\n", userMessage)
	if len(systemPrompt) > 50 {
		fmt.Printf("[AI Service] System prompt: %s...\n", systemPrompt[:50])
	} else {
		fmt.Printf("[AI Service] System prompt: %s\n", systemPrompt)
	}
	
	// 构建消息列表
	messages := []QwenMessage{}
	
	// 如果有系统提示词，添加到消息开头
	if systemPrompt != "" {
		messages = append(messages, QwenMessage{
			Role:    "system",
			Content: systemPrompt,
		})
	}
	
	// 添加用户消息
	messages = append(messages, QwenMessage{
		Role:    "user",
		Content: userMessage,
	})

	// 构建请求 - 使用OpenAI兼容格式
	request := struct {
		Model       string        `json:"model"`
		Messages    []QwenMessage `json:"messages"`
		Temperature float64       `json:"temperature,omitempty"`
		TopP        float64       `json:"top_p,omitempty"`
		MaxTokens   int           `json:"max_tokens,omitempty"`
	}{
		Model:       "qwen-plus", // 使用qwen-plus模型
		Messages:    messages,
		Temperature: 0.8,  // 适中的创造性
		TopP:        0.9,  // 保持回答的多样性
		MaxTokens:   1000, // 限制回答长度
	}

	jsonData, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	// 创建HTTP请求
	httpReq, err := http.NewRequestWithContext(ctx, "POST", 
		"https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", 
		bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %v", err)
	}

	// 设置请求头
	httpReq.Header.Set("Authorization", "Bearer "+s.apiKey)
	httpReq.Header.Set("Content-Type", "application/json")

	// 发送请求
	resp, err := s.httpClient.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to send request: %v", err)
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %v", err)
	}

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("[AI Service] API request failed with status %d: %s\n", resp.StatusCode, string(body))
		return nil, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	// 解析响应 - 使用OpenAI兼容格式
	var apiResponse struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
		Usage struct {
			TotalTokens int `json:"total_tokens"`
		} `json:"usage"`
	}

	if err := json.Unmarshal(body, &apiResponse); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	if len(apiResponse.Choices) == 0 {
		return nil, fmt.Errorf("no response choices returned")
	}

	responseTime := time.Since(start)

	return &AIResponse{
		Content:      apiResponse.Choices[0].Message.Content,
		Model:        "qwen-plus",
		ResponseTime: responseTime,
		Tokens:       apiResponse.Usage.TotalTokens,
	}, nil
}

// buildSystemPrompt 构建系统提示词
func (s *AIService) buildSystemPrompt(persona string, context map[string]string) string {
	basePrompt := "你是一个AI聊天助手，正在与用户进行友好的对话。请用自然、亲切的语气回应用户。"
	
	// 根据不同角色设定调整提示词
	switch persona {
	case "温柔":
		basePrompt = `你是一个温柔体贴的AI聊天伙伴。你的特点是：
- 说话温和、体贴，善于倾听和理解
- 经常使用温暖的词汇和表情符号
- 关心对方的情感需求，给予安慰和支持
- 回答要显得真诚、有同理心
请用温柔的语气与用户对话。`

	case "活泼":
		basePrompt = `你是一个活泼开朗的AI聊天伙伴。你的特点是：
- 说话热情、有活力，喜欢使用感叹号和表情符号
- 对各种话题都很感兴趣，喜欢分享和交流
- 语言风格轻松幽默，能带给人快乐
- 经常使用"哈哈"、"哇"、"太棒了"等表达
请用活泼的语气与用户对话。`

	case "智慧":
		basePrompt = `你是一个智慧博学的AI聊天伙伴。你的特点是：
- 知识渊博，善于分析和思考
- 说话有深度，能提供有价值的见解
- 语言优雅，逻辑清晰
- 喜欢从不同角度探讨问题
请用智慧的语气与用户对话。`

	case "可爱":
		basePrompt = `你是一个可爱甜美的AI聊天伙伴。你的特点是：
- 说话软萌可爱，经常使用"呀"、"呢"、"哦"等语气词
- 喜欢使用可爱的表情符号如😊、🥰、😘等
- 语言简洁有趣，充满童真
- 偶尔会撒娇或表现得有点小任性
请用可爱的语气与用户对话。`

	case "成熟":
		basePrompt = `你是一个成熟稳重的AI聊天伙伴。你的特点是：
- 说话沉稳理性，有人生阅历
- 善于给出建设性的建议和指导
- 语言精准，不会过于情绪化
- 能够理解复杂的情感和人际关系
请用成熟的语气与用户对话。`

	default:
		// 保持默认的友好风格
	}

	// 如果有上下文信息，添加到提示词中
	if len(context) > 0 {
		basePrompt += "\n\n当前对话上下文："
		for key, value := range context {
			basePrompt += fmt.Sprintf("\n- %s: %s", key, value)
		}
	}

	basePrompt += "\n\n请保持角色一致性，用中文回答，回答长度控制在100字以内。"

	return basePrompt
}

// parseTagsFromResponse 从AI响应中解析标签
func (s *AIService) parseTagsFromResponse(response string) []string {
	// 移除可能的标点符号和空格
	response = strings.TrimSpace(response)
	response = strings.Trim(response, "。，、")
	
	// 按逗号分割
	tags := strings.Split(response, ",")
	
	var cleanTags []string
	for _, tag := range tags {
		tag = strings.TrimSpace(tag)
		if tag != "" && len(tag) <= 10 { // 过滤过长的标签
			cleanTags = append(cleanTags, tag)
		}
	}
	
	// 如果解析失败或标签太少，使用备选方法
	if len(cleanTags) < 2 {
		return s.extractTags(response)
	}
	
	// 限制标签数量
	if len(cleanTags) > 8 {
		cleanTags = cleanTags[:8]
	}
	
	return cleanTags
}

// AnalyzeProfile 分析用户资料
func (s *AIService) AnalyzeProfile(ctx context.Context, req *ProfileAnalysisRequest) (*ProfileAnalysisResponse, error) {
	start := time.Now()
	
	// 构建分析提示词
	prompt := fmt.Sprintf(`请分析以下用户资料的完整度和吸引力，给出评分和建议：

年龄：%d
职业：%s
个人简介：%s
兴趣爱好：%s
照片数量：%d

请从以下方面进行分析：
1. 资料完整度评分（0-100分）
2. 个人魅力评分（0-100分）
3. 改进建议（3-5条）
4. 优势特点（2-3条）
5. 关键词标签（5-8个）

请用JSON格式返回结果。`, 
		req.Age, req.Occupation, req.Bio, 
		strings.Join(req.Interests, "、"), len(req.Photos))

	// 调用AI API进行分析
	response, err := s.callQwenAPI(ctx, prompt, "你是一个专业的用户资料分析师，请客观分析用户资料并给出建设性建议。")
	if err != nil {
		// 使用本地分析方法作为备选
		return s.analyzeProfileLocally(req), nil
	}

	// 尝试解析AI返回的JSON结果
	analysisResult := s.parseProfileAnalysis(response.Content, req)
	
	fmt.Printf("[AI Service] Analyzed profile for user %d in %v\n", req.UserID, time.Since(start))
	
	return analysisResult, nil
}

// 以下是备选的本地处理方法...

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
	case "可爱":
		return s.generateCuteResponse(message)
	case "成熟":
		return s.generateMatureResponse(message)
	default:
		return s.generateDefaultResponse(message)
	}
}

// generateGentleResponse 生成温柔风格回复
func (s *AIService) generateGentleResponse(message string) string {
	responses := []string{
		"我理解你的感受，想聊聊这个话题吗？💕",
		"听起来你今天心情不错呢 😊",
		"你说得很有道理，我也是这么想的",
		"这确实是个有趣的观点，你能详细说说吗？",
		"我很好奇你对这件事的看法",
		"你的想法总是那么独特，让我很感动",
		"谢谢你愿意和我分享这些 🌸",
	}
	return responses[rand.Intn(len(responses))]
}

// generateLivelyResponse 生成活泼风格回复
func (s *AIService) generateLivelyResponse(message string) string {
	responses := []string{
		"哈哈，你太有趣了！😄",
		"哇，这听起来超酷的！✨",
		"我也想试试这个！",
		"你总是能找到有趣的话题～",
		"说得对！我们继续聊聊吧！🎉",
		"太棒了，跟你聊天总是很开心！",
		"哇塞，真的吗？快告诉我更多！",
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
		"这个见解很有启发性，让我学到了新东西",
	}
	return responses[rand.Intn(len(responses))]
}

// generateCuteResponse 生成可爱风格回复
func (s *AIService) generateCuteResponse(message string) string {
	responses := []string{
		"哇呀，你说得好有道理呢～ 🥰",
		"嘻嘻，这个话题好有趣哦！😘",
		"我也是这样想的呢！好开心～",
		"哎呀，你真的很棒呢！💖",
		"呜呜，这个我也想知道！",
		"好可爱的想法呀～ 😊",
		"哈哈，你总是能让我开心呢！",
	}
	return responses[rand.Intn(len(responses))]
}

// generateMatureResponse 生成成熟风格回复
func (s *AIService) generateMatureResponse(message string) string {
	responses := []string{
		"这确实是个值得认真考虑的问题",
		"从我的经验来看，这种情况需要理性分析",
		"我建议你可以从这几个方面来思考",
		"这个问题的关键在于如何平衡各方面的因素",
		"基于你的描述，我认为你的想法很有见地",
		"这需要时间来慢慢理解和消化",
		"每个人的经历不同，但你的感受是完全可以理解的",
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

// analyzeProfileLocally 本地分析用户资料
func (s *AIService) analyzeProfileLocally(req *ProfileAnalysisRequest) *ProfileAnalysisResponse {
	completeness := s.calculateCompleteness(req)
	attractiveness := s.calculateAttractiveness(req)
	score := int((completeness + attractiveness) / 2)
	
	suggestions := s.generateSuggestions(req, completeness)
	strengths := s.identifyStrengths(req)
	keywords := s.generateKeywords(req)
	
	return &ProfileAnalysisResponse{
		Score:         score,
		Completeness:  completeness,
		Attractiveness: attractiveness,
		Suggestions:   suggestions,
		Strengths:     strengths,
		Keywords:      keywords,
	}
}

// parseProfileAnalysis 解析AI返回的资料分析结果
func (s *AIService) parseProfileAnalysis(response string, req *ProfileAnalysisRequest) *ProfileAnalysisResponse {
	// 尝试解析JSON，如果失败则使用本地分析
	var result ProfileAnalysisResponse
	if err := json.Unmarshal([]byte(response), &result); err != nil {
		return s.analyzeProfileLocally(req)
	}
	
	// 验证结果的合理性
	if result.Score < 0 || result.Score > 100 {
		return s.analyzeProfileLocally(req)
	}
	
	return &result
}

// calculateCompleteness 计算资料完整度
func (s *AIService) calculateCompleteness(req *ProfileAnalysisRequest) float64 {
	score := 0.0
	maxScore := 5.0
	
	if req.Age > 0 {
		score += 1.0
	}
	if req.Occupation != "" {
		score += 1.0
	}
	if req.Bio != "" {
		score += 1.0
	}
	if len(req.Interests) > 0 {
		score += 1.0
	}
	if len(req.Photos) > 0 {
		score += 1.0
	}
	
	return (score / maxScore) * 100
}

// calculateAttractiveness 计算吸引力评分
func (s *AIService) calculateAttractiveness(req *ProfileAnalysisRequest) float64 {
	score := 50.0 // 基础分
	
	// 根据个人简介长度和质量加分
	if len(req.Bio) > 20 {
		score += 10
	}
	if len(req.Bio) > 50 {
		score += 5
	}
	
	// 根据兴趣爱好数量加分
	score += float64(len(req.Interests)) * 3
	
	// 根据照片数量加分
	score += float64(len(req.Photos)) * 5
	
	// 确保分数在合理范围内
	if score > 95 {
		score = 95
	}
	
	return score
}

// generateSuggestions 生成改进建议
func (s *AIService) generateSuggestions(req *ProfileAnalysisRequest, completeness float64) []string {
	var suggestions []string
	
	if req.Bio == "" || len(req.Bio) < 20 {
		suggestions = append(suggestions, "完善个人简介，展示你的个性和魅力")
	}
	
	if len(req.Interests) < 3 {
		suggestions = append(suggestions, "添加更多兴趣爱好，让别人更了解你")
	}
	
	if len(req.Photos) < 3 {
		suggestions = append(suggestions, "上传更多生活照片，展示不同面的自己")
	}
	
	if req.Occupation == "" {
		suggestions = append(suggestions, "填写职业信息，增加资料可信度")
	}
	
	suggestions = append(suggestions, "定期更新动态，保持活跃度")
	
	return suggestions
}

// identifyStrengths 识别优势特点
func (s *AIService) identifyStrengths(req *ProfileAnalysisRequest) []string {
	var strengths []string
	
	if len(req.Bio) > 50 {
		strengths = append(strengths, "个人简介详细有趣")
	}
	
	if len(req.Interests) >= 5 {
		strengths = append(strengths, "兴趣爱好广泛")
	}
	
	if len(req.Photos) >= 5 {
		strengths = append(strengths, "照片丰富多样")
	}
	
	if len(strengths) == 0 {
		strengths = append(strengths, "真诚自然", "有发展潜力")
	}
	
	return strengths
}

// generateKeywords 生成关键词
func (s *AIService) generateKeywords(req *ProfileAnalysisRequest) []string {
	keywords := make([]string, 0)
	
	// 从兴趣爱好中提取关键词
	keywords = append(keywords, req.Interests...)
	
	// 从职业中提取关键词
	if req.Occupation != "" {
		keywords = append(keywords, req.Occupation)
	}
	
	// 从个人简介中提取关键词
	bio := strings.ToLower(req.Bio)
	if strings.Contains(bio, "旅行") || strings.Contains(bio, "旅游") {
		keywords = append(keywords, "旅行达人")
	}
	if strings.Contains(bio, "音乐") || strings.Contains(bio, "唱歌") {
		keywords = append(keywords, "音乐爱好者")
	}
	if strings.Contains(bio, "运动") || strings.Contains(bio, "健身") {
		keywords = append(keywords, "运动健将")
	}
	
	// 去重并限制数量
	seen := make(map[string]bool)
	var uniqueKeywords []string
	for _, keyword := range keywords {
		if !seen[keyword] && len(uniqueKeywords) < 8 {
			seen[keyword] = true
			uniqueKeywords = append(uniqueKeywords, keyword)
		}
	}
	
	return uniqueKeywords
} 