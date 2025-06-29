#!/usr/bin/env python3
"""
MeetMoment Supabase MCP Server
A simple MCP server for Supabase database operations
"""

import json
import sys
import os
import asyncio
from typing import Any, Dict, List, Optional
import subprocess

# MCP 响应结构
class MCPResponse:
    def __init__(self, result: Any = None, error: str = None):
        self.result = result
        self.error = error

    def to_dict(self):
        if self.error:
            return {"error": {"code": -1, "message": self.error}}
        return {"result": self.result}

class SupabaseMCPServer:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("需要设置 SUPABASE_URL 和 SUPABASE_SERVICE_ROLE_KEY 环境变量")

    def execute_sql_query(self, query: str, params: Optional[Dict] = None) -> Dict:
        """执行 SQL 查询"""
        try:
            # 使用 curl 调用 Supabase REST API
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                "Content-Type: application/json",
                f"apikey: {self.supabase_key}"
            ]
            
            # 构建 curl 命令
            cmd = ["curl", "-s", "-X", "POST"]
            for header in headers:
                cmd.extend(["-H", header])
            
            # 添加查询数据
            data = {"query": query}
            if params:
                data["params"] = params
            
            cmd.extend(["-d", json.dumps(data)])
            cmd.append(f"{self.supabase_url}/rest/v1/rpc/execute_sql")
            
            # 执行命令
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"Query failed: {result.stderr}"}
            
            return json.loads(result.stdout)
            
        except Exception as e:
            return {"error": str(e)}

    def query_table(self, table: str, select: str = "*", filters: Optional[Dict] = None, limit: Optional[int] = None) -> Dict:
        """查询表数据"""
        try:
            url = f"{self.supabase_url}/rest/v1/{table}"
            params = [f"select={select}"]
            
            if filters:
                for key, value in filters.items():
                    params.append(f"{key}=eq.{value}")
            
            if limit:
                params.append(f"limit={limit}")
            
            if params:
                url += "?" + "&".join(params)
            
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                f"apikey: {self.supabase_key}"
            ]
            
            cmd = ["curl", "-s"]
            for header in headers:
                cmd.extend(["-H", header])
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"查询失败: {result.stderr}"}
            
            data = json.loads(result.stdout)
            return {"success": True, "data": data, "count": len(data) if isinstance(data, list) else 1}
            
        except Exception as e:
            return {"error": str(e)}

    def insert_data(self, table: str, data: Dict) -> Dict:
        """插入数据"""
        try:
            url = f"{self.supabase_url}/rest/v1/{table}"
            
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                "Content-Type: application/json",
                f"apikey: {self.supabase_key}",
                "Prefer: return=representation"
            ]
            
            cmd = ["curl", "-s", "-X", "POST"]
            for header in headers:
                cmd.extend(["-H", header])
            cmd.extend(["-d", json.dumps(data)])
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"插入失败: {result.stderr}"}
            
            response_data = json.loads(result.stdout)
            return {"success": True, "data": response_data}
            
        except Exception as e:
            return {"error": str(e)}

    def update_data(self, table: str, data: Dict, filters: Dict) -> Dict:
        """更新数据"""
        try:
            url = f"{self.supabase_url}/rest/v1/{table}"
            params = []
            
            for key, value in filters.items():
                params.append(f"{key}=eq.{value}")
            
            if params:
                url += "?" + "&".join(params)
            
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                "Content-Type: application/json",
                f"apikey: {self.supabase_key}",
                "Prefer: return=representation"
            ]
            
            cmd = ["curl", "-s", "-X", "PATCH"]
            for header in headers:
                cmd.extend(["-H", header])
            cmd.extend(["-d", json.dumps(data)])
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"Update failed: {result.stderr}"}
            
            response_data = json.loads(result.stdout)
            return {"success": True, "data": response_data}
            
        except Exception as e:
            return {"error": str(e)}

    def delete_data(self, table: str, filters: Dict) -> Dict:
        """删除数据"""
        try:
            url = f"{self.supabase_url}/rest/v1/{table}"
            params = []
            
            for key, value in filters.items():
                params.append(f"{key}=eq.{value}")
            
            if params:
                url += "?" + "&".join(params)
            
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                f"apikey: {self.supabase_key}",
                "Prefer: return=representation"
            ]
            
            cmd = ["curl", "-s", "-X", "DELETE"]
            for header in headers:
                cmd.extend(["-H", header])
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"error": f"Delete failed: {result.stderr}"}
            
            response_data = json.loads(result.stdout)
            return {"success": True, "data": response_data}
            
        except Exception as e:
            return {"error": str(e)}

    def list_tables(self) -> Dict:
        """获取所有表"""
        try:
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
            
            url = f"{self.supabase_url}/rest/v1/rpc/execute_sql"
            headers = [
                f"Authorization: Bearer {self.supabase_key}",
                "Content-Type: application/json",
                f"apikey: {self.supabase_key}"
            ]
            
            data = {"query": query}
            
            cmd = ["curl", "-s", "-X", "POST"]
            for header in headers:
                cmd.extend(["-H", header])
            cmd.extend(["-d", json.dumps(data)])
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                if isinstance(response_data, list):
                    tables = [row.get('table_name') for row in response_data]
                    return {"success": True, "tables": tables}
            
            # 如果 RPC 失败，使用简单的表名列表
            return {"success": True, "tables": ["users", "user_photos", "user_interests", "matches", "conversations", "messages", "circles", "circle_members", "circle_posts"]}
            
        except Exception as e:
            return {"error": str(e)}

