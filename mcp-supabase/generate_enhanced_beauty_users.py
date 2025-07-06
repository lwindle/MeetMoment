#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成20个增强版美女用户数据，包含AI生成头像和真实信息
使用更加丰富、真实的图片提示词
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

class EnhancedAliyunImageGenerator:
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
                "negative_prompt": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, mutation, watermark, text, signature, logo, brand, artificial, fake, plastic surgery, heavy makeup, overexposed, underexposed, cartoon, anime, illustration"
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
    
    def generate_enhanced_beauty_portrait(self, style_description, lighting, pose, expression, background):
        """生成增强版美女头像，使用更丰富的提示词"""
        
        # 构建超详细的中文提示词
        prompt = f"""
超高清真实美女头像摄影作品，{style_description}，
{lighting}，{pose}，{expression}，{background}，
专业摄影师拍摄，使用85mm镜头，f/1.4光圈，浅景深背景虚化，
自然真实的亚洲女性面孔，精致五官，健康肌肤，自然妆容，
无瑕疵皮肤质感，自然光泽，真实人像摄影，
高质量，超高分辨率，8K画质，专业摄影作品，
真实感，自然美，现代时尚，优雅气质
"""
        
        print(f"正在生成增强版图片，风格: {style_description}")
        
        # 创建任务
        task_response = self.create_image_task(prompt)
        task_id = task_response['output']['task_id']
        
        print(f"任务创建成功，ID: {task_id}")
        
        # 等待完成
        result = self.wait_for_completion(task_id)
        
        if result['output']['results']:
            image_url = result['output']['results'][0]['url']
            print(f"增强版图片生成成功: {image_url}")
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

