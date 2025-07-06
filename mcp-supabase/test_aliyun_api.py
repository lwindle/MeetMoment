#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云通义万相API连接
"""

import os
import requests
import json

def test_aliyun_api():
    """测试阿里云API连接"""
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY', '')
    if not api_key:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        print("   export DASHSCOPE_API_KEY='your-api-key'")
        return False
    
    print(f"✅ API密钥已设置: {api_key[:20]}...")
    
    # 测试API连接
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'X-DashScope-Async': 'enable'
    }
    
    payload = {
        "model": "wanx2.1-t2i-turbo",
        "input": {
            "prompt": "测试图片生成，一朵简单的花",
            "negative_prompt": "low quality, blurry"
        },
        "parameters": {
            "size": "1024*1024",
            "n": 1,
            "prompt_extend": True,
            "watermark": False
        }
    }
    
    try:
        print("🔄 正在测试API连接...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API连接成功！")
            print(f"📝 任务ID: {result.get('output', {}).get('task_id', 'N/A')}")
            return True
        else:
            print(f"❌ API连接失败: {response.status_code}")
            print(f"📄 错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_supabase_connection():
    """测试Supabase连接"""
    
    supabase_url = os.getenv('SUPABASE_URL', '')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
    
    if not supabase_url or not supabase_key:
        print("❌ 请设置Supabase环境变量")
        print("   export SUPABASE_URL='https://your-project.supabase.co'")
        print("   export SUPABASE_SERVICE_ROLE_KEY='your-service-role-key'")
        return False
    
    print(f"✅ Supabase URL: {supabase_url}")
    print(f"✅ Service Role Key: {supabase_key[:20]}...")
    
    # 测试数据库连接
    url = f"{supabase_url}/rest/v1/users?select=count"
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔄 正在测试Supabase连接...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Supabase连接成功！")
            return True
        else:
            print(f"❌ Supabase连接失败: {response.status_code}")
            print(f"📄 错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase连接错误: {e}")
        return False

if __name__ == "__main__":
    print("🧪 开始测试阿里云和Supabase连接...")
    print("=" * 50)
    
    # 测试阿里云API
    print("\n1️⃣ 测试阿里云通义万相API:")
    aliyun_ok = test_aliyun_api()
    
    # 测试Supabase
    print("\n2️⃣ 测试Supabase数据库:")
    supabase_ok = test_supabase_connection()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"   阿里云API: {'✅ 正常' if aliyun_ok else '❌ 异常'}")
    print(f"   Supabase: {'✅ 正常' if supabase_ok else '❌ 异常'}")
    
    if aliyun_ok and supabase_ok:
        print("\n🎉 所有服务连接正常，可以开始生成美女用户数据！")
        print("   运行命令: python3 generate_beauty_users.py")
    else:
        print("\n⚠️ 请修复上述问题后再运行生成脚本") 