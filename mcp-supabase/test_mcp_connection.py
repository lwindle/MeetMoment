#!/usr/bin/env python3
"""
测试 MCP Supabase 连接
"""
import os
import sys

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
os.environ['SUPABASE_URL'] = 'https://odnalktszcfoxpcvmshw.supabase.co'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8'

# 测试连接
import subprocess
import json

def test_supabase_connection():
    """测试 Supabase 连接"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not key:
        print("❌ 环境变量未设置")
        return False
    
    print(f"🔗 测试连接到: {url}")
    
    # 使用 curl 测试连接
    cmd = [
        'curl', '-s',
        f'{url}/rest/v1/',
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Supabase 连接成功")
            return True
        else:
            print(f"❌ 连接失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False

def test_list_tables():
    """测试列出现有表"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    cmd = [
        'curl', '-s',
        f'{url}/rest/v1/',
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("📋 当前数据库表:")
            print(result.stdout)
            return True
        else:
            print(f"❌ 获取表列表失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 获取表列表异常: {e}")
        return False

if __name__ == "__main__":
    print("🧪 测试 MCP Supabase 连接...")
    
    if test_supabase_connection():
        print("\n📋 获取现有表信息...")
        test_list_tables()
    else:
        print("❌ 无法连接到 Supabase")
        sys.exit(1)
