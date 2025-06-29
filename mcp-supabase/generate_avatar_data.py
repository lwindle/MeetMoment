#!/usr/bin/env python3
"""
生成合法头像数据的脚本
使用免费的头像生成服务，避免版权和隐私问题
"""

import requests
import json
import os
import time
import random
from typing import List, Dict

# 配置
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

def generate_pravatar_urls(count: int = 20) -> List[str]:
    """
    生成Pravatar头像URL列表
    Pravatar是免费的头像服务，可商用
    """
    avatar_urls = []
    for i in range(count):
        # 使用不同的种子生成不同头像
        seed = random.randint(1, 1000)
        url = f"https://i.pravatar.cc/300?img={seed}"
        avatar_urls.append(url)
    return avatar_urls

def generate_dicebear_urls(count: int = 20) -> List[str]:
    """
    生成Dicebear头像URL列表
    Dicebear是开源的头像生成器
    """
    avatar_urls = []
    styles = ['avataaars', 'personas', 'notionists', 'lorelei']
    
    for i in range(count):
        style = random.choice(styles)
        seed = f"user{i}_{random.randint(1000, 9999)}"
        url = f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}&size=300"
        avatar_urls.append(url)
    return avatar_urls

def generate_robohash_urls(count: int = 20) -> List[str]:
    """
    生成RoboHash头像URL列表
    RoboHash生成机器人风格头像
    """
    avatar_urls = []
    for i in range(count):
        seed = f"user{i}_{random.randint(1000, 9999)}"
        url = f"https://robohash.org/{seed}?size=300x300&set=set1"
        avatar_urls.append(url)
    return avatar_urls

def create_sample_users_with_avatars():
    """
    创建带有合法头像的示例用户数据
    """
    
    # 生成不同类型的头像
    pravatar_urls = generate_pravatar_urls(10)
    dicebear_urls = generate_dicebear_urls(10)
    
    sample_users = [
        {
            "phone": "13800000001",
            "password": "$2a$10$example.hash.for.password123",  # 实际应用中需要正确哈希
            "nickname": "小雨",
            "gender": 0,  # 0=女, 1=男
            "age": 25,
            "city": "北京",
            "occupation": "设计师",
            "bio": "喜欢旅行和摄影，寻找有趣的灵魂",
            "emotion_status": "单身",
            "avatar": pravatar_urls[0],
            "verified": True,
            "ai_score": 85
        },
        {
            "phone": "13800000002", 
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "晴天",
            "gender": 0,
            "age": 23,
            "city": "上海", 
            "occupation": "程序员",
            "bio": "代码改变世界，咖啡续命",
            "emotion_status": "单身",
            "avatar": pravatar_urls[1],
            "verified": True,
            "ai_score": 92
        },
        {
            "phone": "13800000003",
            "password": "$2a$10$example.hash.for.password123", 
            "nickname": "月亮",
            "gender": 0,
            "age": 27,
            "city": "深圳",
            "occupation": "产品经理", 
            "bio": "热爱生活，享受当下",
            "emotion_status": "单身",
            "avatar": pravatar_urls[2],
            "verified": False,
            "ai_score": 78
        },
        {
            "phone": "13800000004",
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "星星",
            "gender": 0, 
            "age": 24,
            "city": "广州",
            "occupation": "教师",
            "bio": "传道授业解惑，桃李满天下",
            "emotion_status": "单身",
            "avatar": pravatar_urls[3],
            "verified": True,
            "ai_score": 88
        },
        {
            "phone": "13800000005",
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "彩虹", 
            "gender": 0,
            "age": 26,
            "city": "杭州",
            "occupation": "医生",
            "bio": "救死扶伤，医者仁心",
            "emotion_status": "单身", 
            "avatar": pravatar_urls[4],
            "verified": True,
            "ai_score": 95
        },
        {
            "phone": "13800000006",
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "花朵",
            "gender": 0,
            "age": 22,
            "city": "成都", 
            "occupation": "学生",
            "bio": "青春无悔，未来可期",
            "emotion_status": "单身",
            "avatar": dicebear_urls[0],
            "verified": False,
            "ai_score": 82
        },
        {
            "phone": "13800000007",
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "蝴蝶",
            "gender": 0,
            "age": 28,
            "city": "武汉",
            "occupation": "律师", 
            "bio": "正义之剑，法律之盾",
            "emotion_status": "单身",
            "avatar": dicebear_urls[1],
            "verified": True,
            "ai_score": 90
        },
        {
            "phone": "13800000008", 
            "password": "$2a$10$example.hash.for.password123",
            "nickname": "樱花",
            "gender": 0,
            "age": 25,
            "city": "西安",
            "occupation": "记者",
            "bio": "用文字记录世界，用镜头捕捉真相",
            "emotion_status": "单身",
            "avatar": dicebear_urls[2],
            "verified": True,
            "ai_score": 87
        }
    ]
    
    return sample_users

def insert_users_to_supabase(users: List[Dict]):
    """
    将用户数据插入到Supabase数据库
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置 SUPABASE_URL 和 SUPABASE_SERVICE_ROLE_KEY 环境变量")
        return False
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    url = f"{SUPABASE_URL}/rest/v1/users"
    
    try:
        response = requests.post(url, headers=headers, json=users)
        
        if response.status_code in [200, 201]:
            print(f"✅ 成功插入 {len(users)} 个用户记录")
            return True
        else:
            print(f"❌ 插入失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """
    主函数
    """
    print("🎭 开始生成合法头像数据...")
    
    # 生成示例用户数据
    users = create_sample_users_with_avatars()
    
    print(f"📝 生成了 {len(users)} 个用户数据")
    
    # 显示头像URL示例
    print("\n🖼️ 头像URL示例:")
    for i, user in enumerate(users[:3]):
        print(f"  {user['nickname']}: {user['avatar']}")
    
    # 询问是否插入数据库
    confirm = input("\n❓ 是否要将数据插入到Supabase数据库? (y/n): ")
    
    if confirm.lower() == 'y':
        success = insert_users_to_supabase(users)
        if success:
            print("🎉 数据插入完成!")
        else:
            print("💥 数据插入失败!")
    else:
        print("📋 数据已生成但未插入数据库")
        
        # 保存到JSON文件
        with open('sample_users_with_avatars.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print("💾 数据已保存到 sample_users_with_avatars.json")

if __name__ == "__main__":
    main() 