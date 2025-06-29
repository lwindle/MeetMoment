#!/usr/bin/env python3
"""
直接通过 Supabase API 执行 SQL 创建表
"""
import subprocess
import json
import time
import sys

SUPABASE_URL = "https://odnalktszcfoxpcvmshw.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8"

def execute_sql_statement(sql):
    """执行单个 SQL 语句"""
    # 使用 PostgREST 的 rpc 功能执行 SQL
    # 注意：这需要在 Supabase 中创建一个 SQL 执行函数
    
    # 先尝试通过直接 API 调用
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'{SUPABASE_URL}/rest/v1/rpc/exec_sql',
        '-H', f'apikey: {SERVICE_ROLE_KEY}',
        '-H', f'Authorization: Bearer {SERVICE_ROLE_KEY}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"query": sql})
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ SQL 执行成功")
            return True
        else:
            print(f"❌ SQL 执行失败: {result.stderr}")
            # 尝试其他方法
            return execute_via_edge_function(sql)
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return False

def execute_via_edge_function(sql):
    """通过 Edge Function 执行 SQL"""
    print("🔄 尝试通过 Edge Function 执行...")
    
    # 这需要部署一个 Edge Function 来执行 SQL
    # 目前我们先跳过这个方法
    return False

def create_sql_execution_function():
    """在 Supabase 中创建 SQL 执行函数"""
    function_sql = """
CREATE OR REPLACE FUNCTION exec_sql(query text)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    EXECUTE query;
    RETURN 'Success';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Error: ' || SQLERRM;
END;
$$;
"""
    
    print("🔧 创建 SQL 执行函数...")
    return execute_raw_sql(function_sql)

def execute_raw_sql(sql):
    """执行原始 SQL（需要数据库直接访问）"""
    # 由于我们没有直接的数据库访问权限，这里返回 False
    # 实际使用中需要通过 psql 或其他数据库客户端
    return False

def main():
    print("🚀 开始通过 API 创建数据库表...")
    
    # 读取 SQL 文件
    try:
        with open('meetmoment_tables.sql', 'r', encoding='utf-8') as f:
            full_sql = f.read()
    except FileNotFoundError:
        print("❌ 找不到 meetmoment_tables.sql 文件")
        return False
    
    # 分割 SQL 语句
    sql_statements = []
    current_statement = ""
    
    for line in full_sql.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            current_statement += line + " "
            if line.endswith(';'):
                sql_statements.append(current_statement.strip())
                current_statement = ""
    
    print(f"📋 找到 {len(sql_statements)} 个 SQL 语句")
    
    # 由于 API 限制，我们建议手动执行
    print("\n⚠️  由于 Supabase REST API 的限制，无法直接执行 DDL 语句")
    print("📝 请手动在 Supabase Dashboard 中执行以下操作:")
    print("\n1. 打开 https://supabase.com/dashboard/project/odnalktszcfoxpcvmshw")
    print("2. 点击左侧菜单的 'SQL Editor'")
    print("3. 点击 'New query'")
    print("4. 复制以下 SQL 内容:")
    print("\n" + "="*50)
    print(full_sql)
    print("="*50)
    print("\n5. 点击 'Run' 按钮执行")
    
    return True

if __name__ == "__main__":
    main()
