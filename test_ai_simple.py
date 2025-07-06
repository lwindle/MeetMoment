#!/usr/bin/env python3
"""
Simple AI conversation test script
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8080"
USER_ID = 83  # Known user from database
PHONE = "13900000001"

def generate_simple_jwt():
    """Generate a simple JWT token for testing"""
    import time
    import base64
    import hmac
    import hashlib
    
    # Proper JWT payload matching backend expectations
    payload = {
        "user_id": USER_ID,
        "phone": PHONE,
        "nickname": "测试用户2",
        "exp": int(time.time()) + 3600,  # 1 hour from now
        "iat": int(time.time()),         # issued at
        "iss": "meetmoment"              # issuer
    }
    
    # Proper JWT header
    header = {"alg": "HS256", "typ": "JWT"}
    
    # Convert to base64url (no padding)
    def base64url_encode(data):
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip('=')
    
    header_b64 = base64url_encode(header)
    payload_b64 = base64url_encode(payload)
    
    # Generate signature
    secret = "your-super-secret-jwt-key-change-this-in-production"
    message = f"{header_b64}.{payload_b64}".encode()
    signature = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), message, hashlib.sha256).digest()
    ).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature}"

def test_ai_conversation():
    """Test AI conversation functionality"""
    print("🤖 Testing AI Conversation...")
    
    # Generate token
    token = generate_simple_jwt()
    print(f"📝 Generated token for user {USER_ID}")
    
    # Test different personas
    personas = ["温柔", "活泼", "智慧", "可爱", "成熟"]
    messages = [
        "你好，我今天心情不太好，能陪我聊聊吗？",
        "我最近工作压力很大，你能给我一些建议吗？",
        "今天天气真好，你喜欢什么样的天气？",
        "你觉得什么样的人最有魅力？",
        "我想听听你对人生的看法"
    ]
    
    for i, persona in enumerate(personas):
        message = messages[i % len(messages)]
        print(f"\n🎭 Testing persona: {persona}")
        print(f"💬 Message: {message}")
        
        conversation_data = {
            "message": message,
            "persona": persona,
            "context": {
                "conversation_type": "ai_chat",
                "persona": persona
            }
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/api/ai/conversation", 
                                   json=conversation_data, 
                                   headers=headers,
                                   timeout=30)
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"🤖 AI Response: {result.get('response', 'No response')}")
                print(f"🎯 Model: {result.get('model', 'Unknown')}")
                print(f"⚡ Tokens: {result.get('tokens', 0)}")
                print(f"📋 Full Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_ai_conversation() 