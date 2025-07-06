#!/usr/bin/env python3
"""
Test script for AI conversation functionality
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8080"
TEST_USER_PHONE = "13800138000"
TEST_USER_PASSWORD = "password123"

def login_user():
    """Login and get JWT token"""
    login_data = {
        "phone": TEST_USER_PHONE,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Login successful for user: {result.get('user', {}).get('nickname', 'Unknown')}")
        return result.get('token')
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_ai_conversation(token, persona, message):
    """Test AI conversation with specific persona"""
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
    print(f"📝 User message: {message}")
    
    start_time = time.time()
    response = requests.post(f"{BACKEND_URL}/api/ai/conversation", 
                           json=conversation_data, headers=headers)
    response_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ AI Response ({response_time:.2f}s):")
        print(f"   Model: {result.get('model', 'unknown')}")
        print(f"   Content: {result.get('content', 'No content')}")
        print(f"   Tokens: {result.get('tokens', 0)}")
        return True
    else:
        print(f"❌ AI conversation failed: {response.status_code} - {response.text}")
        return False

def main():
    print("🚀 Starting AI Conversation Test...")
    
    # Login first
    token = login_user()
    if not token:
        print("❌ Cannot proceed without valid token")
        return
    
    # Test messages for different personas
    test_cases = [
        ("温柔", "你好，我今天心情不太好，能陪我聊聊吗？"),
        ("活泼", "哈哈，今天天气真好！你喜欢做什么运动吗？"),
        ("智慧", "我在思考人生的意义，你觉得什么是最重要的？"),
        ("可爱", "呀，你好可爱呢！我们可以做朋友吗？"),
        ("成熟", "最近工作压力很大，你有什么建议吗？"),
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for persona, message in test_cases:
        if test_ai_conversation(token, persona, message):
            success_count += 1
        time.sleep(1)  # Add delay between requests
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All AI conversation tests passed!")
    else:
        print("⚠️  Some tests failed. Check the backend logs for details.")

 