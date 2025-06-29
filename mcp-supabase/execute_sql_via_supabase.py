#!/usr/bin/env python3
"""
通过 Supabase SQL 执行器创建 MeetMoment 表结构
"""
import os
import sys
import subprocess
import json
import time

# 设置环境变量
os.environ['SUPABASE_URL'] = 'https://odnalktszcfoxpcvmshw.supabase.co'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8'

def execute_sql(sql_query, description=""):
    """通过 Supabase RPC 执行 SQL"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    print(f"\n🔄 执行: {description}")
    print(f"SQL: {sql_query[:100]}..." if len(sql_query) > 100 else f"SQL: {sql_query}")
    
    # 使用 Supabase RPC 执行 SQL
    rpc_url = f"{url}/rest/v1/rpc/exec_sql"
    
    payload = {
        "sql": sql_query
    }
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        rpc_url,
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            response = result.stdout.strip()
            if response and not response.startswith('{"'):
                print(f"✅ 成功: {description}")
                return True
            elif 'error' in response.lower():
                print(f"❌ SQL 错误: {response}")
                return False
            else:
                print(f"✅ 成功: {description}")
                return True
        else:
            print(f"❌ 执行失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def execute_sql_direct(sql_query, description=""):
    """直接通过 psql 执行 SQL（如果可用）"""
    print(f"\n🔄 执行: {description}")
    
    # 构建 PostgreSQL 连接字符串
    # 从 Supabase URL 提取连接信息
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    # Supabase 的 PostgreSQL 连接信息
    # 格式: postgres://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
    project_ref = url.replace('https://', '').replace('.supabase.co', '')
    
    # 这里需要数据库密码，通常在 Supabase Dashboard 的 Settings > Database 中找到
    # 由于我们没有密码，我们使用 REST API 方式
    
    return execute_via_rest_api(sql_query, description)

def execute_via_rest_api(sql_query, description=""):
    """通过 REST API 执行 SQL"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    print(f"\n🔄 执行: {description}")
    
    # 对于 DDL 语句，我们需要使用不同的方法
    # 尝试通过 HTTP POST 到特定端点
    
    # 先尝试检查表是否存在
    if "CREATE TABLE" in sql_query:
        table_name = extract_table_name(sql_query)
        if table_name and check_table_exists(table_name):
            print(f"ℹ️  表 {table_name} 已存在，跳过创建")
            return True
    
    # 由于 Supabase REST API 不直接支持任意 SQL 执行，
    # 我们需要将 SQL 写入文件，然后建议用户在 Supabase Dashboard 中执行
    
    print(f"📝 SQL 语句已准备好，需要在 Supabase Dashboard 的 SQL Editor 中执行")
    return True

def extract_table_name(sql_query):
    """从 CREATE TABLE 语句中提取表名"""
    import re
    match = re.search(r'CREATE TABLE.*?(\w+)\s*\(', sql_query, re.IGNORECASE)
    return match.group(1) if match else None

def check_table_exists(table_name):
    """检查表是否存在"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    cmd = [
        'curl', '-s',
        f'{url}/rest/v1/{table_name}?limit=0',
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and 'error' not in result.stdout.lower()
    except:
        return False

# 分步创建表的 SQL 语句
CREATION_STEPS = [
    {
        "description": "启用 UUID 扩展",
        "sql": 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
    },
    {
        "description": "创建用户主表",
        "sql": """
CREATE TABLE IF NOT EXISTS users (
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
);"""
    },
    {
        "description": "创建用户照片表",
        "sql": """
CREATE TABLE IF NOT EXISTS user_photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);"""
    },
    {
        "description": "创建用户兴趣表",
        "sql": """
CREATE TABLE IF NOT EXISTS user_interests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);"""
    },
    {
        "description": "创建匹配表",
        "sql": """
CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    target_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(20) NOT NULL,
    is_matched BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(user_id, target_user_id)
);"""
    },
    {
        "description": "创建会话表",
        "sql": """
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL DEFAULT 'private',
    last_message_id INTEGER,
    last_message_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);"""
    },
    {
        "description": "创建会话参与者表",
        "sql": """
