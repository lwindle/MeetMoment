#!/bin/bash

# MeetMoment Supabase MCP for Cursor 设置脚本

echo "🚀 设置 MeetMoment Supabase MCP 服务器..."

# 获取当前目录
CURRENT_DIR="$(pwd)"
MCP_SERVER_PATH="$CURRENT_DIR/mcp-supabase/server.py"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请安装 Python 3: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 已安装: $(python3 --version)"

# 检查 curl
if ! command -v curl &> /dev/null; then
    echo "❌ 错误: 未找到 curl"
    echo "请安装 curl 或使用 Homebrew: brew install curl"
    exit 1
fi

echo "✅ curl 已安装"

# 检查 MCP 服务器文件
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ 错误: 未找到 MCP 服务器文件"
    echo "请确保在 MeetMoment 项目根目录运行此脚本"
    exit 1
fi

echo "✅ MCP 服务器文件存在"

# 创建 Cursor MCP 配置目录
CURSOR_CONFIG_DIR="$HOME/.cursor"
CURSOR_MCP_CONFIG="$CURSOR_CONFIG_DIR/mcp.json"

mkdir -p "$CURSOR_CONFIG_DIR"

# 检查现有配置
if [ -f "$CURSOR_MCP_CONFIG" ]; then
    echo "📝 发现现有 Cursor MCP 配置，创建备份..."
    cp "$CURSOR_MCP_CONFIG" "$CURSOR_MCP_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 提示用户输入 Supabase 信息
echo ""
echo "📋 请提供你的 Supabase 项目信息:"
echo "   (可以在 Supabase Dashboard > Settings > API 中找到)"
echo ""

read -p "🔗 Supabase URL (例: https://xxx.supabase.co): " SUPABASE_URL
read -p "🔑 Service Role Key: " SUPABASE_SERVICE_KEY

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_KEY" ]; then
    echo "❌ 错误: Supabase URL 和 Service Role Key 不能为空"
    exit 1
fi

# 创建 MCP 配置
cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "meetmoment-supabase": {
      "command": "python3",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "SUPABASE_URL": "$SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY": "$SUPABASE_SERVICE_KEY"
      }
    }
  }
}
EOF

echo ""
echo "🎉 MCP 服务器配置完成！"
echo ""
echo "📁 配置文件位置: $CURSOR_MCP_CONFIG"
echo "🔧 MCP 服务器位置: $MCP_SERVER_PATH"
echo ""
echo "📋 下一步:"
echo "1. 重启 Cursor IDE"
echo "2. 在 Cursor 中尝试查询: '查询 users 表中的所有用户'"
echo "3. 查看文档: mcp-supabase/README.md"
echo ""
echo "💡 测试 MCP 服务器:"
echo "   cd mcp-supabase"
echo "   export SUPABASE_URL='$SUPABASE_URL'"
echo "   export SUPABASE_SERVICE_ROLE_KEY='$SUPABASE_SERVICE_KEY'"
echo "   python3 server.py"
echo ""
echo "✨ 现在你可以在 Cursor 中直接查询 Supabase 数据了！" 