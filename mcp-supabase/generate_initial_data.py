#!/usr/bin/env python3
"""
通过 MCP 协议为 MeetMoment 生成初始化数据
"""
import subprocess
import json
import time
import random
from datetime import datetime, timedelta

SUPABASE_URL = "https://odnalktszcfoxpcvmshw.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8"

def insert_data(table_name, data, description=""):
    """向指定表插入数据"""
    print(f"🔄 {description or f'插入数据到 {table_name}'}")
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'{SUPABASE_URL}/rest/v1/{table_name}',
        '-H', f'apikey: {SERVICE_ROLE_KEY}',
        '-H', f'Authorization: Bearer {SERVICE_ROLE_KEY}',
        '-H', 'Content-Type: application/json',
        '-H', 'Prefer: return=representation',
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            response = result.stdout.strip()
            if response and not response.startswith('{"code"'):
                print(f"✅ {description or f'{table_name} 数据插入成功'}")
                return json.loads(response) if response else True
            else:
                print(f"❌ {description or f'{table_name} 数据插入失败'}: {response}")
                return False
        else:
            print(f"❌ {description or f'{table_name} 请求失败'}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description or f'{table_name} 插入异常'}: {e}")
        return False

def generate_users_data():
    """生成用户数据"""
    users = [
        {
            "phone": "13800138001",
            "password": "hashed_password_1",
            "nickname": "小明",
            "gender": 0,
            "age": 25,
            "city": "北京",
            "occupation": "软件工程师",
            "bio": "热爱编程，喜欢旅行和摄影",
            "emotion_status": "single",
            "avatar": "https://example.com/avatar1.jpg",
            "verified": True,
            "is_online": True,
            "ai_score": 85
        },
        {
            "phone": "13800138002", 
            "password": "hashed_password_2",
            "nickname": "小红",
            "gender": 1,
            "age": 23,
            "city": "上海",
            "occupation": "产品经理",
            "bio": "喜欢美食和音乐，寻找有趣的灵魂",
            "emotion_status": "single",
            "avatar": "https://example.com/avatar2.jpg",
            "verified": True,
            "is_online": False,
            "ai_score": 92
        },
        {
            "phone": "13800138003",
            "password": "hashed_password_3", 
            "nickname": "阿强",
            "gender": 0,
            "age": 28,
            "city": "深圳",
            "occupation": "设计师",
            "bio": "追求完美的设计，热爱生活",
            "emotion_status": "single",
            "avatar": "https://example.com/avatar3.jpg",
            "verified": False,
            "is_online": True,
            "ai_score": 78
        },
        {
            "phone": "13800138004",
            "password": "hashed_password_4",
            "nickname": "小丽",
            "gender": 1,
            "age": 26,
            "city": "广州",
            "occupation": "市场营销",
            "bio": "乐观开朗，喜欢运动和读书",
            "emotion_status": "single", 
            "avatar": "https://example.com/avatar4.jpg",
            "verified": True,
            "is_online": True,
            "ai_score": 88
        },
        {
            "phone": "13800138005",
            "password": "hashed_password_5",
            "nickname": "大伟",
            "gender": 0,
            "age": 30,
            "city": "杭州",
            "occupation": "创业者",
            "bio": "梦想改变世界，寻找志同道合的伙伴",
            "emotion_status": "single",
            "avatar": "https://example.com/avatar5.jpg",
            "verified": True,
            "is_online": False,
            "ai_score": 95
        }
    ]
    
    return users

def generate_interests_data(user_ids):
    """生成用户兴趣数据"""
    interests_pool = [
        "编程", "旅行", "摄影", "音乐", "电影", "读书", "运动", "美食",
        "游戏", "绘画", "舞蹈", "瑜伽", "健身", "烹饪", "咖啡", "茶艺",
        "投资", "创业", "科技", "时尚", "宠物", "园艺", "手工", "收藏"
    ]
    
    user_interests = []
    for user_id in user_ids:
        # 每个用户随机选择3-6个兴趣
        selected_interests = random.sample(interests_pool, random.randint(3, 6))
        for interest in selected_interests:
            user_interests.append({
                "user_id": user_id,
                "tag": interest,
                "ai_generated": random.choice([True, False])
            })
    
    return user_interests

