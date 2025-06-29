# 🚀 Supabase 设置指南

本指南将帮你为 MeetMoment 项目设置 Supabase 数据库和存储。

## 📋 前提条件

- 一个 [Supabase](https://supabase.com) 账户
- 基本的 SQL 知识

## 🔧 步骤 1: 创建 Supabase 项目

1. 登录 [Supabase Dashboard](https://supabase.com/dashboard)
2. 点击 "New Project"
3. 选择你的组织
4. 填写项目信息：
   - **Name**: `meetmoment`
   - **Database Password**: 创建一个强密码（记住这个密码！）
   - **Region**: 选择离你最近的区域
5. 点击 "Create new project"

## 🔑 步骤 2: 获取项目凭据

项目创建完成后，前往 **Settings > API**：

```bash
# 你需要的凭据
Project URL: https://your-project-ref.supabase.co
anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🗄️ 步骤 3: 设置数据库

### 获取数据库连接字符串

前往 **Settings > Database**，复制连接字符串：

```
postgres://postgres:[YOUR-PASSWORD]@db.your-project-ref.supabase.co:5432/postgres
```

### 创建数据库表

在 Supabase SQL Editor 中运行以下 SQL 来创建所需的表：

```sql
-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(100) NOT NULL,
    gender INTEGER DEFAULT 0,
    age INTEGER,
    city VARCHAR(100),
    occupation VARCHAR(100),
    bio TEXT,
    emotion_status VARCHAR(50),
    avatar VARCHAR(500),
    verified BOOLEAN DEFAULT FALSE,
    is_online BOOLEAN DEFAULT FALSE,
    last_active_time TIMESTAMP,
    ai_score INTEGER DEFAULT 0,
    profile_complete DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 用户照片表
CREATE TABLE user_photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 用户兴趣表
CREATE TABLE user_interests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 匹配表
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    target_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(20) NOT NULL,
    is_matched BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(user_id, target_user_id)
);

-- 会话表
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL DEFAULT 'private',
    last_message_id INTEGER,
    last_message_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 会话参与者表
CREATE TABLE conversation_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(conversation_id, user_id)
);

-- 消息表
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL DEFAULT 'text',
    is_from_ai BOOLEAN DEFAULT FALSE,
    ai_response_time BIGINT,
    read_by JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- AI对话记录表
CREATE TABLE ai_conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    prompt TEXT,
    response TEXT,
    ai_model VARCHAR(100),
    response_time BIGINT,
    tokens INTEGER,
    context JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 圈子表