CREATE TABLE IF NOT EXISTS conversation_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(conversation_id, user_id)
);"""
    },
    {
        "description": "创建消息表",
        "sql": """
CREATE TABLE IF NOT EXISTS messages (
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
);"""
    },
    {
        "description": "创建 AI 对话记录表",
        "sql": """
CREATE TABLE IF NOT EXISTS ai_conversations (
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
);"""
    },
    {
        "description": "创建圈子表",
        "sql": """
CREATE TABLE IF NOT EXISTS circles (
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
);"""
    },
    {
        "description": "创建圈子成员表",
        "sql": """
CREATE TABLE IF NOT EXISTS circle_members (
    id SERIAL PRIMARY KEY,
    circle_id INTEGER REFERENCES circles(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(circle_id, user_id)
);"""
    },
    {
        "description": "创建圈子动态表",
        "sql": """
CREATE TABLE IF NOT EXISTS circle_posts (
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
);"""
    },
    {
        "description": "创建动态评论表",
        "sql": """
CREATE TABLE IF NOT EXISTS post_comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES circle_posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);"""
    },
    {
        "description": "创建动态点赞表",
        "sql": """
CREATE TABLE IF NOT EXISTS post_likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES circle_posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    UNIQUE(post_id, user_id)
);"""
    },
    {
        "description": "创建索引",
        "sql": """
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
CREATE INDEX IF NOT EXISTS idx_users_city ON users(city);
CREATE INDEX IF NOT EXISTS idx_users_age ON users(age);
CREATE INDEX IF NOT EXISTS idx_user_photos_user_id ON user_photos(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interests_user_id ON user_interests(user_id);
CREATE INDEX IF NOT EXISTS idx_matches_user_id ON matches(user_id);
CREATE INDEX IF NOT EXISTS idx_matches_target_user_id ON matches(target_user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_circle_members_circle_id ON circle_members(circle_id);
CREATE INDEX IF NOT EXISTS idx_circle_members_user_id ON circle_members(user_id);
CREATE INDEX IF NOT EXISTS idx_circle_posts_circle_id ON circle_posts(circle_id);
CREATE INDEX IF NOT EXISTS idx_post_comments_post_id ON post_comments(post_id);
CREATE INDEX IF NOT EXISTS idx_post_likes_post_id ON post_likes(post_id);"""
    }
]

def main():
    print("🚀 开始创建 MeetMoment 数据库表结构...")
    
    # 将所有 SQL 写入文件，供手动执行
    with open('meetmoment_tables.sql', 'w', encoding='utf-8') as f:
        f.write("-- MeetMoment 数据库表结构\n")
        f.write("-- 请在 Supabase Dashboard 的 SQL Editor 中执行此文件\n\n")
        
        for step in CREATION_STEPS:
            f.write(f"-- {step['description']}\n")
            f.write(step['sql'].strip() + "\n\n")
    
    print("📝 所有 SQL 语句已写入 meetmoment_tables.sql 文件")
    print("\n📋 请按照以下步骤操作:")
    print("1. 打开 Supabase Dashboard: https://supabase.com/dashboard")
    print("2. 选择你的项目: odnalktszcfoxpcvmshw")
    print("3. 点击左侧菜单的 'SQL Editor'")
    print("4. 点击 'New query'")
    print("5. 复制 meetmoment_tables.sql 文件的内容到编辑器中")
    print("6. 点击 'Run' 按钮执行")
    
    print("\n🔍 或者，你可以逐步执行以下 SQL 语句:")
    
    for i, step in enumerate(CREATION_STEPS, 1):
        print(f"\n--- 步骤 {i}: {step['description']} ---")
        print(step['sql'].strip())
        
        # 可选：尝试自动执行（如果有合适的方法）
        # execute_via_rest_api(step['sql'], step['description'])
        
        time.sleep(0.5)
    
    print("\n✅ 表结构定义完成！")
    print("📄 完整的 SQL 文件: meetmoment_tables.sql")

if __name__ == "__main__":
    main()
