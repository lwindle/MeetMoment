# MeetMoment 数据库表结构创建指南

## 🎯 目标
在 Supabase 中创建 MeetMoment AI 交友平台的完整数据库表结构。

## 📋 表结构概览

### 用户相关表 (4个)
- **users**: 用户主表
- **user_photos**: 用户照片表
- **user_interests**: 用户兴趣标签表
- **matches**: 用户匹配记录表

### 聊天相关表 (4个)
- **conversations**: 会话表
- **conversation_participants**: 会话参与者表
- **messages**: 消息表
- **ai_conversations**: AI对话记录表

### 社交圈子相关表 (5个)
- **circles**: 圈子表
- **circle_members**: 圈子成员表
- **circle_posts**: 圈子动态表
- **post_comments**: 动态评论表
- **post_likes**: 动态点赞表

## 🚀 执行步骤

### 方法一：Supabase Dashboard（推荐）

1. **打开 Supabase Dashboard**
   ```
   https://supabase.com/dashboard/project/odnalktszcfoxpcvmshw
   ```

2. **进入 SQL Editor**
   - 点击左侧菜单的 "SQL Editor"
   - 点击 "New query"

3. **执行 SQL**
   - 复制 `meetmoment_tables.sql` 文件的全部内容
   - 粘贴到 SQL Editor 中
   - 点击 "Run" 按钮执行

### 方法二：通过 MCP 协议（自动化）

由于你已经配置了 MCP，理论上可以通过以下方式自动执行：

```bash
# 使用 MCP 服务器执行（需要 Cursor 重启以加载配置）
python3 server.py
```

## 📊 执行结果验证

执行完成后，你可以通过以下方式验证：

1. **在 Supabase Dashboard 中查看**
   - 进入 "Table Editor"
   - 应该能看到所有 13 个表

2. **通过 API 验证**
   ```bash
   curl -s "https://odnalktszcfoxpcvmshw.supabase.co/rest/v1/" \
     -H "apikey: YOUR_ANON_KEY" \
     -H "Authorization: Bearer YOUR_ANON_KEY"
   ```

3. **通过 MCP 查询**
   ```bash
   python3 -c "
   import os
   os.environ['SUPABASE_URL'] = 'https://odnalktszcfoxpcvmshw.supabase.co'
   os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'YOUR_SERVICE_ROLE_KEY'
   # 然后使用 MCP 工具查询表列表
   "
   ```

## 🔧 故障排除

### 常见问题

1. **权限错误**
   - 确保使用的是 `service_role` 密钥，不是 `anon` 密钥
   - 检查密钥是否完整且有效

2. **表已存在错误**
   - SQL 中使用了 `IF NOT EXISTS`，应该不会出现此错误
   - 如果出现，说明部分表已经创建成功

3. **外键约束错误**
   - 确保按照 SQL 文件中的顺序执行
   - 主表（如 users）必须先于关联表创建

### 手动清理（如果需要）

如果需要重新创建表，可以先删除现有表：

```sql
-- 注意：这会删除所有数据！
DROP TABLE IF EXISTS post_likes CASCADE;
DROP TABLE IF EXISTS post_comments CASCADE;
DROP TABLE IF EXISTS circle_posts CASCADE;
DROP TABLE IF EXISTS circle_members CASCADE;
DROP TABLE IF EXISTS circles CASCADE;
DROP TABLE IF EXISTS ai_conversations CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversation_participants CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS user_interests CASCADE;
DROP TABLE IF EXISTS user_photos CASCADE;
DROP TABLE IF EXISTS users CASCADE;
```

## 📁 相关文件

- `meetmoment_tables.sql`: 完整的表创建 SQL 脚本
- `create_tables.sql`: 原始表结构文件
- `server.py`: MCP Supabase 服务器
- `.env`: 环境变量配置（如果存在）

## 🎉 完成确认

表结构创建完成后，你的 MeetMoment 项目就具备了：

✅ 完整的用户管理系统
✅ 智能匹配功能
✅ 实时聊天系统
✅ AI 对话集成
✅ 社交圈子功能
✅ 优化的数据库索引
✅ 软删除支持
✅ 时间戳追踪

现在可以开始开发和测试你的 AI 交友平台了！
