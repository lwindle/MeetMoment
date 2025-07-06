#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成20个时尚风格美女用户数据，包含性感、可爱、都市、卷发、身材修长、凹凸有致、妆容精致、耳环、御姐风格等特征
使用超详细的图片提示词
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
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

class StylishAliyunImageGenerator:
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
                "negative_prompt": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, mutation, watermark, text, signature, logo, brand, artificial, fake, cartoon, anime, illustration, child, underage, old, elderly"
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
    
    def generate_stylish_beauty_portrait(self, style_features, pose_details, fashion_details, makeup_details, background_setting):
        """生成时尚风格美女头像，使用超详细的提示词"""
        
        # 构建超详细的中文提示词
        prompt = f"""
超高清时尚美女摄影作品，{style_features}，
{pose_details}，{fashion_details}，{makeup_details}，{background_setting}，
专业时尚摄影师拍摄，使用85mm人像镜头，f/1.4大光圈，完美景深控制，
成熟魅力的亚洲女性，精致立体五官，完美身材比例，优雅气质，
无瑕疵肌肤质感，自然健康光泽，高端时尚摄影风格，
超高质量，8K超高分辨率，专业摄影作品，
时尚杂志封面品质，现代都市风格，优雅性感魅力
"""
        
        print(f"正在生成时尚风格图片: {style_features}")
        
        # 创建任务
        task_response = self.create_image_task(prompt)
        task_id = task_response['output']['task_id']
        
        print(f"任务创建成功，ID: {task_id}")
        
        # 等待完成
        result = self.wait_for_completion(task_id)
        
        if result['output']['results']:
            image_url = result['output']['results'][0]['url']
            print(f"时尚风格图片生成成功: {image_url}")
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

