#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查美女用户生成进度
"""

import os
import requests

# Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://odnalktszcfoxpcvmshw.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8')

def check_user_count():
    """检查数据库中的用户数量"""
    url = f"{SUPABASE_URL}/rest/v1/users"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 获取总用户数
    params = {
        'select': 'count'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        total_count = response.headers.get('Content-Range', '0').split('/')[-1]
        print(f"📊 数据库中总用户数: {total_count}")
        
        # 获取最近创建的用户
        recent_params = {
            'select': 'id,nickname,city,occupation,created_at',
            'order': 'created_at.desc',
            'limit': 10
        }
        
        recent_response = requests.get(url, headers=headers, params=recent_params)
        
        if recent_response.status_code == 200:
            recent_users = recent_response.json()
            print(f"\n🆕 最近创建的 {len(recent_users)} 个用户:")
            for user in recent_users:
                print(f"  • {user['nickname']} ({user['city']}) - {user['occupation']} - ID: {user['id']}")
                
        return int(total_count) if total_count.isdigit() else 0
    else:
        print(f"❌ 获取用户数量失败: {response.status_code}")
        return 0

def check_users_with_avatars():
    """检查有头像的用户数量"""
    url = f"{SUPABASE_URL}/rest/v1/users"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 获取有头像的用户
    params = {
        'select': 'id,nickname,city,avatar',
        'avatar': 'not.is.null',
        'order': 'created_at.desc'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        users_with_avatars = response.json()
        print(f"\n🖼️ 有头像的用户数量: {len(users_with_avatars)}")
        
        for user in users_with_avatars:
            avatar_status = "✅ 有头像" if user['avatar'] else "❌ 无头像"
            print(f"  • {user['nickname']} ({user['city']}) - {avatar_status}")
            
        return len(users_with_avatars)
    else:
        print(f"❌ 获取头像用户失败: {response.status_code}")
        return 0

if __name__ == "__main__":
    print("🔍 检查美女用户生成进度...\n")
    
    total_users = check_user_count()
    users_with_avatars = check_users_with_avatars()
    
    print(f"\n📈 进度总结:")
    print(f"  • 总用户数: {total_users}")
    print(f"  • 有头像用户数: {users_with_avatars}")
    print(f"  • 完成度: {(users_with_avatars/max(total_users, 1)*100):.1f}%") 