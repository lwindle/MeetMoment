#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示生成单个美女用户 - 用于测试阿里云API集成
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta

# 配置
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

def create_image_task(api_key, prompt):
    """创建图像生成任务"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'X-DashScope-Async': 'enable'
    }
    
    payload = {
        "model": "wanx2.1-t2i-turbo",
        "input": {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, mutation, watermark, text, signature, logo, brand"
        },
        "parameters": {
            "size": "1024*1024",
            "n": 1,
            "prompt_extend": True,
            "watermark": False
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"创建任务失败: {response.status_code} - {response.text}")

def query_task_result(api_key, task_id):
    """查询任务结果"""
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"查询任务失败: {response.status_code} - {response.text}")

def wait_for_completion(api_key, task_id, max_wait_time=180):
    """等待任务完成"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        try:
            result = query_task_result(api_key, task_id)
            status = result['output']['task_status']
            
            print(f"⏳ 任务状态: {status}")
            
            if status == 'SUCCEEDED':
                return result
            elif status == 'FAILED':
                raise Exception("任务失败")
            elif status in ['PENDING', 'RUNNING']:
                time.sleep(10)
            else:
                raise Exception(f"未知状态: {status}")
                
        except Exception as e:
            print(f"查询任务时出错: {e}")
            time.sleep(10)
    
    raise Exception("任务超时")

def insert_user_to_supabase(user_data):
    """插入用户数据到Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/users"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    response = requests.post(url, headers=headers, json=user_data)
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"插入用户失败: {response.status_code} - {response.text}")

def demo_generate_beauty_user():
    """演示生成单个美女用户"""
    
    # 检查环境变量
    if not DASHSCOPE_API_KEY:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        print("   获取地址: https://bailian.console.aliyun.com/")
        return False
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置 Supabase 环境变量")
        return False
    
    print("🎨 演示阿里云通义万相 + Supabase 集成")
    print("=" * 50)
    
    # 演示用户数据
    demo_user = {
        "nickname": "小雨",
        "age": 24,
        "city": "上海",
        "occupation": "UI设计师",
        "bio": "热爱设计和美食，喜欢用镜头记录生活中的美好瞬间。周末喜欢去咖啡厅看书，或者和朋友一起探索城市的小众景点。",
        "emotion_status": "single",
        "description": "温柔甜美的女孩，长发飘逸，穿着简约白色上衣，温和的笑容",
        "interests": ["摄影", "设计", "咖啡", "阅读", "旅行"]
    }
    
    try:
        print(f"👩 正在生成用户: {demo_user['nickname']}")
        
        # 1. 生成AI头像
        print("🎨 步骤1: 生成AI头像...")
        prompt = f"高清写实美女头像摄影，{demo_user['description']}，专业摄影，柔和自然光线，清晰五官，温和微笑表情，现代时尚，高质量，8K分辨率，亚洲女性，自然妆容，健康肌肤"
        
        print(f"📝 提示词: {prompt}")
        
        # 创建任务
        task_response = create_image_task(DASHSCOPE_API_KEY, prompt)
        task_id = task_response['output']['task_id']
        
        print(f"✅ 任务创建成功，ID: {task_id}")
        
        # 等待完成
        print("⏳ 等待图片生成（大约1-3分钟）...")
        result = wait_for_completion(DASHSCOPE_API_KEY, task_id)
        
        if result['output']['results']:
            avatar_url = result['output']['results'][0]['url']
            print(f"🖼️ 头像生成成功!")
            print(f"📎 图片链接: {avatar_url}")
        else:
            raise Exception("没有生成图片")
        
        # 2. 准备用户数据
        print("\n📋 步骤2: 准备用户数据...")
        user_data = {
            "phone": f"138{random.randint(10000000, 99999999)}",
            "password": "$2a$10$example.hash.password",
            "nickname": demo_user['nickname'],
            "gender": 1,  # 女性
            "age": demo_user['age'],
            "city": demo_user['city'],
            "occupation": demo_user['occupation'],
            "bio": demo_user['bio'],
            "emotion_status": demo_user['emotion_status'],
            "avatar": avatar_url,
            "verified": True,
            "is_online": random.choice([True, False]),
            "ai_score": random.randint(85, 98),
            "profile_complete": 95.0,
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 3. 保存到数据库
        print("💾 步骤3: 保存到Supabase数据库...")
        user_result = insert_user_to_supabase(user_data)
        
        if user_result:
            user_id = user_result[0]['id']
            print(f"✅ 用户保存成功，ID: {user_id}")
            
            # 4. 显示结果
            print("\n🎉 演示完成！生成的用户信息:")
            print(f"   👤 昵称: {demo_user['nickname']}")
            print(f"   🎂 年龄: {demo_user['age']}岁")
            print(f"   🏙️ 城市: {demo_user['city']}")
            print(f"   💼 职业: {demo_user['occupation']}")
            print(f"   🖼️ 头像: {avatar_url}")
            print(f"   💾 数据库ID: {user_id}")
            
            print(f"\n📝 个人简介: {demo_user['bio']}")
            print(f"🏷️ 兴趣标签: {', '.join(demo_user['interests'])}")
            
            return True
            
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

if __name__ == "__main__":
    success = demo_generate_beauty_user()
    
    if success:
        print("\n🎊 演示成功完成！")
        print("💡 现在你可以运行完整脚本生成10个用户:")
        print("   python3 generate_beauty_users.py")
    else:
        print("\n⚠️ 演示失败，请检查配置和网络连接")
        print("🔧 运行测试脚本检查问题:")
        print("   python3 test_aliyun_api.py") 