def generate_stylish_beauty_users():
    """生成20个时尚风格美女用户"""
    
    if not DASHSCOPE_API_KEY:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        return
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("❌ 请设置 Supabase 环境变量")
        return
    
    # 初始化时尚风格图像生成器
    image_generator = StylishAliyunImageGenerator(DASHSCOPE_API_KEY)
    
    # 20个时尚风格美女用户模板数据
    stylish_beauty_templates = [
        {
            "nickname": "璐璐",
            "age": 26,
            "city": "上海",
            "occupation": "时尚博主",
            "bio": "时尚界的新星，拥有独特的审美眼光。热爱高端时尚，经常参加时装周和品牌活动。相信每个女人都应该活出自己的精彩。",
            "emotion_status": "single",
            "style_features": "性感御姐风格的时尚博主，蓬松卷发披肩，身材修长凹凸有致，气质高贵冷艳",
            "pose_details": "优雅地靠在落地窗前，一手轻抚卷发，侧身展现完美身材曲线",
            "fashion_details": "穿着黑色紧身连衣裙，佩戴精致的钻石耳环和项链，高跟鞋",
            "makeup_details": "妆容精致完美，烟熏眼妆，丰满红唇，立体轮廓",
            "background_setting": "现代奢华的都市公寓，落地窗外是繁华夜景",
            "interests": ["时尚", "奢侈品", "摄影", "旅行", "美妆"]
        },
        {
            "nickname": "安琪儿",
            "age": 24,
            "city": "北京",
            "occupation": "模特",
            "bio": "职业模特，拥有天使般的面容和魔鬼般的身材。热爱镜头前的每一刻，相信美丽是一种态度。希望找到欣赏我的人。",
            "emotion_status": "single",
            "style_features": "可爱性感的职业模特，金色大波浪卷发，身材高挑纤细，甜美中带着妩媚",
            "pose_details": "坐在化妆台前，回眸一笑，手轻触耳边的卷发",
            "fashion_details": "穿着粉色丝绸吊带裙，佩戴珍珠耳环，精致手镯",
            "makeup_details": "清透底妆，粉色眼影，水润粉唇，自然腮红",
            "background_setting": "专业摄影棚，柔和的灯光营造梦幻氛围",
            "interests": ["模特", "时尚", "健身", "舞蹈", "美容"]
        },
        {
            "nickname": "薇薇",
            "age": 28,
            "city": "深圳",
            "occupation": "金融分析师",
            "bio": "金融界的精英女性，白天是严谨的分析师，晚上是优雅的都市女郎。喜欢挑战，追求完美，相信实力与美貌并存。",
            "emotion_status": "single",
            "style_features": "都市御姐风格的金融精英，栗色卷发优雅盘起，身材完美比例，知性魅力十足",
            "pose_details": "站在办公室落地窗前，手持文件，专业而优雅的姿态",
            "fashion_details": "穿着定制西装套装，佩戴名牌手表和耳钉，职业而时尚",
            "makeup_details": "精致职业妆容，眼线清晰，唇色优雅，整体干练",
            "background_setting": "现代化的金融中心办公室，城市天际线背景",
            "interests": ["金融", "投资", "高尔夫", "红酒", "艺术"]
        },
        {
            "nickname": "娜娜",
            "age": 25,
            "city": "广州",
            "occupation": "服装设计师",
            "bio": "才华横溢的服装设计师，对时尚有着敏锐的嗅觉。每一件作品都是艺术品，相信服装能表达女性的内在美。",
            "emotion_status": "single",
            "style_features": "时尚前卫的设计师，深棕色螺旋卷发，身材纤细修长，艺术气质浓厚",
            "pose_details": "在设计工作室中，手持设计图纸，专注而优雅",
            "fashion_details": "穿着自己设计的创意连衣裙，搭配设计感耳环和手镯",
            "makeup_details": "创意妆容，强调眼部轮廓，个性唇色，艺术感十足",
            "background_setting": "充满创意的服装设计工作室，面料和设计图纸",
            "interests": ["服装设计", "艺术", "时尚", "手工", "创意"]
        },
        {
            "nickname": "莉莉",
            "age": 27,
            "city": "杭州",
            "occupation": "律师",
            "bio": "资深律师，法庭上的女王。拥有锐利的思维和优雅的外表，相信正义与美丽同样重要。寻找能理解我职业的伴侣。",
            "emotion_status": "single",
            "style_features": "知性御姐风格的律师，黑色卷发严谨盘起，身材高挑优雅，气场强大",
            "pose_details": "坐在律师事务所中，手持法律文件，自信而专业",
            "fashion_details": "穿着黑色职业套装，佩戴简约而精致的耳环和胸针",
            "makeup_details": "专业妆容，突出眼神的锐利，唇色庄重而优雅",
            "background_setting": "现代化的律师事务所，法律书籍和文件背景",
            "interests": ["法律", "辩论", "阅读", "古典音乐", "收藏"]
        },
        {
            "nickname": "思琪",
            "age": 23,
            "city": "成都",
            "occupation": "网红主播",
            "bio": "人气网红主播，拥有甜美的外表和有趣的灵魂。每天和粉丝分享生活的美好，相信快乐是最好的化妆品。",
            "emotion_status": "single",
            "style_features": "可爱甜美的网红主播，粉色卷发蓬松可爱，身材娇小玲珑，青春活力",
            "pose_details": "在直播间中，对着镜头甜美微笑，做可爱手势",
            "fashion_details": "穿着粉色蕾丝连衣裙，佩戴可爱的耳环和项链",
            "makeup_details": "甜美妆容，大眼妆，粉嫩唇色，可爱腮红",
            "background_setting": "温馨的直播间，粉色装饰和柔和灯光",
            "interests": ["直播", "美妆", "游戏", "动漫", "美食"]
        },
        {
            "nickname": "雅雅",
            "age": 29,
            "city": "武汉",
            "occupation": "医美医生",
            "bio": "专业医美医生，致力于帮助女性变得更美。自己就是最好的广告，相信科学的美丽。希望找到一个懂得欣赏美的人。",
            "emotion_status": "single",
            "style_features": "精致优雅的医美医生，波浪卷发完美造型，身材比例完美，气质出众",
            "pose_details": "在诊所中，专业而优雅地查看资料，展现专业魅力",
            "fashion_details": "穿着白色医生大衣配精致内搭，佩戴高端耳环和手表",
            "makeup_details": "完美无瑕的妆容，突出立体五官，自然而精致",
            "background_setting": "高端医美诊所，现代化医疗设备背景",
            "interests": ["医美", "护肤", "健身", "瑜伽", "美容"]
        },
        {
            "nickname": "小蝶",
            "age": 24,
            "city": "西安",
            "occupation": "舞蹈老师",
            "bio": "专业舞蹈老师，身体就是最美的艺术品。热爱舞蹈带来的自由感，相信每个动作都能诠释美丽。",
            "emotion_status": "single",
            "style_features": "优雅性感的舞蹈老师，栗色卷发自然飘逸，身材修长柔韧，舞者气质",
            "pose_details": "在舞蹈室中，正在做优美的舞蹈动作，身姿曼妙",
            "fashion_details": "穿着贴身舞蹈服，搭配精致的耳环，展现身材曲线",
            "makeup_details": "舞台妆容，强调眼部表现力，唇色鲜艳，整体精致",
            "background_setting": "专业舞蹈教室，镜子和把杆背景",
            "interests": ["舞蹈", "音乐", "健身", "瑜伽", "表演"]
        },
        {
            "nickname": "晴儿",
            "age": 26,
            "city": "南京",
            "occupation": "珠宝设计师",
            "bio": "高端珠宝设计师，每一件作品都是艺术珍品。相信珠宝能衬托女性的美丽，自己也是珠宝最好的模特。",
            "emotion_status": "single",
            "style_features": "奢华优雅的珠宝设计师，金棕色卷发华丽造型，身材高贵典雅，贵族气质",
            "pose_details": "在珠宝工作室中，手持精美珠宝，优雅展示",
            "fashion_details": "穿着黑色晚礼服，佩戴自己设计的珍贵珠宝耳环和项链",
            "makeup_details": "奢华妆容，金色眼影，红色唇彩，突出贵族气质",
            "background_setting": "高端珠宝设计工作室，珠宝展示柜背景",
            "interests": ["珠宝设计", "奢侈品", "艺术", "收藏", "时尚"]
        },
        {
            "nickname": "美美",
            "age": 25,
            "city": "重庆",
            "occupation": "美容顾问",
            "bio": "专业美容顾问，帮助女性发现自己的美丽。自己就是美丽的代言人，相信每个女人都有独特的魅力。",
            "emotion_status": "single",
            "style_features": "甜美可爱的美容顾问，蜜糖色卷发甜美可人，身材娇小精致，亲和力十足",
            "pose_details": "在美容院中，正在为客户提供咨询，温柔而专业",
            "fashion_details": "穿着粉色职业装，佩戴珍珠耳环，温柔而专业",
            "makeup_details": "清新自然妆容，强调肌肤质感，粉色系妆容",
            "background_setting": "高端美容院，温馨的咨询环境",
            "interests": ["美容", "护肤", "化妆", "时尚", "健康"]
        },
        {
            "nickname": "欣怡",
            "age": 28,
            "city": "天津",
            "occupation": "品牌经理",
            "bio": "国际品牌经理，经常出席高端活动。拥有国际化视野和优雅气质，相信品味决定人生高度。",
            "emotion_status": "single",
            "style_features": "国际化都市女性，深棕色大波浪卷发，身材高挑完美，国际范十足",
            "pose_details": "在品牌发布会现场，优雅地与客户交流，展现专业魅力",
            "fashion_details": "穿着国际大牌套装，佩戴限量版耳环和手表",
            "makeup_details": "国际化妆容，突出立体五官，优雅而时尚",
            "background_setting": "高端品牌发布会现场，时尚背景",
            "interests": ["品牌管理", "时尚", "旅行", "红酒", "艺术"]
        },
        {
            "nickname": "诗诗",
            "age": 24,
            "city": "青岛",
            "occupation": "摄影师",
            "bio": "时尚摄影师，用镜头捕捉美丽瞬间。自己也是镜头前的美丽主角，相信美丽需要被记录和分享。",
            "emotion_status": "single",
            "style_features": "艺术气质的摄影师，自然卷发随性飘逸，身材纤细修长，文艺范十足",
            "pose_details": "手持专业相机，在拍摄现场，专注而美丽",
            "fashion_details": "穿着时尚休闲装，佩戴个性化耳环，展现艺术气质",
            "makeup_details": "自然妆容，突出眼神的灵动，整体清新脱俗",
            "background_setting": "时尚摄影工作室，专业设备背景",
            "interests": ["摄影", "艺术", "旅行", "电影", "音乐"]
        },
        {
            "nickname": "婉儿",
            "age": 27,
            "city": "苏州",
            "occupation": "酒店经理",
            "bio": "五星级酒店经理，接待过无数名流贵客。拥有优雅的谈吐和完美的仪态，相信细节决定品质。",
            "emotion_status": "single",
            "style_features": "优雅知性的酒店经理，黑色卷发典雅盘起，身材高贵优雅，服务业的完美典范",
            "pose_details": "在酒店大堂中，优雅地接待客人，展现专业素养",
            "fashion_details": "穿着高端职业套装，佩戴经典耳环和胸针",
            "makeup_details": "经典妆容，突出专业形象，优雅而庄重",
            "background_setting": "五星级酒店豪华大堂，奢华装饰背景",
            "interests": ["酒店管理", "服务", "礼仪", "语言", "文化"]
        },
        {
            "nickname": "悦悦",
            "age": 23,
            "city": "厦门",
            "occupation": "化妆师",
            "bio": "专业化妆师，为无数女性打造完美妆容。自己就是化妆艺术的最佳展示，相信化妆是一门艺术。",
            "emotion_status": "single",
            "style_features": "时尚前卫的化妆师，彩色挑染卷发个性十足，身材时尚纤细，潮流先锋",
            "pose_details": "在化妆工作室中，正在化妆，展现专业技艺",
            "fashion_details": "穿着时尚潮流服装，佩戴前卫设计的耳环",
            "makeup_details": "创意化妆，色彩丰富，展现化妆技艺",
            "background_setting": "专业化妆工作室，化妆品和工具背景",
            "interests": ["化妆", "美容", "时尚", "艺术", "创意"]
        },
        {
            "nickname": "灵儿",
            "age": 26,
            "city": "长沙",
            "occupation": "瑜伽教练",
            "bio": "专业瑜伽教练，拥有完美的身材和心灵的平静。相信瑜伽能带来内在和外在的美丽，寻找同样热爱健康的伴侣。",
            "emotion_status": "single",
            "style_features": "健康性感的瑜伽教练，自然卷发清新脱俗，身材匀称健美，健康美丽",
            "pose_details": "在瑜伽馆中，正在做优美的瑜伽动作，身姿曼妙",
            "fashion_details": "穿着贴身瑜伽服，佩戴简约耳环，展现健康美",
            "makeup_details": "清新自然妆容，突出健康肌肤，整体清爽",
            "background_setting": "温馨的瑜伽教室，自然光线和植物背景",
            "interests": ["瑜伽", "健身", "冥想", "健康", "自然"]
        },
        {
            "nickname": "韵韵",
            "age": 29,
            "city": "大连",
            "occupation": "艺术总监",
            "bio": "广告公司艺术总监，创意无限的艺术家。用视觉语言诠释美丽，自己也是艺术作品的一部分。",
            "emotion_status": "single",
            "style_features": "创意十足的艺术总监，酒红色卷发个性张扬，身材艺术感十足，创意无限",
            "pose_details": "在设计工作室中，正在创作，展现艺术才华",
            "fashion_details": "穿着设计感强的服装，佩戴艺术化耳环和饰品",
            "makeup_details": "艺术化妆容，色彩大胆，创意十足",
            "background_setting": "创意设计工作室，艺术作品和设计图背景",
            "interests": ["艺术", "设计", "创意", "绘画", "摄影"]
        },
        {
            "nickname": "倩倩",
            "age": 25,
            "city": "福州",
            "occupation": "公关经理",
            "bio": "知名企业公关经理，经常出席各种社交场合。拥有出色的社交能力和迷人的魅力，相信沟通是艺术。",
            "emotion_status": "single",
            "style_features": "社交名媛风格的公关经理，金色卷发华丽动人，身材优雅迷人，社交女王",
            "pose_details": "在商务酒会中，优雅地与人交谈，展现社交魅力",
            "fashion_details": "穿着高端晚礼服，佩戴华丽的耳环和项链",
            "makeup_details": "社交妆容，突出魅力，优雅而迷人",
            "background_setting": "高端商务酒会现场，奢华背景",
            "interests": ["公关", "社交", "时尚", "艺术", "旅行"]
        },
        {
            "nickname": "妍妍",
            "age": 24,
            "city": "昆明",
            "occupation": "空乘",
            "bio": "国际航空公司空乘，飞遍世界各地。拥有国际化的视野和优雅的气质，相信世界很大，爱情很美。",
            "emotion_status": "single",
            "style_features": "优雅知性的空乘人员，深棕色卷发专业造型，身材高挑匀称，国际化气质",
            "pose_details": "在机舱中，专业而优雅地为乘客服务，展现职业魅力",
            "fashion_details": "穿着航空公司制服，佩戴职业化耳环，优雅专业",
            "makeup_details": "职业妆容，突出亲和力，优雅而专业",
            "background_setting": "豪华客机内部，国际化背景",
            "interests": ["旅行", "语言", "文化", "服务", "时尚"]
        },
        {
            "nickname": "柔柔",
            "age": 27,
            "city": "海口",
            "occupation": "SPA馆长",
            "bio": "高端SPA会所馆长，致力于为女性提供身心放松的服务。自己就是最好的代言人，相信美丽需要用心呵护。",
            "emotion_status": "single",
            "style_features": "温柔优雅的SPA馆长，浅棕色卷发柔美动人，身材柔美迷人，温柔如水",
            "pose_details": "在SPA会所中，温柔地为客户提供服务，展现专业关怀",
            "fashion_details": "穿着专业SPA服装，佩戴温柔的耳环，整体柔美",
            "makeup_details": "温柔妆容，强调柔美气质，整体温暖",
            "background_setting": "高端SPA会所，温馨放松的环境",
            "interests": ["SPA", "美容", "养生", "瑜伽", "健康"]
        },
        {
            "nickname": "甜甜",
            "age": 23,
            "city": "拉萨",
            "occupation": "旅游博主",
            "bio": "旅游博主，用镜头记录世界的美丽。拥有甜美的笑容和冒险的心，相信最美的风景在路上，最好的爱情在远方。",
            "emotion_status": "single",
            "style_features": "甜美可爱的旅游博主，蜜糖色卷发甜美可人，身材娇小可爱，青春活力",
            "pose_details": "在美丽的风景前，甜美地拍照，展现旅行的快乐",
            "fashion_details": "穿着旅行休闲装，佩戴民族风耳环，自然可爱",
            "makeup_details": "清新甜美妆容，突出青春活力，整体可爱",
            "background_setting": "西藏美丽的自然风光，雪山和蓝天背景",
            "interests": ["旅行", "摄影", "探险", "文化", "自然"]
        }
    ]
    
    print("🎨 开始生成20个时尚风格美女用户数据...")
    
    for i, template in enumerate(stylish_beauty_templates, 1):
        try:
            print(f"\n📸 正在生成第 {i}/20 个用户: {template['nickname']}")
            
            # 生成时尚风格头像
            print("⏳ 正在生成时尚风格AI头像...")
            avatar_url = image_generator.generate_stylish_beauty_portrait(
                template['style_features'],
                template['pose_details'],
                template['fashion_details'],
                template['makeup_details'],
                template['background_setting']
            )
            
            # 准备用户数据
            user_data = {
                "phone": f"150{random.randint(10000000, 99999999)}",  # 随机手机号
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
                "ai_score": random.randint(90, 99),  # 超高AI评分
                "profile_complete": random.uniform(95.0, 99.9),
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 45))).isoformat(),
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
            if i < len(stylish_beauty_templates):
                print("⏱️ 等待20秒避免API限流...")
                
        except Exception as e:
            print(f"❌ 创建用户 {template['nickname']} 时出错: {e}")
            continue
    
    print("\n🎊 所有20个时尚风格美女用户生成完成！")

if __name__ == "__main__":
    generate_stylish_beauty_users() 