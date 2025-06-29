#!/bin/bash

# MeetMoment Supabase MCP 服务器安装脚本
# 此脚本将自动安装和配置 MCP 服务器

set -e

echo "🚀 开始安装 MeetMoment Supabase MCP 服务器..."

# 检查 Node.js 版本
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js 18 或更高版本"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误: Node.js 版本过低 (当前: v$NODE_VERSION)，需要 v18 或更高版本"
    exit 1
fi

echo "✅ Node.js 版本检查通过: $(node -v)"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm"
    exit 1
fi

echo "✅ npm 版本: $(npm -v)"

# 进入 MCP 服务器目录
cd "$(dirname "$0")/../mcp-server"

echo "📦 安装依赖..."
npm install

echo "🔧 构建项目..."
npm run build

# 检查环境配置
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，从示例文件复制..."
    cp env.example .env
    echo "📝 请编辑 .env 文件，填入你的 Supabase 配置信息"
    echo "   文件位置: $(pwd)/.env"
    echo ""
    echo "需要配置的变量:"
    echo "  - SUPABASE_URL"
    echo "  - SUPABASE_ANON_KEY"
    echo "  - SUPABASE_SERVICE_ROLE_KEY"
    echo ""
fi

# 检查 Claude Desktop 配置目录
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "🔍 发现 Claude Desktop 配置目录"
    
    # 获取当前目录的绝对路径
    MCP_SERVER_PATH="$(pwd)/dist/index.js"
    
    # 创建或更新 Claude Desktop 配置
    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        echo "📝 更新 Claude Desktop 配置..."
        # 备份现有配置
        cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo "   (已备份原配置文件)"
    else
        echo "📝 创建 Claude Desktop 配置文件..."
        mkdir -p "$CLAUDE_CONFIG_DIR"
    fi
    
    # 生成配置文件内容
    cat > "$CLAUDE_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "meetmoment-supabase": {
      "command": "node",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "SUPABASE_URL": "https://your-project-ref.supabase.co",
        "SUPABASE_ANON_KEY": "your-anon-key",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
EOF
    
    echo "✅ Claude Desktop 配置已更新"
    echo "   配置文件: $CLAUDE_CONFIG_FILE"
    echo "   ⚠️  请编辑配置文件中的 Supabase 环境变量"
else
    echo "⚠️  未找到 Claude Desktop 配置目录"
    echo "   如果你使用 Claude Desktop，请手动配置 MCP 服务器"
    echo "   配置路径: ~/Library/Application Support/Claude/claude_desktop_config.json"
fi

echo ""
echo "🎉 MCP 服务器安装完成！"
echo ""
echo "📋 后续步骤:"
echo "1. 编辑环境配置文件: $(pwd)/.env"
echo "2. 填入你的 Supabase 项目信息"
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "3. 编辑 Claude Desktop 配置: $CLAUDE_CONFIG_FILE"
    echo "4. 重启 Claude Desktop"
else
    echo "3. 配置 Claude Desktop (如果使用)"
fi
echo "5. 测试连接: npm run dev"
echo ""
echo "📚 详细文档请查看: README.md"
echo ""

# 提供测试命令
echo "🧪 测试 MCP 服务器:"
echo "   npm run dev    # 开发模式"
echo "   npm start      # 生产模式"
echo ""

echo "✨ 安装完成！享受使用 MCP 管理 Supabase 数据的便利！" 