def generate_enhanced_beauty_users():
    """生成20个增强版美女用户"""
    
    if not DASHSCOPE_API_KEY:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置 Supabase 环境变量")
        return
    
    # 初始化增强版图像生成器
    image_generator = EnhancedAliyunImageGenerator(DASHSCOPE_API_KEY)
    
    # 20个增强版美女用户模板数据
    enhanced_beauty_templates = [
        {
            "nickname": "雨薇",
            "age": 25,
            "city": "杭州",
            "occupation": "室内设计师",
            "bio": "热爱空间美学，喜欢为每个家庭创造温馨的居住环境。业余时间喜欢插花和茶艺，相信生活需要仪式感。希望遇到一个有品味、懂生活的人。",
            "emotion_status": "single",
            "style_description": "优雅知性的室内设计师，栗色波浪长发自然垂肩，穿着米白色高领毛衣",
            "lighting": "温暖的午后阳光透过百叶窗洒在脸上，形成柔和的光影效果",
            "pose": "侧身坐在现代简约的椅子上，手轻抚头发",
            "expression": "温和恬静的微笑，眼神专注而温柔",
            "background": "现代简约的工作室背景，有绿植和设计图纸",
            "interests": ["室内设计", "插花", "茶艺", "美学", "家居"]
        },
        {
            "nickname": "诗涵",
            "age": 24,
            "city": "苏州",
            "occupation": "古典舞老师",
            "bio": "从小学习古典舞，毕业于舞蹈学院。喜欢传统文化，平时爱穿汉服，喜欢古诗词。性格温婉如水，希望找到一个能欣赏传统美的知音。",
            "emotion_status": "single",
            "style_description": "古典优雅的舞蹈老师，乌黑长发盘成古典发髻，穿着淡雅的旗袍",
            "lighting": "柔和的室内灯光，营造古典韵味的氛围",
            "pose": "端坐在红木椅上，双手优雅地放在膝盖上",
            "expression": "恬静淡雅的笑容，眼神清澈如水",
            "background": "古色古香的茶室，有古筝和书画作品",
            "interests": ["古典舞", "汉服", "古诗词", "书法", "传统文化"]
        },
        {
            "nickname": "晓萌",
            "age": 22,
            "city": "厦门",
            "occupation": "海洋生物学研究生",
            "bio": "海洋大学研究生，专业研究海洋生物。热爱大海和自然，经常参与海洋保护活动。性格开朗活泼，喜欢潜水和摄影。",
            "emotion_status": "single",
            "style_description": "青春活力的研究生，自然的栗色长发，穿着清新的蓝色衬衫",
            "lighting": "明亮的自然光，仿佛海边的阳光",
            "pose": "坐在实验室里，手中拿着海洋生物标本",
            "expression": "充满好奇心的灿烂笑容，眼神专注而热情",
            "background": "现代化的海洋生物实验室，有水族箱和研究设备",
            "interests": ["海洋生物", "潜水", "摄影", "环保", "科研"]
        },
        {
            "nickname": "梓琪",
            "age": 26,
            "city": "成都",
            "occupation": "心理咨询师",
            "bio": "国家二级心理咨询师，专注于情感心理治疗。喜欢倾听他人的故事，帮助别人解决心理困扰。平时喜欢瑜伽和冥想，保持内心平静。",
            "emotion_status": "single",
            "style_description": "温和专业的心理咨询师，中分的黑色长发，穿着温暖的驼色针织衫",
            "lighting": "温暖柔和的室内灯光，营造安全感的氛围",
            "pose": "坐在舒适的沙发上，双手自然放置，身体略微前倾",
            "expression": "温暖理解的微笑，眼神充满关怀和智慧",
            "background": "温馨的心理咨询室，有绿植和温暖的装饰",
            "interests": ["心理学", "瑜伽", "冥想", "阅读", "音乐治疗"]
        },
        {
            "nickname": "若汐",
            "age": 23,
            "city": "青岛",
            "occupation": "海洋摄影师",
            "bio": "自由摄影师，专门拍摄海洋主题作品。热爱旅行和探险，足迹遍布各大海岛。喜欢用镜头记录大海的美丽瞬间，希望找到一个同样热爱自由的灵魂。",
            "emotion_status": "single",
            "style_description": "自由洒脱的摄影师，海风吹动的长发，穿着休闲的白色T恤",
            "lighting": "海边的金色夕阳光线，温暖而浪漫",
            "pose": "手持相机，回眸一笑的瞬间",
            "expression": "自由奔放的笑容，眼神充满冒险精神",
            "background": "美丽的海滩背景，有海浪和礁石",
            "interests": ["摄影", "旅行", "海洋", "冲浪", "探险"]
        },
        {
            "nickname": "慕容雪",
            "age": 27,
            "city": "西安",
            "occupation": "文物修复师",
            "bio": "博物馆文物修复师，专门修复古代字画和瓷器。对历史文化有深厚兴趣，平时喜欢逛博物馆和古玩市场。性格沉静内敛，希望找到一个有文化底蕴的人。",
            "emotion_status": "single",
            "style_description": "古典知性的文物修复师，简单的低马尾，穿着素雅的中式上衣",
            "lighting": "博物馆内柔和的专业照明，突出文物的质感",
            "pose": "专注地修复古代文物，侧脸轮廓优美",
            "expression": "专注认真的神情，偶尔露出满足的微笑",
            "background": "文物修复工作室，有古代文物和修复工具",
            "interests": ["文物修复", "历史", "古代艺术", "书法", "收藏"]
        },
        {
            "nickname": "语嫣",
            "age": 25,
            "city": "南京",
            "occupation": "播音主持人",
            "bio": "电台主播，声音甜美动听。每天晚上主持情感类节目，陪伴夜归人。喜欢阅读和音乐，有一把好嗓子。希望现实中也能遇到那个对的人。",
            "emotion_status": "single",
            "style_description": "优雅的播音主持人，精致的短发造型，穿着职业的深蓝色西装",
            "lighting": "专业的演播室灯光，突出面部轮廓",
            "pose": "坐在播音台前，手持话筒",
            "expression": "专业自信的笑容，眼神温暖而有亲和力",
            "background": "现代化的广播电台演播室",
            "interests": ["播音主持", "音乐", "阅读", "声乐", "电台"]
        },
        {
            "nickname": "芷若",
            "age": 24,
            "city": "桂林",
            "occupation": "景观设计师",
            "bio": "景观设计专业毕业，热爱大自然。经常到各地采风，寻找设计灵感。喜欢徒步和登山，相信最美的风景在路上。希望找到一个同样热爱自然的人。",
            "emotion_status": "single",
            "style_description": "自然清新的景观设计师，自然卷曲的长发，穿着户外休闲装",
            "lighting": "自然的户外阳光，清新明亮",
            "pose": "站在山水之间，手中拿着设计图纸",
            "expression": "热爱自然的纯真笑容，眼神清澈明亮",
            "background": "桂林山水风光，有青山绿水",
            "interests": ["景观设计", "徒步", "登山", "摄影", "自然"]
        },
        {
            "nickname": "梦瑶",
            "age": 26,
            "city": "长沙",
            "occupation": "珠宝设计师",
            "bio": "独立珠宝设计师，有自己的工作室。喜欢用珠宝诠释女性的美丽，每一件作品都是独一无二的艺术品。性格细腻敏感，对美有独特的理解。",
            "emotion_status": "single",
            "style_description": "精致优雅的珠宝设计师，光泽的黑色长发，佩戴自己设计的精美首饰",
            "lighting": "珠宝工作室的专业灯光，突出珠宝的光泽",
            "pose": "在工作台前设计珠宝，手中拿着设计工具",
            "expression": "专注创作的神情，眼神充满艺术气息",
            "background": "精美的珠宝设计工作室，有各种宝石和设计工具",
            "interests": ["珠宝设计", "艺术", "时尚", "手工", "美学"]
        },
        {
            "nickname": "安琪",
            "age": 23,
            "city": "大连",
            "occupation": "海洋工程师",
            "bio": "海洋工程专业毕业，在海洋工程公司工作。虽然是理工科女生，但内心很温柔。喜欢大海，也喜欢精密的工程设计。希望找到一个理解我工作的人。",
            "emotion_status": "single",
            "style_description": "知性的女工程师，简洁的短发，穿着专业的工作服",
            "lighting": "现代办公室的明亮灯光",
            "pose": "在电脑前查看工程图纸，侧脸专注",
            "expression": "认真专业的神情，偶尔露出自信的微笑",
            "background": "现代化的工程设计办公室",
            "interests": ["海洋工程", "科技", "游泳", "数学", "创新"]
        },
        {
            "nickname": "紫萱",
            "age": 25,
            "city": "昆明",
            "occupation": "花艺师",
            "bio": "专业花艺师，经营着一家温馨的花店。每天与鲜花为伴，用花艺传递美好情感。性格温柔浪漫，相信每一朵花都有自己的故事。",
            "emotion_status": "single",
            "style_description": "温柔浪漫的花艺师，柔软的波浪长发，穿着碎花连衣裙",
            "lighting": "花店里温暖的自然光线，花香弥漫",
            "pose": "在花店里整理鲜花，动作优雅",
            "expression": "温柔甜美的笑容，眼神如花朵般纯净",
            "background": "充满鲜花的花艺工作室",
            "interests": ["花艺", "园艺", "摄影", "手工", "美学"]
        },
        {
            "nickname": "沐晴",
            "age": 24,
            "city": "三亚",
            "occupation": "潜水教练",
            "bio": "专业潜水教练，PADI高级开放水域潜水员。热爱海洋运动，经常带学员探索海底世界。性格开朗勇敢，喜欢挑战和冒险。",
            "emotion_status": "single",
            "style_description": "健康活力的潜水教练，阳光下的棕色长发，穿着潜水服",
            "lighting": "海边强烈的阳光，健康的小麦色肌肤",
            "pose": "站在海边，手持潜水装备",
            "expression": "阳光自信的笑容，眼神充满活力",
            "background": "美丽的三亚海滩，清澈的海水",
            "interests": ["潜水", "海洋运动", "健身", "旅行", "冒险"]
        },
        {
            "nickname": "书瑶",
            "age": 26,
            "city": "北京",
            "occupation": "图书编辑",
            "bio": "出版社编辑，负责文学类图书的编辑工作。热爱阅读和写作，相信文字的力量。性格安静内敛，喜欢在书海中寻找知音。",
            "emotion_status": "single",
            "style_description": "文静知性的图书编辑，简单的马尾辫，穿着舒适的毛衣",
            "lighting": "图书馆里柔和的阅读灯光",
            "pose": "坐在书桌前阅读，手中拿着书本",
            "expression": "专注阅读的神情，眼神充满智慧",
            "background": "温馨的图书馆或书房环境",
            "interests": ["阅读", "写作", "文学", "编辑", "咖啡"]
        },
        {
            "nickname": "欣然",
            "age": 23,
            "city": "重庆",
            "occupation": "美食博主",
            "bio": "美食博主和料理研究家，在社交媒体上分享各地美食。热爱烹饪和探店，相信美食能连接人心。性格开朗热情，喜欢和大家分享快乐。",
            "emotion_status": "single",
            "style_description": "活泼可爱的美食博主，扎着丸子头，穿着可爱的围裙",
            "lighting": "厨房里温暖的灯光，食物的香气扑鼻",
            "pose": "在厨房里烹饪，手持厨具",
            "expression": "享受烹饪的快乐笑容，眼神充满热情",
            "background": "现代化的开放式厨房",
            "interests": ["美食", "烹饪", "摄影", "旅行", "分享"]
        },
        {
            "nickname": "月儿",
            "age": 25,
            "city": "乌鲁木齐",
            "occupation": "天文学研究员",
            "bio": "天文台研究员，专门研究深空天体。从小就对星空充满好奇，经常熬夜观测星象。性格理性而浪漫，相信宇宙中有无限可能。",
            "emotion_status": "single",
            "style_description": "神秘知性的天文学家，长直发，穿着深色的研究服",
            "lighting": "天文台里微弱的红色灯光，营造神秘氛围",
            "pose": "在天文望远镜前观测，侧脸轮廓优美",
            "expression": "专注探索的神情，眼神充满好奇和智慧",
            "background": "现代化的天文观测台",
            "interests": ["天文学", "物理", "观星", "科研", "宇宙"]
        },
        {
            "nickname": "采薇",
            "age": 24,
            "city": "拉萨",
            "occupation": "藏文化研究者",
            "bio": "藏学研究专业毕业，致力于藏族文化的保护和传承。经常深入藏区进行田野调查，收集民间故事和传说。性格坚韧独立，内心纯净如雪山。",
            "emotion_status": "single",
            "style_description": "纯净质朴的文化研究者，自然的长发，穿着藏式服装",
            "lighting": "高原上纯净的阳光，清澈明亮",
            "pose": "在藏式建筑前，手中拿着研究资料",
            "expression": "纯真质朴的笑容，眼神清澈如高原湖水",
            "background": "壮美的西藏高原风光",
            "interests": ["藏文化", "人类学", "摄影", "徒步", "民俗"]
        },
        {
            "nickname": "雅琴",
            "age": 27,
            "city": "扬州",
            "occupation": "古琴演奏家",
            "bio": "古琴演奏家，师从名师学习古琴十余年。经常在茶馆和文化中心演出，用琴声传递古典之美。性格恬静淡雅，如古琴之音般悠远。",
            "emotion_status": "single",
            "style_description": "古典雅致的古琴演奏家，古典发髻，穿着素雅的汉服",
            "lighting": "古典茶室里的柔和灯光，营造古韵氛围",
            "pose": "端坐在古琴前，手指轻抚琴弦",
            "expression": "恬静淡雅的神情，眼神如古井般深邃",
            "background": "古色古香的琴室，有古琴和字画",
            "interests": ["古琴", "古典音乐", "茶艺", "古诗词", "禅修"]
        },
        {
            "nickname": "小鱼",
            "age": 22,
            "city": "哈尔滨",
            "occupation": "花样滑冰教练",
            "bio": "前花样滑冰运动员，现在是专业教练。从小在冰雪中长大，对冰雪运动有着特殊的情感。性格坚韧优雅，如冰雪般纯洁美丽。",
            "emotion_status": "single",
            "style_description": "优雅的花样滑冰教练，运动型短发，穿着专业的滑冰服装",
            "lighting": "冰场上明亮的灯光，反射出冰雪的光芒",
            "pose": "在冰面上优雅地滑行，动作轻盈",
            "expression": "专注优雅的神情，眼神坚定而美丽",
            "background": "专业的花样滑冰训练场",
            "interests": ["花样滑冰", "冰雪运动", "舞蹈", "音乐", "健身"]
        },
        {
            "nickname": "晨曦",
            "age": 26,
            "city": "福州",
            "occupation": "茶艺师",
            "bio": "高级茶艺师，经营着一家传统茶馆。精通各种茶艺表演，对茶文化有深入研究。性格温和细腻，相信一杯好茶能温暖人心。",
            "emotion_status": "single",
            "style_description": "优雅的茶艺师，简洁的盘发，穿着中式茶服",
            "lighting": "茶馆里温暖的灯光，茶香袅袅",
            "pose": "在茶台前泡茶，动作优雅流畅",
            "expression": "专注泡茶的神情，眼神温和宁静",
            "background": "传统的中式茶馆环境",
            "interests": ["茶艺", "茶文化", "书法", "古典音乐", "禅修"]
        },
        {
            "nickname": "梓涵",
            "age": 23,
            "city": "海口",
            "occupation": "热带植物研究员",
            "bio": "热带植物研究专业，在植物园工作。热爱大自然，经常深入热带雨林进行科研调查。性格开朗自然，如热带植物般充满生命力。",
            "emotion_status": "single",
            "style_description": "自然清新的植物研究员，自然的长发，穿着户外研究服装",
            "lighting": "热带植物园里斑驳的阳光，绿意盎然",
            "pose": "在热带植物中进行研究，手中拿着植物标本",
            "expression": "热爱自然的纯真笑容，眼神充满好奇",
            "background": "热带植物园的绿色环境",
            "interests": ["植物学", "生态学", "徒步", "摄影", "环保"]
        }
    ]
    
    print("🎨 开始生成20个增强版美女用户数据...")
    
    for i, template in enumerate(enhanced_beauty_templates, 1):
        try:
            print(f"\n📸 正在生成第 {i}/20 个用户: {template['nickname']}")
            
            # 生成增强版头像
            print("⏳ 正在生成增强版AI头像...")
            avatar_url = image_generator.generate_enhanced_beauty_portrait(
                template['style_description'],
                template['lighting'],
                template['pose'],
                template['expression'],
                template['background']
            )
            
            # 准备用户数据
            user_data = {
                "phone": f"139{random.randint(10000000, 99999999)}",  # 随机手机号
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
                "ai_score": random.randint(88, 99),  # 更高的AI评分
                "profile_complete": random.uniform(90.0, 99.0),
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
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
            if i < len(enhanced_beauty_templates):
                print("⏱️ 等待15秒避免API限流...")
                
                
        except Exception as e:
            print(f"❌ 创建用户 {template['nickname']} 时出错: {e}")
            continue
    
    print("\n🎊 所有20个增强版美女用户生成完成！")

if __name__ == "__main__":
    generate_enhanced_beauty_users()