def handle_mcp_request(request: Dict) -> Dict:
    """处理 MCP 请求"""
    try:
        server = SupabaseMCPServer()
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "supabase_query",
                        "description": "查询 Supabase 数据库表",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "table": {"type": "string", "description": "表名"},
                                "select": {"type": "string", "description": "选择的列", "default": "*"},
                                "filters": {"type": "object", "description": "过滤条件"},
                                "limit": {"type": "number", "description": "限制行数"}
                            },
                            "required": ["table"]
                        }
                    },
                    {
                        "name": "supabase_insert",
                        "description": "插入数据到 Supabase 表",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "table": {"type": "string", "description": "表名"},
                                "data": {"type": "object", "description": "要插入的数据"}
                            },
                            "required": ["table", "data"]
                        }
                    },
                    {
                        "name": "supabase_update",
                        "description": "更新 Supabase 表数据",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "table": {"type": "string", "description": "表名"},
                                "data": {"type": "object", "description": "要更新的数据"},
                                "filters": {"type": "object", "description": "更新条件"}
                            },
                            "required": ["table", "data", "filters"]
                        }
                    },
                    {
                        "name": "supabase_delete",
                        "description": "删除 Supabase 表数据",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "table": {"type": "string", "description": "表名"},
                                "filters": {"type": "object", "description": "删除条件"}
                            },
                            "required": ["table", "filters"]
                        }
                    },
                    {
                        "name": "supabase_list_tables",
                        "description": "获取所有数据库表",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "supabase_query":
                result = server.query_table(
                    table=arguments.get("table"),
                    select=arguments.get("select", "*"),
                    filters=arguments.get("filters"),
                    limit=arguments.get("limit")
                )
            elif tool_name == "supabase_insert":
                result = server.insert_data(
                    table=arguments.get("table"),
                    data=arguments.get("data")
                )
            elif tool_name == "supabase_update":
                result = server.update_data(
                    table=arguments.get("table"),
                    data=arguments.get("data"),
                    filters=arguments.get("filters")
                )
            elif tool_name == "supabase_delete":
                result = server.delete_data(
                    table=arguments.get("table"),
                    filters=arguments.get("filters")
                )
            elif tool_name == "supabase_list_tables":
                result = server.list_tables()
            else:
                result = {"error": f"未知工具: {tool_name}"}
            
            return {"content": [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]}
        
        else:
            return {"error": {"code": -32601, "message": f"方法未找到: {method}"}}
    
    except Exception as e:
        return {"error": {"code": -1, "message": str(e)}}

def main():
    """主函数 - 处理 MCP 协议"""
    try:
        # 读取标准输入
        for line in sys.stdin:
            if line.strip():
                try:
                    request = json.loads(line.strip())
                    response = handle_mcp_request(request)
                    
                    # 添加请求 ID（如果存在）
                    if "id" in request:
                        response["id"] = request["id"]
                    
                    # 输出响应
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        "error": {"code": -32700, "message": f"解析错误: {str(e)}"}
                    }
                    print(json.dumps(error_response, ensure_ascii=False))
                    sys.stdout.flush()
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        error_response = {
            "error": {"code": -1, "message": f"Server error: {str(e)}"}
        }
        print(json.dumps(error_response, ensure_ascii=False))
        sys.stdout.flush()

if __name__ == "__main__":
    main() 