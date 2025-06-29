# 🎉 MeetMoment - AI交友网站

一个现代化的AI交友平台，帮助用户通过智能匹配找到志同道合的朋友。

## 🆕 重要更新: 已迁移至 Supabase + MCP 支持

项目已从 MySQL 迁移至 **Supabase** 作为后端数据存储解决方案，并新增 **MCP (Model Context Protocol)** 支持：

### 🎯 Supabase 优势
- ✅ **托管的 PostgreSQL 数据库** - 无需自维护数据库
- ✅ **内置文件存储** - 用户头像和照片上传
- ✅ **实时功能** - 消息推送和在线状态
- ✅ **认证服务** - 可选的 Supabase Auth 集成
- ✅ **自动备份** - 数据安全有保障
- ✅ **全球 CDN** - 文件访问更快速

### 🔗 MCP 集成
- ✅ **Claude Desktop 集成** - 直接在 Claude 中操作数据库
- ✅ **智能数据查询** - 自然语言查询 Supabase 数据
- ✅ **文件管理** - 通过 AI 管理存储文件
- ✅ **实时协作** - AI 辅助的数据库操作

## 🏗️ 技术栈

### 前端
- **Next.js 15** - React 框架
- **React 19** - 用户界面库
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **Radix UI** - 组件库

### 后端
- **Go 1.21** - 后端编程语言
- **Gin** - HTTP Web 框架
- **GORM** - ORM 库
- **JWT** - 身份认证
- **WebSocket** - 实时通信

### 数据库 & 存储
- **Supabase PostgreSQL** - 主数据库
- **Supabase Storage** - 文件存储
- **Redis** - 缓存和会话管理

### 部署
- **Docker** - 容器化
- **Docker Compose** - 多服务编排
- **Nginx** - 反向代理

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/MeetMoment.git
cd MeetMoment
```

### 2. 设置 Supabase

请参考 [Supabase 设置指南](docs/SUPABASE_SETUP.md) 完成以下步骤：

1. 创建 Supabase 项目
2. 获取数据库连接信息和 API 密钥
3. 运行数据库迁移 SQL
4. 设置 Storage buckets

### 3. 设置 MCP 服务器 (可选，用于 Claude Desktop 集成)

```bash
# 运行自动安装脚本
./scripts/setup-mcp.sh

# 或手动安装
cd mcp-server
npm install
npm run build
```

详细配置请查看 [MCP 服务器文档](mcp-server/README.md)。

### 4. 配置环境变量

```bash
# 复制环境配置文件
cp env.example backend/.env

# 编辑 backend/.env 文件，填入你的 Supabase 配置
```

### 5. 启动服务

#### 使用 Docker Compose (推荐)

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 本地开发

```bash
# 启动前端
cd frontend
npm install
npm run dev

# 启动后端 (新终端)
cd backend
go mod tidy
go run main.go

# 启动 Redis (新终端)
redis-server
```

### 6. 访问应用

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8080
- **Supabase Dashboard**: https://supabase.com/dashboard

## 📖 API 文档

### 认证接口

```bash
# 用户注册
POST /api/auth/register
Content-Type: application/json
{
  "phone": "13800138000",
  "password": "password123",
  "nickname": "用户昵称"
}

# 用户登录
POST /api/auth/login
Content-Type: application/json
{
  "phone": "13800138000",
  "password": "password123"
}

# 刷新令牌
POST /api/auth/refresh
Authorization: Bearer <refresh_token>

# 退出登录
POST /api/auth/logout
Authorization: Bearer <access_token>
```

### 用户接口

```bash
# 获取用户信息
GET /api/user/profile
Authorization: Bearer <access_token>

# 更新用户信息
PUT /api/user/profile
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "nickname": "新昵称",
  "bio": "个人简介"
}

# 上传照片
POST /api/user/upload-photo
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
photo: <file>
```

### 匹配接口

```bash
# 获取推荐用户
GET /api/match/recommendations
Authorization: Bearer <access_token>

# 喜欢用户
POST /api/match/like
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "target_user_id": 123
}

# 获取匹配列表
GET /api/match/matches
Authorization: Bearer <access_token>
```

## 🌟 核心功能

### ✅ 已实现功能

1. **用户认证**
   - 手机号注册/登录
   - JWT 身份验证
   - 令牌刷新机制

2. **用户资料**
   - 个人信息管理
   - 照片上传 (Supabase Storage)
   - AI 生成兴趣标签

3. **智能匹配**
   - 基于地理位置的推荐
   - 兴趣相似度匹配
   - 喜欢/跳过机制

4. **实时聊天**
   - WebSocket 实时消息
   - 消息历史记录
   - AI 聊天助手

5. **社交圈子**
   - 兴趣圈子功能
   - 动态发布和互动
   - 圈子成员管理

### 🔄 计划中功能

- [ ] 视频通话集成
- [ ] 地理位置服务
- [ ] 推送通知
- [ ] 高级匹配算法
- [ ] 内容审核系统

## 🗂️ 项目结构

```
MeetMoment/
├── app/                    # Next.js 前端应用
│   ├── components/         # React 组件
│   ├── globals.css        # 全局样式
│   ├── layout.tsx         # 应用布局
│   └── page.tsx           # 首页
├── backend/               # Go 后端服务
│   ├── config/           # 配置管理
│   ├── database/         # 数据库连接
│   ├── handlers/         # HTTP 处理器
│   ├── middleware/       # 中间件
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑
│   └── main.go          # 应用入口
├── components/           # 共享 UI 组件
├── docs/                # 文档
│   └── SUPABASE_SETUP.md # Supabase 设置指南
├── mcp-server/          # MCP 服务器
│   ├── src/            # MCP 服务器源码
│   ├── package.json    # MCP 依赖配置
│   └── README.md       # MCP 使用指南
├── scripts/            # 工具脚本
│   └── setup-mcp.sh    # MCP 自动安装脚本
├── docker-compose.yml   # Docker 编排
├── env.example         # 环境配置示例
└── README.md           # 项目说明
```

## 🛠️ 开发指南

### 本地开发环境

1. **前端开发**
   ```bash
   cd app
   npm run dev
   ```

2. **后端开发**
   ```bash
   cd backend
   go run main.go
   ```

3. **数据库迁移**
   - 应用会自动执行数据库迁移
   - 手动迁移请参考 [Supabase 设置指南](docs/SUPABASE_SETUP.md)

### 代码规范

- 使用 TypeScript 进行前端开发
- 遵循 Go 语言最佳实践
- 提交前运行代码格式化和测试

## 🔧 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 Supabase 配置是否正确
   - 确认网络连接正常

2. **文件上传失败**
   - 验证 Supabase Storage 设置
   - 检查文件大小限制

3. **认证失败**
   - 确认 JWT 密钥配置
   - 检查令牌是否过期

详细的故障排除指南请参考 [Supabase 设置指南](docs/SUPABASE_SETUP.md)。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系我们

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/yourusername/MeetMoment/issues)
- 发送邮件至 your-email@example.com

---

**享受你的 AI 交友之旅！** 🎉