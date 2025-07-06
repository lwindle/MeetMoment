# 阿里云通义万相集成使用指南

本文档介绍如何使用阿里云通义万相API生成美女头像和用户数据。

## 🚀 快速开始

### 1. 获取阿里云API密钥

1. 访问[阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 开通通义万相-文生图V2版服务
3. 获取API Key (DashScope API Key)

### 2. 配置环境变量

```bash
# 设置阿里云API密钥
export DASHSCOPE_API_KEY="your-dashscope-api-key"

# 设置Supabase配置（如果还没有）
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### 3. 运行美女用户生成脚本

```bash
cd mcp-supabase
python3 generate_beauty_users.py
```

## 📋 功能特性

### 🎨 AI图像生成
- 使用通义万相wanx2.1-t2i-turbo模型
- 高质量1024x1024分辨率
- 中文提示词优化
- 负面提示词过滤

### 👥 用户数据生成
- 10个不同风格的美女用户
- 真实的个人信息和自我介绍
- 多样化的职业和兴趣爱好
- 自动生成兴趣标签

### 🔄 异步处理
- 支持异步任务创建和查询
- 智能等待机制
- API限流保护

## 🛠️ API接口

### 后端API接口

#### 1. 生成图片任务
```http
POST /api/aliyun/generate-image
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "prompt": "高清写实美女头像摄影，温柔甜美的女孩"
}
```

响应：
```json
{
  "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx"
}
```

#### 2. 查询任务状态
```http
POST /api/aliyun/query-task
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx"
}
```

响应：
```json
{
  "output": {
    "task_status": "SUCCEEDED",
    "results": [{
      "url": "https://dashscope-result-xxx.oss-cn-xxx.aliyuncs.com/xxx.png"
    }]
  }
}
```

#### 3. 生成美女头像（同步）
```http
POST /api/aliyun/generate-beauty-portrait
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "description": "温柔甜美的女孩，长发飘逸，穿着简约白色上衣"
}
```

响应：
```json
{
  "image_url": "https://dashscope-result-xxx.oss-cn-xxx.aliyuncs.com/xxx.png"
}
```

## 👩‍💼 生成的用户类型

脚本会生成以下10种不同类型的美女用户：

1. **小雨** - UI设计师，上海，24岁
   - 温柔甜美，热爱设计和摄影

2. **艾米** - 产品经理，北京，26岁
   - 知性优雅，科技控，爱健身

3. **婷婷** - 插画师，杭州，23岁
   - 文艺清新，艺术系毕业

4. **欣欣** - 金融分析师，深圳，25岁
   - 理性感性并存，喜欢烘焙

5. **小柠檬** - 大学生，成都，22岁
   - 青春活泼，心理学专业

6. **安娜** - 市场营销，广州，27岁
   - 时尚靓丽，热爱生活

7. **思思** - 教师，南京，24岁
   - 温婉知性，喜欢古典文学

8. **小鹿** - 护士，西安，23岁
   - 清纯可爱，有爱心

9. **梦琪** - 律师助理，武汉，26岁
   - 干练优雅，坚强独立

10. **糖糖** - 甜品师，重庆，25岁
    - 甜美可爱，开甜品店

## 💰 费用说明

根据[阿里云通义万相定价](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)：

- **wanx2.1-t2i-turbo**: 0.14元/张
- **免费额度**: 新用户500张，有效期180天
- **生成10个用户**: 约1.4元（如果超出免费额度）

## ⚠️ 注意事项

### 1. API限流
- QPS限制：2次/秒
- 同时处理任务数：2个
- 脚本内置30秒等待避免限流

### 2. 图片有效期
- 生成的图片链接有效期24小时
- 建议及时下载或上传到自己的存储服务

### 3. 内容审核
- 阿里云会对生成内容进行审核
- 避免包含敏感或不当内容的提示词

### 4. 网络访问
如果无法访问阿里云OSS链接，需要配置白名单：
```
dashscope-result-bj.oss-cn-beijing.aliyuncs.com
dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com
dashscope-result-sh.oss-cn-shanghai.aliyuncs.com
dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com
```

## 🔧 故障排除

### 1. API密钥错误
```
❌ 请设置 DASHSCOPE_API_KEY 环境变量
```
解决：确保正确设置了阿里云API密钥

### 2. 任务失败
```
❌ 创建用户 xxx 时出错: 任务失败
```
解决：检查提示词是否包含敏感内容，或稍后重试

### 3. 数据库连接失败
```
❌ 插入用户失败: 401 - Unauthorized
```
解决：检查Supabase服务角色密钥是否正确

### 4. 网络超时
```
❌ 任务超时
```
解决：检查网络连接，或增加超时时间

## 🎯 使用建议

1. **首次使用**：建议先生成1-2个用户测试
2. **批量生成**：避免短时间内大量请求
3. **图片保存**：及时将生成的图片保存到持久化存储
4. **提示词优化**：根据需要调整描述文本获得更好效果

## 📞 技术支持

如果遇到问题，请检查：
1. API密钥是否正确配置
2. 网络连接是否正常
3. Supabase数据库是否可访问
4. 是否有足够的API配额

更多技术细节请参考[阿里云通义万相官方文档](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)。 