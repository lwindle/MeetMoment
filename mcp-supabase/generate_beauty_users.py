#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成美女用户数据，包含AI生成头像和真实信息
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta

# 阿里云DashScope API配置
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

# Supabase配置
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://odnalktszcfoxpcvmshw.supabase.co')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8')

class AliyunImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-DashScope-Async': 'enable'
        }
    
    def create_image_task(self, prompt):
        """创建图像生成任务"""
        url = f"{DASHSCOPE_BASE_URL}/services/aigc/text2image/image-synthesis"
        
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
        
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"创建任务失败: {response.status_code} - {response.text}")
    
    def query_task_result(self, task_id):
        """查询任务结果"""
        url = f"{DASHSCOPE_BASE_URL}/tasks/{task_id}"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"查询任务失败: {response.status_code} - {response.text}")
    
    def wait_for_completion(self, task_id, max_wait_time=300):
        """等待任务完成"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                result = self.query_task_result(task_id)
                status = result['output']['task_status']
                
                print(f"任务状态: {status}")
                
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
    
    def generate_beauty_portrait(self, description):
        """生成美女头像"""
        # 构建详细的中文提示词
        prompt = f"""高清写实美女头像摄影，{description}，专业摄影，柔和自然光线，清晰五官，温和微笑表情，现代时尚，高质量，8K分辨率，亚洲女性，自然妆容，健康肌肤"""
        
        print(f"正在生成图片，提示词: {prompt}")
        
        # 创建任务
        task_response = self.create_image_task(prompt)
        task_id = task_response['output']['task_id']
        
        print(f"任务创建成功，ID: {task_id}")
        
        # 等待完成
        result = self.wait_for_completion(task_id)
        
        if result['output']['results']:
            image_url = result['output']['results'][0]['url']
            print(f"图片生成成功: {image_url}")
            return image_url
        else:
            raise Exception("没有生成图片")

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

def insert_user_interests(user_id, interests):
    """插入用户兴趣标签"""
    url = f"{SUPABASE_URL}/rest/v1/user_interests"
    
    headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json'
    }
    
    for interest in interests:
        interest_data = {
            'user_id': user_id,
            'tag': interest,
            'ai_generated': True
        }
        
        response = requests.post(url, headers=headers, json=interest_data)
        if response.status_code not in [200, 201]:
            print(f"插入兴趣标签失败: {interest} - {response.text}")

def generate_beauty_users():
    """生成10个美女用户"""
    
    if not DASHSCOPE_API_KEY:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置 Supabase 环境变量")
        return
    
    # 初始化图像生成器
    image_generator = AliyunImageGenerator(DASHSCOPE_API_KEY)
    
    # 美女用户模板数据
    beauty_templates = [
{
"nickname": "绯棕御",
"age": 28,
"city": "上海",
"occupation": "时尚主编",
"bio": "执掌潮流话语权，偏爱高定与威士忌。在名利场游刃有余，却独爱深夜书房的独处时光。",
"emotion_status": "single",
"description": "致命性感的御姐，棕粉渐变长卷发大波浪，发根深棕发梢粉雾紫，挑染几缕银灰色发丝。身穿酒红色丝绒裹身长裙，深 V 开到腰际，露出小麦色肌肤与精致锁骨链。眼妆采用烟熏棕搭配粉紫色亮片，红唇如浆果饱满，指尖夹着细长雪茄，身后是落地窗外的城市夜景，气场全开又透着慵懒魅惑",
"interests": ["高定设计", "威士忌品鉴", "艺术策展", "马术", "深夜阅读"]
},
{
"nickname": "褐粉刃",
"age": 29,
"city": "北京",
"occupation": "格斗教练",
"bio": "用拳头击碎偏见，私下爱收集中古珠宝。在拳台是冷酷教官，转身能泡出一壶温柔的手冲咖啡。",
"emotion_status": "single",
"description": "力量感性感御姐，深棕色短发挑染樱花粉挑染，发型利落露出清晰下颌线。穿着黑色皮质运动背心 + 战术裤，小麦色肌肤上有运动后的薄汗光泽，手臂肌肉线条流畅，眉骨处有一道淡粉色疤痕。眼神锐利如刀，却在唇角勾起时露出反差萌，腰间挂着格斗手套，背景是格斗场的金属围栏，荷尔蒙与危险气息交织",
"interests": ["综合格斗", "中古珠宝", "手冲咖啡", "机械摩托", "硬核音乐"]
},
{
"nickname": "檀粉魅",
"age": 27,
"city": "广州",
"occupation": "调香师",
"bio": "在香氛里构建灵魂，迷恋木质调与皮革味。擅长用气味操纵情绪，却在遇见鸢尾花时乱了心跳。",
"emotion_status": "single",
"description": "神秘性感的御姐，深棕色长卷发中编入股股樱花粉发丝，发尾烫成复古羊毛卷。身穿驼色皮革风衣内搭藕粉色蕾丝吊带，颈间缠绕同色系丝巾，手腕叠戴多枚铜质香水瓶手链。眼妆采用肉桂棕眼影搭配粉色珠光卧蚕，唇色是裸粉调豆沙色，指尖沾着淡粉色香精油，身后是摆满香水瓶的古董木架，空气中弥漫着檀木与玫瑰的混合香气",
"interests": ["香氛调香", "皮革工艺", "古籍修复", "植物学", "老电影"]
},
{
"nickname": "灼粉翎",
"age": 30,
"city": "深圳",
"occupation": "赛车手",
"bio": "在赛道燃烧肾上腺素，私下爱拼乐高机械组。能单手漂移过弯，也能耐心拼完千片星空拼图。",
"emotion_status": "single",
"description": "速度感性感御姐，深棕色脏辫中穿插粉色荧光绳，发尾绑着赛车彩带。穿着碳纤维赛车服，拉链拉至胸口露出黑色运动内衣，手臂有赛车图腾纹身，膝盖处有磨损痕迹。脸上沾着机油与粉色荧光颜料，眼神在头盔下闪着野性光芒，身后是火焰涂装的赛车，轮胎青烟与粉色烟雾弹交织，充满叛逆与危险的吸引力",
"interests": ["赛车竞技", "机械乐高", "极限运动", "改装车", "电子音乐"]
},
{
"nickname": "栗粉靡",
"age": 28,
"city": "杭州",
"occupation": "昆曲演员",
"bio": "在戏台上唱尽悲欢，现实中爱研究哥特文学。水袖挥舞间是古典佳人，合上书卷后是暗黑系御姐。",
"emotion_status": "single",
"description": "古典性感的御姐，深栗色长发中编入樱花粉丝线，盘成复古发髻点缀珍珠与粉色琉璃珠。穿着墨色改良昆曲褶子，领口与袖口绣着粉色缠枝莲，低开叉露出黑色蕾丝长筒袜。眼妆采用工笔重彩技法，棕红色眼线勾勒出凤眼，眼角点着粉色泪痣，唇色是暗粉色咬唇妆，手持黑色折扇半遮面，身后是青瓦白墙配哥特式烛台，传统与暗黑美学碰撞",
"interests": ["昆曲表演", "哥特文学", "传统刺绣", "古着收藏", "悬疑电影"]
}
]
    
    print("🎨 开始生成美女用户数据...")
    
    for i, template in enumerate(beauty_templates, 1):
        try:
            print(f"\n📸 正在生成第 {i}/10 个用户: {template['nickname']}")
            
            # 生成头像
            print("⏳ 正在生成AI头像...")
            avatar_url = image_generator.generate_beauty_portrait(template['description'])
            
            # 准备用户数据
            user_data = {
                "phone": f"138{random.randint(10000000, 99999999)}",  # 随机手机号
                "password": "$2a$10$example.hash.password",  # 占位密码哈希
                "nickname": template['nickname'],
                "gender": 2,  # 女性
                "age": template['age'],
                "city": template['city'],
                "occupation": template['occupation'],
                "bio": template['bio'],
                "emotion_status": template['emotion_status'],
                "avatar": avatar_url,
                "verified": True,
                "is_online": random.choice([True, False]),
                "ai_score": random.randint(85, 98),  # 高AI评分
                "profile_complete": 95.0,
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # 插入用户数据
            print("💾 正在保存用户数据...")
            user_result = insert_user_to_supabase(user_data)
            
            if user_result:
                user_id = user_result[0]['id']
                print(f"✅ 用户创建成功，ID: {user_id}")
                
                # 插入兴趣标签
                print("🏷️ 正在添加兴趣标签...")
                insert_user_interests(user_id, template['interests'])
                
                print(f"🎉 {template['nickname']} 创建完成！")
                
            # 避免API限流，等待一段时间
            if i < len(beauty_templates):
                print("⏱️ 等待10秒避免API限流...")
                
        except Exception as e:
            print(f"❌ 创建用户 {template['nickname']} 时出错: {e}")
            continue
    
    print("\n🎊 所有美女用户生成完成！")

if __name__ == "__main__":
    generate_beauty_users() 