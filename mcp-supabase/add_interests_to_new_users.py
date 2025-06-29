#!/usr/bin/env python3
import requests
import json
import os
import random
from datetime import datetime

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://odnalktszcfoxpcvmshw.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

def supabase_request(method, endpoint, data=None):
    """Make a request to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
    
    return response

def get_female_users():
    """Get all female users (gender = 2)"""
    response = supabase_request('GET', 'users?gender=eq.2&select=id,nickname,age,city')
    if response.status_code == 200:
        return response.json()
    return []

def generate_interests_for_users(user_ids):
    """Generate interests for the users"""
    interests_data = [
        "旅行", "摄影", "音乐", "电影", "读书", "健身", "美食", "购物", "瑜伽", "跑步",
        "游泳", "绘画", "舞蹈", "唱歌", "烹饪", "咖啡", "茶艺", "花艺", "手工", "宠物",
        "时尚", "化妆", "护肤", "减肥", "养生", "心理学", "哲学", "历史", "文学", "艺术"
    ]
    
    interests = []
    for user_id in user_ids:
        # Each user gets 3-8 random interests
        user_interests = random.sample(interests_data, random.randint(3, 8))
        for interest in user_interests:
            interests.append({
                "user_id": user_id,
                "tag": interest,
                "ai_generated": random.choice([True, False]),
                "created_at": datetime.now().isoformat()
            })
    
    return interests

def main():
    if not SUPABASE_SERVICE_ROLE_KEY:
        print("Error: SUPABASE_SERVICE_ROLE_KEY environment variable is required")
        return
    
    print("Getting female users...")
    female_users = get_female_users()
    
    if not female_users:
        print("No female users found")
        return
    
    print(f"Found {len(female_users)} female users")
    
    # Get users who don't have interests yet
    users_without_interests = []
    for user in female_users:
        # Check if user already has interests
        response = supabase_request('GET', f'user_interests?user_id=eq.{user["id"]}&limit=1')
        if response.status_code == 200 and len(response.json()) == 0:
            users_without_interests.append(user)
    
    if not users_without_interests:
        print("All female users already have interests")
        return
    
    print(f"Adding interests for {len(users_without_interests)} users without interests...")
    
    user_ids = [user['id'] for user in users_without_interests]
    interests = generate_interests_for_users(user_ids)
    
    # Insert interests
    response = supabase_request('POST', 'user_interests', interests)
    if response.status_code in [200, 201]:
        print(f"✅ Successfully added {len(interests)} interests")
        
        # Show sample
        print("\n📋 Sample interests added:")
        for user in users_without_interests[:3]:
            user_interests = [i for i in interests if i['user_id'] == user['id']]
            tags = [i['tag'] for i in user_interests]
            print(f"- {user['nickname']} ({user['age']}岁, {user['city']}): {', '.join(tags)}")
    else:
        print(f"❌ Failed to add interests: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main() 