CREATE TABLE circles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    cover_image VARCHAR(500),
    is_public BOOLEAN DEFAULT TRUE,
    member_count INTEGER DEFAULT 0,
    post_count INTEGER DEFAULT 0,
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 圈子成员表
CREATE TABLE circle_members (
    id SERIAL PRIMARY KEY,
    circle_id INTEGER REFERENCES circles(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(circle_id, user_id)
);

-- 圈子动态表
CREATE TABLE circle_posts (
    id SERIAL PRIMARY KEY,
    circle_id INTEGER REFERENCES circles(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    images JSONB DEFAULT '[]',
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    is_from_ai BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 动态评论表
CREATE TABLE post_comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES circle_posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- 动态点赞表
CREATE TABLE post_likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES circle_posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(post_id, user_id)
);

-- 创建索引以优化查询性能
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_city ON users(city);
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_user_photos_user_id ON user_photos(user_id);
CREATE INDEX idx_user_interests_user_id ON user_interests(user_id);
CREATE INDEX idx_matches_user_id ON matches(user_id);
CREATE INDEX idx_matches_target_user_id ON matches(target_user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_circle_members_circle_id ON circle_members(circle_id);
CREATE INDEX idx_circle_members_user_id ON circle_members(user_id);
CREATE INDEX idx_circle_posts_circle_id ON circle_posts(circle_id);
CREATE INDEX idx_post_comments_post_id ON post_comments(post_id);
CREATE INDEX idx_post_likes_post_id ON post_likes(post_id);

-- 更新触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要的表添加自动更新时间戳的触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_photos_updated_at BEFORE UPDATE ON user_photos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_interests_updated_at BEFORE UPDATE ON user_interests FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_matches_updated_at BEFORE UPDATE ON matches FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_messages_updated_at BEFORE UPDATE ON messages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_circles_updated_at BEFORE UPDATE ON circles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_circle_members_updated_at BEFORE UPDATE ON circle_members FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_circle_posts_updated_at BEFORE UPDATE ON circle_posts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 🗃️ 步骤 4: 设置 Storage

### 启用 Storage

1. 在 Supabase Dashboard 中前往 **Storage**
2. 如果首次使用，点击 "Start using Storage"

### 创建 Buckets

在 Supabase Dashboard 的 Storage 页面创建以下 buckets：

1. **avatars** (公开访问)
   - 用于存储用户头像
   - 设置为 Public bucket

2. **photos** (公开访问)
   - 用于存储用户照片
   - 设置为 Public bucket

3. **documents** (私有访问)
   - 用于存储文档文件
   - 设置为 Private bucket

### 设置 Storage 政策 (RLS)

在 SQL Editor 中运行以下命令来设置存储策略：

```sql
-- 为 avatars bucket 设置策略
INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true);
INSERT INTO storage.buckets (id, name, public) VALUES ('photos', 'photos', true);
INSERT INTO storage.buckets (id, name, public) VALUES ('documents', 'documents', false);

-- 允许所有用户查看公开的头像和照片
CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'avatars');
CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'photos');

-- 允许认证用户上传自己的文件
CREATE POLICY "Users can upload own avatar" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'avatars');
CREATE POLICY "Users can upload own photos" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'photos');

-- 允许用户删除自己的文件
CREATE POLICY "Users can delete own avatar" ON storage.objects FOR DELETE USING (bucket_id = 'avatars');
CREATE POLICY "Users can delete own photos" ON storage.objects FOR DELETE USING (bucket_id = 'photos');
```

## 🔐 步骤 5: 配置环境变量

### 本地开发环境

创建 `backend/.env` 文件：

```bash
# 环境配置
ENVIRONMENT=development
PORT=8080

# Supabase 数据库配置
DATABASE_URL=postgres://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres?sslmode=require

# Redis配置 (本地开发可选)
REDIS_URL=redis://localhost:6379/0

# JWT配置
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# AI配置
AI_API_KEY=your-ai-api-key-here

# 文件上传配置
FILE_UPLOAD_PATH=./uploads
MAX_FILE_SIZE=5242880

# Supabase配置
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```

### 生产环境

在 Docker Compose 或你的部署平台中设置相同的环境变量。

## 🧪 步骤 6: 测试连接

### 测试数据库连接

运行后端服务，检查日志中是否出现：

```
Supabase PostgreSQL connection established and migrated successfully
```

### 测试文件上传

1. 启动后端服务
2. 使用 API 测试工具（如 Postman）测试文件上传端点
3. 检查文件是否正确上传到 Supabase Storage

## 🔧 常见问题

### 1. 连接失败

**问题**: `failed to connect to Supabase database`

**解决方案**:
- 检查 `DATABASE_URL` 是否正确
- 确认密码中没有特殊字符需要编码
- 验证项目是否已完全部署

### 2. 文件上传失败

**问题**: 文件上传返回 403 错误

**解决方案**:
- 检查 Storage buckets 是否已创建
- 验证 RLS 政策是否正确设置
- 确认 `SUPABASE_SERVICE_ROLE_KEY` 是否正确

### 3. 表不存在

**问题**: `relation "users" does not exist`

**解决方案**:
- 确保已在 SQL Editor 中运行了所有建表语句
- 检查表名大小写是否正确
- 验证 schema 是否为 `public`

## 📚 进阶配置

### 启用实时功能

在 Supabase Dashboard 中：

1. 前往 **Database > Replication**
2. 为需要实时更新的表启用 Realtime
3. 推荐为 `messages` 和 `conversations` 表启用

### 设置 Row Level Security (RLS)

```sql
-- 启用 RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- 用户只能查看和修改自己的数据
CREATE POLICY "Users can view own data" ON users FOR SELECT USING (id = auth.uid()::integer);
CREATE POLICY "Users can update own data" ON users FOR UPDATE USING (id = auth.uid()::integer);
```

### 备份和监控

1. 在 Supabase Dashboard 中设置定期备份
2. 配置监控和告警
3. 定期检查数据库性能

## 🎉 完成！

现在你的 MeetMoment 应用已经成功配置了 Supabase 作为后端存储。你可以：

- ✅ 存储用户数据到 PostgreSQL
- ✅ 上传文件到 Supabase Storage  
- ✅ 使用实时功能进行消息推送
- ✅ 利用 Supabase 的认证和安全功能

有任何问题请参考 [Supabase 官方文档](https://supabase.com/docs) 或提交 Issue。 