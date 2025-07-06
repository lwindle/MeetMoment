#!/usr/bin/env python3
"""
Create a test user directly in the database for testing
"""

import requests
import json
import hashlib

# Configuration
BACKEND_URL = "http://localhost:8080"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_user():
    """Create a test user via registration API"""
    user_data = {
        "phone": "13800138888",
        "password": "test123456",
        "nickname": "AI测试用户",
        "age": 25,
        "city": "上海",
        "occupation": "软件工程师",
        "gender": 1,
        "bio": "我是一个AI测试用户，喜欢科技和编程。"
    }
    
    print("🔄 Creating test user...")
    response = requests.post(f"{BACKEND_URL}/api/auth/register", json=user_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ User created successfully!")
        print(f"   User ID: {result.get('user', {}).get('id')}")
        print(f"   Nickname: {result.get('user', {}).get('nickname')}")
        return result.get('token')
    else:
        print(f"❌ User creation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def login_test_user():
    """Login with test user"""
    login_data = {
        "phone": "13800138888",
        "password": "test123456"
    }
    
    print("🔄 Logging in test user...")
    response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Login successful!")
        print(f"   User: {result.get('user', {}).get('nickname')}")
        return result.get('token')
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_ai_conversation(token, persona, message):
    """Test AI conversation"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    conversation_data = {
        "message": message,
        "persona": persona,
        "context": {
            "conversation_type": "ai_chat",
            "persona": persona
        }
    }
    
    print(f"\n🤖 Testing {persona} persona...")
    print(f"📝 Message: {message}")
    
    response = requests.post(f"{BACKEND_URL}/api/ai/conversation", 
                           json=conversation_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ AI Response:")
        print(f"   Model: {result.get('model', 'unknown')}")
        print(f"   Content: {result.get('content', 'No content')}")
        print(f"   Tokens: {result.get('tokens', 0)}")
        return True
    else:
        print(f"❌ AI conversation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    print("🚀 AI Conversation Test Setup")
    
    # Try to create user first (might fail if exists)
    token = create_test_user()
    
    # If creation failed, try to login
    if not token:
        print("\n🔄 User might already exist, trying to login...")
        token = login_test_user()
    
    if not token:
        print("❌ Cannot get valid token, exiting...")
        return
    
    print(f"\n🎫 Got token: {token[:50]}...")
    
    # Test different personas
    test_cases = [
        ("温柔", "你好，我今天心情不太好，能陪我聊聊吗？"),
        ("活泼", "哈哈，今天天气真好！你喜欢做什么运动吗？"),
        ("智慧", "我在思考人生的意义，你觉得什么是最重要的？"),
    ]
    
    success_count = 0
    for persona, message in test_cases:
        if test_ai_conversation(token, persona, message):
            success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{len(test_cases)} tests passed")

if __name__ == "__main__":
    main() 