def generate_circles_data():
    """生成圈子数据"""
    circles = [
        {
            "name": "程序员交流圈",
            "description": "技术分享，经验交流，一起成长",
            "category": "profession",
            "cover_image": "https://example.com/circle1.jpg",
            "is_public": True,
            "tags": json.dumps(["编程", "技术", "交流", "成长"])
        },
        {
            "name": "北京同城",
            "description": "北京地区的朋友们，一起探索这座城市",
            "category": "location", 
            "cover_image": "https://example.com/circle2.jpg",
            "is_public": True,
            "tags": json.dumps(["北京", "同城", "聚会", "交友"])
        },
        {
            "name": "摄影爱好者",
            "description": "分享美好瞬间，交流摄影技巧",
            "category": "interest",
            "cover_image": "https://example.com/circle3.jpg", 
            "is_public": True,
            "tags": json.dumps(["摄影", "艺术", "分享", "技巧"])
        },
        {
            "name": "美食探索队",
            "description": "发现城市里的美味，分享美食体验",
            "category": "interest",
            "cover_image": "https://example.com/circle4.jpg",
            "is_public": True,
            "tags": json.dumps(["美食", "探索", "分享", "生活"])
        }
    ]
    
    return circles

def generate_circle_members(user_ids, circle_ids):
    """生成圈子成员数据"""
    members = []
    
    for circle_id in circle_ids:
        # 每个圈子随机分配2-4个成员
        selected_users = random.sample(user_ids, random.randint(2, min(4, len(user_ids))))
        for i, user_id in enumerate(selected_users):
            role = "owner" if i == 0 else "member"
            members.append({
                "circle_id": circle_id,
                "user_id": user_id,
                "role": role
            })
    
    return members

def generate_matches_data(user_ids):
    """生成匹配数据"""
    matches = []
    actions = ["like", "pass", "super_like"]
    
    # 生成一些匹配记录
    for i in range(len(user_ids)):
        for j in range(i + 1, len(user_ids)):
            if random.random() < 0.6:  # 60% 概率生成匹配记录
                action = random.choice(actions)
                is_matched = action == "like" and random.random() < 0.3  # 30% 概率匹配成功
                
                matches.append({
                    "user_id": user_ids[i],
                    "target_user_id": user_ids[j], 
                    "action": action,
                    "is_matched": is_matched
                })
    
    return matches

def main():
    print("🚀 开始生成 MeetMoment 初始化数据...")
    
    # 1. 创建用户数据
    print("\n📋 步骤 1: 创建用户数据")
    users_data = generate_users_data()
    created_users = []
    
    for user in users_data:
        result = insert_data("users", user, f"创建用户 {user['nickname']}")
        if result:
            created_users.append(result)
            time.sleep(0.5)
    
    if not created_users:
        print("❌ 用户创建失败，停止执行")
        return
    
    user_ids = [user[0]['id'] if isinstance(user, list) else user['id'] for user in created_users]
    print(f"✅ 成功创建 {len(user_ids)} 个用户")
    
    # 2. 创建用户兴趣数据
    print("\n📋 步骤 2: 创建用户兴趣数据")
    interests_data = generate_interests_data(user_ids)
    
    for interest in interests_data:
        insert_data("user_interests", interest, f"添加兴趣: {interest['tag']}")
        time.sleep(0.2)
    
    # 3. 创建圈子数据
    print("\n📋 步骤 3: 创建圈子数据")
    circles_data = generate_circles_data()
    created_circles = []
    
    for circle in circles_data:
        result = insert_data("circles", circle, f"创建圈子 {circle['name']}")
        if result:
            created_circles.append(result)
            time.sleep(0.5)
    
    circle_ids = [circle[0]['id'] if isinstance(circle, list) else circle['id'] for circle in created_circles]
    print(f"✅ 成功创建 {len(circle_ids)} 个圈子")
    
    # 4. 创建圈子成员数据
    if circle_ids:
        print("\n📋 步骤 4: 创建圈子成员数据")
        members_data = generate_circle_members(user_ids, circle_ids)
        
        for member in members_data:
            insert_data("circle_members", member, f"添加圈子成员")
            time.sleep(0.2)
    
    # 5. 创建匹配数据
    print("\n📋 步骤 5: 创建匹配数据")
    matches_data = generate_matches_data(user_ids)
    
    for match in matches_data:
        insert_data("matches", match, "创建匹配记录")
        time.sleep(0.2)
    
    print("\n🎉 初始化数据生成完成！")
    print(f"📊 数据统计:")
    print(f"  - 用户: {len(user_ids)} 个")
    print(f"  - 圈子: {len(circle_ids)} 个") 
    print(f"  - 兴趣标签: {len(interests_data)} 个")
    print(f"  - 匹配记录: {len(matches_data)} 个")
    
    print(f"\n🔗 你可以在 Supabase Dashboard 中查看数据:")
    print(f"https://supabase.com/dashboard/project/odnalktszcfoxpcvmshw")

if __name__ == "__main__":
    main()
