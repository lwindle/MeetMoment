#!/usr/bin/env python3
"""
Single AI conversation test
"""

import requests
import json
import time
import base64
import hmac
import hashlib

# Configuration
BACKEND_URL = "http://localhost:8080"
USER_ID = 83
PHONE = "13900000001"

def generate_jwt():
    """Generate JWT token"""
    payload = {
        "user_id": USER_ID,
        "phone": PHONE,
        "nickname": "测试用户2",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "iss": "meetmoment"
    }
    
    header = {"alg": "HS256", "typ": "JWT"}
    
    def base64url_encode(data):
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip('=')
    
    header_b64 = base64url_encode(header)
    payload_b64 = base64url_encode(payload)
    
    secret = "your-super-secret-jwt-key-change-this-in-production"
    message = f"{header_b64}.{payload_b64}".encode()
    signature = base64.urlsafe_b64encode(
        hmac.new(secret.encode(), message, hashlib.sha256).digest()
    ).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature}"

def test_single_conversation():
    """Test single AI conversation"""
    print("🤖 Testing Single AI Conversation...")
    
    token = generate_jwt()
    print(f"📝 Generated token for user {USER_ID}")
    
    conversation_data = {
        "message": "你好，我今天心情不太好，能陪我聊聊吗？",
        "persona": "温柔",
        "context": {
            "conversation_type": "ai_chat",
            "persona": "温柔"
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"💬 Sending message: {conversation_data['message']}")
    print(f"🎭 Persona: {conversation_data['persona']}")
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/ai/conversation", 
                               json=conversation_data, 
                               headers=headers,
                               timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Full Response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ Error Response:")
            print(f"Status: {response.status_code}")
            print(f"Text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Exception: {e}")

if __name__ == "__main__":
    test_single_conversation() 