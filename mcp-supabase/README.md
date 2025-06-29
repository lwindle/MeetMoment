# 🔗 MeetMoment Supabase MCP 服务器

这是一个为 Cursor IDE 设计的 Supabase MCP 服务器，让你可以直接在 Cursor 中查询和操作 Supabase 数据库。

## 🚀 快速开始

### 1. 配置 Supabase 信息

编辑 Cursor 的 MCP 配置文件 `~/.cursor/mcp.json`，填入你的 Supabase 项目信息：

```json
{
  "mcpServers": {
    "meetmoment-supabase": {
      "command": "python3",
      "args": ["/Users/lwindle/GolandProjects/MeetMoment/mcp-supabase/server.py"],
      "env": {
        "SUPABASE_URL": "https://your-project-ref.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

### 2. 获取 Supabase 配置信息

从你的 Supabase 项目仪表板获取：

1. **Project URL**: 在 Settings > API 中找到
2. **Service Role Key**: 在 Settings > API 中找到（⚠️ 注意：这是敏感信息）

### 3. 重启 Cursor

配置完成后，重启 Cursor IDE 以加载 MCP 服务器。

## 📖 使用方法

在 Cursor 中，你可以直接使用自然语言查询 Supabase 数据：

### 查询数据示例

```
"查询 users 表中的所有用户"
"显示前 10 个用户的昵称和城市"
"查找城市为北京的用户"
"获取 ID 为 1 的用户信息"
```

### 插入数据示例

```
"在 users 表中插入一个新用户"
"添加一个用户，手机号 13800138000，昵称为测试用户"
```

## 🛠️ 可用工具

### 1. supabase_query
查询数据库表

**参数：**
- `table` (必需): 表名
- `select` (可选): 选择的列，默认为 "*"
- `filters` (可选): 过滤条件，如 `{"city": "北京"}`
- `limit` (可选): 限制返回行数

**示例：**
```json
{
  "table": "users",
  "select": "id, nickname, city",
  "filters": {"city": "北京"},
  "limit": 10
}
```

### 2. supabase_insert
插入数据到表

**参数：**
- `table` (必需): 表名
- `data` (必需): 要插入的数据对象

**示例：**
```json
{
  "table": "users",
  "data": {
    "phone": "13800138000",
    "nickname": "新用户",
    "city": "上海"
  }
}
```

## 🗄️ 数据库表结构

MeetMoment 项目包含以下主要表：

### 用户相关
- `users` - 用户基本信息
- `user_photos` - 用户照片
- `user_interests` - 用户兴趣标签

### 匹配相关
- `matches` - 用户匹配记录

### 聊天相关
- `conversations` - 会话
- `messages` - 消息记录

### 社交圈子
- `circles` - 圈子信息
- `circle_members` - 圈子成员
- `circle_posts` - 圈子动态

## 💡 使用技巧

### 1. 自然语言查询
你可以用自然语言描述你想要的数据，MCP 会自动转换为相应的查询：

- "显示最近注册的 5 个用户"
- "查找有多少个用户来自北京"
- "获取用户 ID 1 的所有照片"

### 2. 数据分析
利用 MCP 进行数据分析：

- "统计每个城市的用户数量"
- "查看最活跃的圈子"
- "分析用户的兴趣标签分布"

### 3. 数据管理
进行数据管理操作：

- "添加测试用户数据"
- "更新用户信息"
- "清理无效数据"

## 🔧 故障排除

### 1. 连接失败
如果 MCP 服务器无法连接到 Supabase：

1. 检查 `SUPABASE_URL` 是否正确
2. 确认 `SUPABASE_SERVICE_ROLE_KEY` 是否有效
3. 验证网络连接

### 2. 权限错误
如果遇到权限问题：

1. 确保使用的是 `service_role` 密钥，不是 `anon` 密钥
2. 检查 Supabase 项目的 RLS 政策
3. 确认数据库表的访问权限

### 3. 查询失败
如果查询返回错误：

1. 检查表名是否正确
2. 确认列名存在
3. 验证过滤条件格式

### 4. 调试模式
如果需要调试，可以直接运行 MCP 服务器：

```bash
cd /Users/lwindle/GolandProjects/MeetMoment/mcp-supabase
export SUPABASE_URL="your-url"
export SUPABASE_SERVICE_ROLE_KEY="your-key"
python3 server.py
```

然后手动输入 JSON 请求进行测试。

## 🔐 安全注意事项

1. **密钥保护**: `service_role` 密钥具有完全访问权限，请妥善保管
2. **本地使用**: 此 MCP 服务器仅供本地开发使用
3. **数据备份**: 在进行数据修改前，建议备份重要数据

## 📚 更多资源

- [Supabase 官方文档](https://supabase.com/docs)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Cursor IDE 文档](https://cursor.sh/docs)

---

**现在你可以在 Cursor 中直接查询 Supabase 数据了！** 🎉 