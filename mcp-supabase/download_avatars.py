#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载用户头像并保存到本地
"""

import os
import requests
import json
from urllib.parse import urlparse
from datetime import datetime

# Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

def get_users_with_avatars():
    """获取所有有头像的用户"""
    url = f"{SUPABASE_URL}/rest/v1/users?select=id,nickname,avatar&avatar=not.is.null"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"获取用户失败: {response.status_code} - {response.text}")

def download_image(url, save_path):
    """下载图片到本地"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"❌ 下载失败 {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 下载错误 {url}: {e}")
        return False

def update_user_avatar(user_id, new_avatar_path):
    """更新用户的头像路径到本地路径"""
    url = f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {"avatar": new_avatar_path}
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return True
    else:
        print(f"❌ 更新用户头像失败: {response.status_code} - {response.text}")
        return False

def download_all_avatars():
    """下载所有用户头像"""
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置Supabase环境变量")
        return
    
    # 创建保存目录
    save_dir = "downloaded_avatars"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"📁 创建目录: {save_dir}")
    
    try:
        # 获取所有用户
        users = get_users_with_avatars()
        print(f"👥 找到 {len(users)} 个有头像的用户")
        
        success_count = 0
        
        for user in users:
            user_id = user['id']
            nickname = user['nickname']
            avatar_url = user['avatar']
            
            # 检查是否是阿里云OSS链接
            if 'dashscope-result' not in avatar_url:
                print(f"⏭️ 跳过 {nickname}: 不是阿里云生成的头像")
                continue
            
            print(f"\n📸 处理用户: {nickname} (ID: {user_id})")
            print(f"🔗 原始链接: {avatar_url}")
            
            # 解析文件名
            parsed_url = urlparse(avatar_url)
            file_extension = os.path.splitext(parsed_url.path)[1] or '.png'
            filename = f"user_{user_id}_{nickname}{file_extension}"
            save_path = os.path.join(save_dir, filename)
            
            # 下载图片
            print(f"⬇️ 正在下载...")
            if download_image(avatar_url, save_path):
                print(f"✅ 下载成功: {save_path}")
                
                # 更新数据库中的头像路径（可选）
                # local_path = f"/avatars/{filename}"
                # if update_user_avatar(user_id, local_path):
                #     print(f"✅ 数据库更新成功")
                
                success_count += 1
            else:
                print(f"❌ 下载失败")
        
        print(f"\n🎉 下载完成!")
        print(f"📊 成功下载: {success_count}/{len(users)} 个头像")
        print(f"📁 保存位置: {os.path.abspath(save_dir)}")
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")

def list_downloaded_avatars():
    """列出已下载的头像"""
    save_dir = "downloaded_avatars"
    
    if not os.path.exists(save_dir):
        print("📁 还没有下载任何头像")
        return
    
    files = [f for f in os.listdir(save_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not files:
        print("📁 目录为空")
        return
    
    print(f"📁 已下载的头像 ({len(files)} 个):")
    print("=" * 50)
    
    for i, filename in enumerate(files, 1):
        file_path = os.path.join(save_dir, filename)
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"{i:2d}. {filename}")
        print(f"    📏 大小: {file_size_mb:.2f} MB")
        print(f"    📍 路径: {os.path.abspath(file_path)}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_downloaded_avatars()
    else:
        print("🎨 开始下载用户头像...")
        print("=" * 50)
        download_all_avatars()
        print("\n" + "=" * 50)
        print("💡 查看已下载文件: python3 download_avatars.py list") 