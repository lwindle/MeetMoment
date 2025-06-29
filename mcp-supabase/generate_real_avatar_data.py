#!/usr/bin/env python3
import requests
import json
import os
import random
from datetime import datetime, timedelta

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
    elif method == 'PATCH':
        response = requests.patch(url, headers=headers, data=json.dumps(data) if data else None)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    
    return response

def get_female_avatar_urls():
    """Generate female avatar URLs from various free services"""
    avatars = []
    
    # Using generated.photos API (free tier)
    # These are AI-generated faces, completely legal to use
    base_urls = [
        "https://images.generated.photos/",
        "https://this-person-does-not-exist.com/img/avatar-gen",
    ]
    
    # Use some specific female avatar services
    female_avatars = [
        # Pravatar with female seeds
        "https://i.pravatar.cc/300?img=1",
        "https://i.pravatar.cc/300?img=5",
        "https://i.pravatar.cc/300?img=9",
        "https://i.pravatar.cc/300?img=16",
        "https://i.pravatar.cc/300?img=20",
        "https://i.pravatar.cc/300?img=24",
        "https://i.pravatar.cc/300?img=25",
        "https://i.pravatar.cc/300?img=26",
        "https://i.pravatar.cc/300?img=29",
        "https://i.pravatar.cc/300?img=32",
        "https://i.pravatar.cc/300?img=36",
        "https://i.pravatar.cc/300?img=44",
        "https://i.pravatar.cc/300?img=47",
        "https://i.pravatar.cc/300?img=48",
        "https://i.pravatar.cc/300?img=49",
        
        # UI Faces (free female avatars)
        "https://randomuser.me/api/portraits/women/1.jpg",
        "https://randomuser.me/api/portraits/women/2.jpg",
        "https://randomuser.me/api/portraits/women/3.jpg",
        "https://randomuser.me/api/portraits/women/4.jpg",
        "https://randomuser.me/api/portraits/women/5.jpg",
        "https://randomuser.me/api/portraits/women/6.jpg",
        "https://randomuser.me/api/portraits/women/7.jpg",
        "https://randomuser.me/api/portraits/women/8.jpg",
        "https://randomuser.me/api/portraits/women/9.jpg",
        "https://randomuser.me/api/portraits/women/10.jpg",
        "https://randomuser.me/api/portraits/women/11.jpg",
        "https://randomuser.me/api/portraits/women/12.jpg",
        "https://randomuser.me/api/portraits/women/13.jpg",
        "https://randomuser.me/api/portraits/women/14.jpg",
        "https://randomuser.me/api/portraits/women/15.jpg",
        "https://randomuser.me/api/portraits/women/16.jpg",
        "https://randomuser.me/api/portraits/women/17.jpg",
        "https://randomuser.me/api/portraits/women/18.jpg",
        "https://randomuser.me/api/portraits/women/19.jpg",
        "https://randomuser.me/api/portraits/women/20.jpg",
    ]
    
    return female_avatars

def generate_female_users():
    """Generate female user data with real avatars"""
    
    # Chinese female names
    first_names = ["雨萱", "诗涵", "梓涵", "欣怡", "思妍", "雨桐", "心怡", "语嫣", "若汐", "艺涵", 
                   "梦琪", "雅琪", "静怡", "婉儿", "晓雯", "紫萱", "诗雅", "梦瑶", "语桐", "雨薇"]
    
    # Cities
    cities = ["北京", "上海", "深圳", "广州", "杭州", "成都", "西安", "南京", "苏州", "武汉"]
    
    # Occupations
    occupations = ["设计师", "教师", "护士", "程序员", "市场经理", "会计师", "律师", "医生", "记者", "翻译", 
                   "心理咨询师", "产品经理", "人事专员", "销售经理", "艺术家", "摄影师", "编辑", "导游"]
    
    # Bio templates
    bio_templates = [
        "喜欢旅行和摄影，寻找有趣的灵魂",
        "热爱生活，喜欢美食和音乐",
        "工作认真，生活有趣，希望遇到对的人",
        "爱读书，爱电影，爱一切美好的事物",
        "简单快乐，真诚待人",
        "喜欢运动健身，保持积极的生活态度",
        "热爱艺术，享受生活中的小美好",
        "温柔善良，希望找到真爱",
        "独立自信，追求精神共鸣",
        "乐观开朗，相信爱情的美好"
    ]
    
    avatar_urls = get_female_avatar_urls()
    users = []
    
    for i in range(20):  # Generate 20 female users
        user = {
            "phone": f"138{random.randint(10000000, 99999999)}",
            "password": "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi",  # hashed "password"
            "nickname": random.choice(first_names),
            "gender": 2,  # Female
            "age": random.randint(22, 32),
            "city": random.choice(cities),
            "occupation": random.choice(occupations),
            "bio": random.choice(bio_templates),
            "emotion_status": random.choice(["单身", "恋爱中", "刚分手", "想恋爱"]),
            "avatar": avatar_urls[i % len(avatar_urls)],
            "verified": random.choice([True, False]),
            "is_online": random.choice([True, False]),
            "last_active_time": (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat(),
            "ai_score": random.randint(60, 95),
            "profile_complete": round(random.uniform(0.7, 1.0), 2),
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        users.append(user)
    
    return users

def generate_interests_for_users(user_ids):
    """Generate interests for the new users"""
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
    
    print("Generating female users with real avatars...")
    
    # Generate users
    users = generate_female_users()
    
    # Insert users
    print(f"Inserting {len(users)} female users...")
    response = supabase_request('POST', 'users', users)
    
    if response.status_code in [200, 201]:
        inserted_users = response.json()
        print(f"✅ Successfully inserted {len(inserted_users)} users")
        
        # Get user IDs
        user_ids = [user['id'] for user in inserted_users]
        
        # Generate and insert interests
        print("Generating interests for users...")
        interests = generate_interests_for_users(user_ids)
        
        response = supabase_request('POST', 'user_interests', interests)
        if response.status_code in [200, 201]:
            print(f"✅ Successfully inserted {len(interests)} user interests")
        else:
            print(f"❌ Failed to insert interests: {response.status_code} - {response.text}")
        
        # Display some sample users
        print("\n📋 Sample users created:")
        for i, user in enumerate(inserted_users[:5]):
            print(f"{i+1}. {user['nickname']} ({user['age']}岁) - {user['city']} - {user['occupation']}")
            print(f"   头像: {user['avatar']}")
            print(f"   简介: {user['bio']}")
            print()
            
    else:
        print(f"❌ Failed to insert users: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main() 