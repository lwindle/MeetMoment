#!/usr/bin/env python3
"""
测试 MCP 协议操作 MeetMoment 数据
"""
import subprocess
import json
import os

# 设置环境变量
os.environ['SUPABASE_URL'] = 'https://odnalktszcfoxpcvmshw.supabase.co'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8'

def supabase_query(table, filters=None, select="*", limit=None):
    """模拟 MCP supabase_query 工具"""
    url = os.environ['SUPABASE_URL']
    key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
    
    query_url = f"{url}/rest/v1/{table}"
    params = []
    
    if select != "*":
        params.append(f"select={select}")
    
    if filters:
        for key_filter, value in filters.items():
            params.append(f"{key_filter}={value}")
    
    if limit:
        params.append(f"limit={limit}")
    
    if params:
        query_url += "?" + "&".join(params)
    
    cmd = [
        'curl', '-s',
        query_url,
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def supabase_insert(table, data):
    """模拟 MCP supabase_insert 工具"""
    url = os.environ['SUPABASE_URL']
    key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'{url}/rest/v1/{table}',
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json',
        '-H', 'Prefer: return=representation',
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def supabase_update(table, filters, data):
    """模拟 MCP supabase_update 工具"""
    url = os.environ['SUPABASE_URL']
    key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
    
    query_url = f"{url}/rest/v1/{table}"
    params = []
    
    for key_filter, value in filters.items():
        params.append(f"{key_filter}=eq.{value}")
    
    if params:
        query_url += "?" + "&".join(params)
    
    cmd = [
        'curl', '-s', '-X', 'PATCH',
        query_url,
        '-H', f'apikey: {key}',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json',
        '-H', 'Prefer: return=representation',
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def test_mcp_operations():
    """测试各种 MCP 操作"""
    print("🧪 测试 MCP 协议操作...")
    
    # 1. 查询所有用户
    print("\n📋 1. 查询所有用户:")
    users = supabase_query("users", select="id,nickname,city,age,is_online")
    if "error" not in users:
        for user in users:
            status = "在线" if user.get('is_online') else "离线"
            print(f"  - {user['nickname']} (ID: {user['id']}, {user['city']}, {user['age']}岁, {status})")
    else:
        print(f"  ❌ 查询失败: {users['error']}")
    
    # 2. 查询特定城市的用户
    print("\n📋 2. 查询北京的用户:")
    beijing_users = supabase_query("users", filters={"city": "eq.北京"}, select="id,nickname,occupation")
    if "error" not in beijing_users:
        for user in beijing_users:
            print(f"  - {user['nickname']} ({user['occupation']})")
    else:
        print(f"  ❌ 查询失败: {beijing_users['error']}")
    
    # 3. 查询圈子信息
    print("\n📋 3. 查询所有圈子:")
    circles = supabase_query("circles", select="id,name,category,description")
    if "error" not in circles:
        for circle in circles:
            print(f"  - {circle['name']} ({circle['category']}): {circle['description']}")
    else:
        print(f"  ❌ 查询失败: {circles['error']}")
    
    # 4. 查询用户兴趣
    print("\n📋 4. 查询用户兴趣 (前10个):")
    interests = supabase_query("user_interests", 
                              select="user_id,tag,ai_generated", 
                              limit=10)
    if "error" not in interests:
        for interest in interests:
            ai_tag = " (AI生成)" if interest.get('ai_generated') else ""
            print(f"  - 用户{interest['user_id']}: {interest['tag']}{ai_tag}")
    else:
        print(f"  ❌ 查询失败: {interests['error']}")
    
    # 5. 查询匹配记录
    print("\n📋 5. 查询匹配记录:")
    matches = supabase_query("matches", select="user_id,target_user_id,action,is_matched")
    if "error" not in matches:
        for match in matches:
            status = "匹配成功" if match.get('is_matched') else "未匹配"
            print(f"  - 用户{match['user_id']} -> 用户{match['target_user_id']}: {match['action']} ({status})")
    else:
        print(f"  ❌ 查询失败: {matches['error']}")
    
    # 6. 测试插入新数据
    print("\n📋 6. 测试插入新用户兴趣:")
    new_interest = {
        "user_id": 1,
        "tag": "人工智能",
        "ai_generated": False
    }
    result = supabase_insert("user_interests", new_interest)
    if "error" not in result and result:
        print(f"  ✅ 成功添加兴趣: {new_interest['tag']}")
    else:
        print(f"  ❌ 添加失败: {result.get('error', '未知错误')}")
    
    # 7. 测试更新数据
    print("\n📋 7. 测试更新用户在线状态:")
    update_result = supabase_update("users", 
                                   {"id": 1}, 
                                   {"is_online": True, "last_active_time": "now()"})
    if "error" not in update_result and update_result:
        print(f"  ✅ 成功更新用户1的在线状态")
    else:
        print(f"  ❌ 更新失败: {update_result.get('error', '未知错误')}")
    
    print("\n🎉 MCP 操作测试完成！")

def generate_additional_data():
    """生成一些额外的测试数据"""
    print("\n📋 生成额外测试数据...")
    
    # 添加一些圈子动态
    posts = [
        {
            "circle_id": 1,
            "user_id": 1,
            "content": "分享一个有趣的编程技巧，使用 Python 的装饰器可以大大简化代码！",
            "like_count": 5,
            "comment_count": 2
        },
        {
            "circle_id": 2,
            "user_id": 2,
            "content": "今天去了三里屯，发现了一家很棒的咖啡店，推荐给大家！",
            "like_count": 8,
            "comment_count": 3
        },
        {
            "circle_id": 3,
            "user_id": 3,
            "content": "刚拍的日落照片，希望大家喜欢 📸",
            "images": json.dumps(["https://example.com/sunset1.jpg"]),
            "like_count": 12,
            "comment_count": 5
        }
    ]
    
    for post in posts:
        result = supabase_insert("circle_posts", post)
        if "error" not in result and result:
            print(f"  ✅ 成功创建动态: {post['content'][:20]}...")
        else:
            print(f"  ❌ 创建动态失败")
    
    # 添加一些会话
    conversation = {
        "type": "private"
    }
    conv_result = supabase_insert("conversations", conversation)
    if "error" not in conv_result and conv_result:
        conv_id = conv_result[0]['id']
        print(f"  ✅ 成功创建会话 ID: {conv_id}")
        
        # 添加会话参与者
        participants = [
            {"conversation_id": conv_id, "user_id": 1},
            {"conversation_id": conv_id, "user_id": 2}
        ]
        
        for participant in participants:
            supabase_insert("conversation_participants", participant)
        
        # 添加一些消息
        messages = [
            {
                "conversation_id": conv_id,
                "sender_id": 1,
                "content": "你好！很高兴认识你",
                "message_type": "text"
            },
            {
                "conversation_id": conv_id,
                "sender_id": 2,
                "content": "你好！我也很高兴认识你，我们有很多共同兴趣呢",
                "message_type": "text"
            }
        ]
        
        for message in messages:
            supabase_insert("messages", message)
        
        print(f"  ✅ 成功创建对话和消息")

if __name__ == "__main__":
    test_mcp_operations()
    generate_additional_data()
    
    print(f"\n🔗 查看数据:")
    print(f"Supabase Dashboard: https://supabase.com/dashboard/project/odnalktszcfoxpcvmshw")
    print(f"\n💡 现在你可以使用 MCP 工具来管理这些数据了！")
