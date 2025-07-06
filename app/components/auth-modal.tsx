"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { X, Upload, Sparkles, Loader2, AlertCircle } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface AuthModalProps {
  onClose: () => void
  onLogin: (userData: any) => void
}

interface FormErrors {
  phone?: string
  password?: string
  nickname?: string
  age?: string
  city?: string
  occupation?: string
  hobbies?: string
  general?: string
}

export default function AuthModal({ onClose, onLogin }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<FormErrors>({})
  const [formData, setFormData] = useState({
    phone: "",
    password: "",
    nickname: "",
    gender: "",
    age: "",
    city: "",
    occupation: "",
    hobbies: "",
    emotionStatus: "",
    photo: null,
  })
  const [aiGeneratedTags, setAiGeneratedTags] = useState<string[]>([])
  const [isGeneratingTags, setIsGeneratingTags] = useState(false)

  // 表单验证函数
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    // 手机号验证
    const phoneRegex = /^1[3-9]\d{9}$/
    if (!formData.phone) {
      newErrors.phone = "请输入手机号"
    } else if (!phoneRegex.test(formData.phone)) {
      newErrors.phone = "请输入有效的手机号"
    }

    // 密码验证
    if (!formData.password) {
      newErrors.password = "请输入密码"
    } else if (formData.password.length < 6) {
      newErrors.password = "密码至少6位"
    }

    // 注册时的额外验证
    if (!isLogin) {
      if (!formData.nickname) {
        newErrors.nickname = "请输入昵称"
      } else if (formData.nickname.length < 2) {
        newErrors.nickname = "昵称至少2个字符"
      }

      if (!formData.age) {
        newErrors.age = "请输入年龄"
      } else {
        const age = parseInt(formData.age)
        if (age < 18 || age > 60) {
          newErrors.age = "年龄需在18-60岁之间"
        }
      }

      if (!formData.city) {
        newErrors.city = "请输入所在城市"
      }

      if (!formData.occupation) {
        newErrors.occupation = "请输入职业"
      }

      if (!formData.hobbies || formData.hobbies.length < 5) {
        newErrors.hobbies = "请详细描述你的兴趣爱好（至少5个字符）"
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // 模拟AI生成标签
  const generateAITags = async (hobbiesText: string) => {
    if (!hobbiesText.trim() || hobbiesText.length < 5) return

    setIsGeneratingTags(true)
    try {
      // 模拟AI处理延迟
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // 模拟AI提取的标签
      const mockTags = []
      if (hobbiesText.includes("摄影") || hobbiesText.includes("拍照")) mockTags.push("摄影")
      if (hobbiesText.includes("旅行") || hobbiesText.includes("旅游")) mockTags.push("旅行")
      if (hobbiesText.includes("电影") || hobbiesText.includes("看电影")) mockTags.push("影视")
      if (hobbiesText.includes("运动") || hobbiesText.includes("健身")) mockTags.push("运动健身")
      if (hobbiesText.includes("音乐") || hobbiesText.includes("唱歌")) mockTags.push("音乐")
      if (hobbiesText.includes("读书") || hobbiesText.includes("阅读")) mockTags.push("阅读")
      if (hobbiesText.includes("美食") || hobbiesText.includes("吃")) mockTags.push("美食")
      if (hobbiesText.includes("游戏")) mockTags.push("游戏")
      if (hobbiesText.includes("艺术") || hobbiesText.includes("绘画")) mockTags.push("艺术")
      if (hobbiesText.includes("咖啡")) mockTags.push("咖啡")

      // 如果没有匹配到，给一些通用标签
      if (mockTags.length === 0) {
        mockTags.push("生活", "社交", "娱乐")
      }

      setAiGeneratedTags(mockTags)
    } catch (error) {
      console.error('AI标签生成失败:', error)
      setErrors((prev: FormErrors) => ({ ...prev, general: 'AI标签生成失败，请稍后重试' }))
    } finally {
      setIsGeneratingTags(false)
    }
  }

  const handleHobbiesChange = (value: string) => {
    setFormData({ ...formData, hobbies: value })
    // 清除相关错误
    if (errors.hobbies) {
      setErrors((prev: FormErrors) => ({ ...prev, hobbies: undefined }))
    }
    if (value.length >= 5) {
      generateAITags(value)
    }
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value })
    // 清除对应字段的错误
    if (errors[field as keyof FormErrors]) {
      setErrors((prev: FormErrors) => ({ ...prev, [field]: undefined }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setErrors({})

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api'
      
      if (isLogin) {
        // 真实登录API调用
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            phone: formData.phone,
            password: formData.password,
          }),
        })

        const data = await response.json()
        
        if (response.ok && data.status === 'success') {
          onLogin({
            token: data.data.token,
            user: data.data.user,
          })
        } else {
          throw new Error(data.message || '登录失败')
        }
      } else {
        // 真实注册API调用
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            phone: formData.phone,
            password: formData.password,
            nickname: formData.nickname,
            gender: parseInt(formData.gender),
            age: parseInt(formData.age),
            city: formData.city,
            occupation: formData.occupation,
            bio: formData.hobbies,
            emotion_status: formData.emotionStatus || '单身',
            interests: aiGeneratedTags,
          }),
        })

        const data = await response.json()
        
        if (response.ok && data.status === 'success') {
          onLogin({
            token: data.data.token,
            user: data.data.user,
          })
        } else {
          throw new Error(data.message || '注册失败')
        }
      }
    } catch (error) {
      setErrors({ general: error instanceof Error ? error.message : '操作失败，请稍后重试' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>{isLogin ? "登录" : "注册"}</CardTitle>
          <Button variant="ghost" size="icon" onClick={onClose} disabled={isLoading}>
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        <CardContent>
          {errors.general && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{errors.general}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="phone">手机号</Label>
              <Input
                id="phone"
                type="tel"
                placeholder="请输入手机号"
                value={formData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                required
                disabled={isLoading}
                className={errors.phone ? "border-red-500" : ""}
              />
              {errors.phone && <p className="text-red-500 text-sm mt-1">{errors.phone}</p>}
            </div>

            <div>
              <Label htmlFor="password">密码</Label>
              <Input
                id="password"
                type="password"
                placeholder="请输入密码"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                required
                disabled={isLoading}
                className={errors.password ? "border-red-500" : ""}
              />
              {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
            </div>

            {!isLogin && (
              <>
                <div>
                  <Label htmlFor="nickname">昵称</Label>
                  <Input
                    id="nickname"
                    placeholder="请输入昵称"
                    value={formData.nickname}
                    onChange={(e) => handleInputChange('nickname', e.target.value)}
                    required
                    disabled={isLoading}
                    className={errors.nickname ? "border-red-500" : ""}
                  />
                  {errors.nickname && <p className="text-red-500 text-sm mt-1">{errors.nickname}</p>}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="gender">性别</Label>
                    <Select
                      value={formData.gender}
                      onValueChange={(value) => handleInputChange('gender', value)}
                      disabled={isLoading}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="选择性别" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">男</SelectItem>
                        <SelectItem value="1">女</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="age">年龄</Label>
                    <Input
                      id="age"
                      type="number"
                      placeholder="年龄"
                      value={formData.age}
                      onChange={(e) => handleInputChange('age', e.target.value)}
                      required
                      disabled={isLoading}
                      className={errors.age ? "border-red-500" : ""}
                    />
                    {errors.age && <p className="text-red-500 text-sm mt-1">{errors.age}</p>}
                  </div>
                </div>

                <div>
                  <Label htmlFor="city">所在城市</Label>
                  <Input
                    id="city"
                    placeholder="请输入所在城市"
                    value={formData.city}
                    onChange={(e) => handleInputChange('city', e.target.value)}
                    required
                    disabled={isLoading}
                    className={errors.city ? "border-red-500" : ""}
                  />
                  {errors.city && <p className="text-red-500 text-sm mt-1">{errors.city}</p>}
                </div>

                <div>
                  <Label htmlFor="occupation">职业</Label>
                  <Input
                    id="occupation"
                    placeholder="请输入职业"
                    value={formData.occupation}
                    onChange={(e) => handleInputChange('occupation', e.target.value)}
                    required
                    disabled={isLoading}
                    className={errors.occupation ? "border-red-500" : ""}
                  />
                  {errors.occupation && <p className="text-red-500 text-sm mt-1">{errors.occupation}</p>}
                </div>

                <div>
                  <Label htmlFor="hobbies" className="flex items-center space-x-2">
                    <span>兴趣爱好</span>
                    <Sparkles className="h-4 w-4 text-purple-500" />
                    <span className="text-sm text-gray-500">AI将自动生成标签</span>
                  </Label>
                  <Textarea
                    id="hobbies"
                    placeholder="详细描述你的兴趣爱好，比如：喜欢摄影和旅行，平时喜欢听音乐看电影..."
                    value={formData.hobbies}
                    onChange={(e) => handleHobbiesChange(e.target.value)}
                    required
                    disabled={isLoading}
                    className={errors.hobbies ? "border-red-500" : ""}
                    rows={3}
                  />
                  {errors.hobbies && <p className="text-red-500 text-sm mt-1">{errors.hobbies}</p>}

                  {isGeneratingTags && (
                    <div className="flex items-center space-x-2 mt-2 text-sm text-purple-600">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>AI正在生成兴趣标签...</span>
                    </div>
                  )}

                  {aiGeneratedTags.length > 0 && (
                    <div className="mt-2">
                      <p className="text-sm text-gray-600 mb-2">AI生成的兴趣标签：</p>
                      <div className="flex flex-wrap gap-1">
                        {aiGeneratedTags.map((tag, index) => (
                          <Badge key={index} className="bg-purple-100 text-purple-800">
                            <Sparkles className="h-3 w-3 mr-1" />
                            {tag}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div>
                  <Label htmlFor="emotionStatus">情感状态</Label>
                  <Select
                    value={formData.emotionStatus}
                    onValueChange={(value) => handleInputChange('emotionStatus', value)}
                    disabled={isLoading}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="选择情感状态" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="single">单身</SelectItem>
                      <SelectItem value="dating">恋爱中</SelectItem>
                      <SelectItem value="complicated">复杂</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="photo">头像照片</Label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-purple-500 transition-colors">
                    <Upload className="h-8 w-8 mx-auto text-gray-400 mb-2" />
                    <p className="text-sm text-gray-600">点击上传照片或拖拽到此处</p>
                    <p className="text-xs text-gray-500 mt-1">支持 JPG、PNG 格式，不超过 5MB</p>
                  </div>
                </div>
              </>
            )}

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  {isLogin ? "登录中..." : "注册中..."}
                </>
              ) : (
                isLogin ? "登录" : "注册"
              )}
            </Button>

            <div className="text-center">
              <Button
                type="button"
                variant="link"
                onClick={() => {
                  setIsLogin(!isLogin)
                  setErrors({})
                  setFormData({
                    phone: "",
                    password: "",
                    nickname: "",
                    gender: "",
                    age: "",
                    city: "",
                    occupation: "",
                    hobbies: "",
                    emotionStatus: "",
                    photo: null,
                  })
                  setAiGeneratedTags([])
                }}
                disabled={isLoading}
              >
                {isLogin ? "没有账号？立即注册" : "已有账号？立即登录"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
