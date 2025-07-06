"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Send, Smile, ImageIcon, Sparkles, Settings, Bot, Heart, Zap, Brain, Star, User } from "lucide-react"

interface Message {
  id: number
  content: string
  sender: "user" | "ai"
  timestamp: Date
  isAI: boolean
  persona?: string
}

interface AIUser {
  id: number
  nickname: string
  age: number
  city: string
  occupation: string
  bio: string
  avatar: string
  interests: string[]
  ai_score: number
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [currentAIUser, setCurrentAIUser] = useState<AIUser | null>(null)
  const [aiUsers, setAIUsers] = useState<AIUser[]>([])
  const [showUserSelector, setShowUserSelector] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingUsers, setIsLoadingUsers] = useState(true)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // 检查登录状态
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const userData = localStorage.getItem('user_data')
    setIsLoggedIn(!!(token && userData))
  }, [])

  // 获取AI用户列表
  useEffect(() => {
    fetchAIUsers()
  }, [])

  const fetchAIUsers = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api'
      const response = await fetch(`${apiUrl}/ai/users`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setAIUsers(data.data)
          // 默认选择第一个AI用户
          if (data.data.length > 0) {
            setCurrentAIUser(data.data[0])
          }
        }
      } else {
        console.error('获取AI用户失败')
        // 使用备用数据
        setCurrentAIUser({
          id: 1,
          nickname: "AI助手",
          age: 25,
          city: "北京",
          occupation: "AI助手",
          bio: "我是你的AI聊天伙伴，随时准备和你聊天",
          avatar: "/placeholder-user.jpg",
          interests: ["聊天", "帮助"],
          ai_score: 95
        })
      }
    } catch (error) {
      console.error('获取AI用户失败:', error)
      // 使用备用数据
      setCurrentAIUser({
        id: 1,
        nickname: "AI助手",
        age: 25,
        city: "北京",
        occupation: "AI助手",
        bio: "我是你的AI聊天伙伴，随时准备和你聊天",
        avatar: "/placeholder-user.jpg",
        interests: ["聊天", "帮助"],
        ai_score: 95
      })
    } finally {
      setIsLoadingUsers(false)
    }
  }

  // 调用AI对话API
  const callAIConversation = async (message: string, aiUserId: number) => {
    try {
      const token = localStorage.getItem('auth_token')
      const userData = localStorage.getItem('user_data')
      
      if (!token || !userData) {
        throw new Error('请先登录后再开始聊天')
      }

      const user = JSON.parse(userData)

      // 使用完整的后端API URL
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api'
      const response = await fetch(`${apiUrl}/ai/conversation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: message,
          persona: currentAIUser?.nickname || "AI助手",
          user_id: user.id, // 从用户数据中获取真实的用户ID
          ai_user_id: aiUserId,
          context: {
            conversation_type: "ai_chat",
            ai_user_name: currentAIUser?.nickname,
            ai_user_occupation: currentAIUser?.occupation,
            ai_user_bio: currentAIUser?.bio
          }
        })
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('API错误响应:', errorText)
        
        if (response.status === 401) {
          throw new Error('登录已过期，请重新登录')
        }
        
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('AI API响应:', data)
      
      if (data.status === 'success') {
        return data.data.content
      } else {
        throw new Error(data.message || 'AI回复失败')
      }
    } catch (error: any) {
      console.error('AI对话API调用失败:', error)
      
      // 如果是登录相关错误，更新登录状态
      if (error.message && (error.message.includes('登录') || error.message.includes('token'))) {
        setIsLoggedIn(false)
        return `${error.message}。请刷新页面重新登录后再试。`
      }
      
      // 返回备用回复
      return "抱歉，我现在有点忙，稍后再聊好吗？😊"
    }
  }

  // 处理发送消息
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading || !currentAIUser) return

    const userMessage: Message = {
      id: Date.now(),
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
      isAI: false
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage("")
    setIsTyping(true)
    setIsLoading(true)

    try {
      // 调用AI API获取回复
      const aiResponse = await callAIConversation(inputMessage, currentAIUser.id)
      
      // 模拟一些延迟让对话更自然
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000))

      const aiMessage: Message = {
        id: Date.now() + 1,
        content: aiResponse,
        sender: "ai",
        timestamp: new Date(),
        isAI: true,
        persona: currentAIUser.nickname
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('发送消息失败:', error)
      // 添加错误消息
      const errorMessage: Message = {
        id: Date.now() + 1,
        content: "抱歉，消息发送失败了，请稍后重试。",
        sender: "ai",
        timestamp: new Date(),
        isAI: true,
        persona: currentAIUser.nickname
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
      setIsLoading(false)
    }
  }

  // 切换AI用户
  const handleAIUserChange = (aiUser: AIUser) => {
    setCurrentAIUser(aiUser)
    setShowUserSelector(false)
    
    // 添加切换提示消息
    const switchMessage: Message = {
      id: Date.now(),
      content: `你好！我是${aiUser.nickname}，${aiUser.age}岁，来自${aiUser.city}。${aiUser.bio}`,
      sender: "ai",
      timestamp: new Date(),
      isAI: true,
      persona: aiUser.nickname
    }
    setMessages(prev => [...prev, switchMessage])
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  // 如果未登录，显示登录提示
  if (!isLoggedIn) {
    return (
      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex items-center justify-center">
        <Card className="p-8 text-center">
          <Bot className="h-16 w-16 mx-auto text-purple-500 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">需要登录才能开始聊天</h3>
          <p className="text-gray-500 mb-6">
            请先登录您的账号，然后就可以和AI聊天伙伴愉快交流了！
          </p>
          <Button 
            onClick={() => window.location.reload()}
            className="bg-gradient-to-r from-pink-500 to-purple-600"
          >
            返回登录
          </Button>
        </Card>
      </div>
    )
  }

  if (isLoadingUsers) {
    return (
      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">正在加载AI聊天伙伴...</p>
        </div>
      </div>
    )
  }

  if (!currentAIUser) {
    return (
      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500">暂无可用的AI聊天伙伴</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)]">
      <Card className="h-full flex flex-col">
        <CardHeader className="border-b">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Avatar className="w-24 h-24">
                  <AvatarImage src={currentAIUser.avatar} alt={currentAIUser.nickname} />
                  <AvatarFallback className="bg-gradient-to-br from-pink-100 to-purple-100">
                    <Bot className="h-12 w-12 text-purple-600" />
                  </AvatarFallback>
                </Avatar>
                {/* 在线状态指示器 */}
                <div className="absolute -top-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <CardTitle className="text-xl">{currentAIUser.nickname}</CardTitle>
                  <Badge variant="secondary" className="bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800">
                    <Sparkles className="h-3 w-3 mr-1" />
                    AI
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    评分 {currentAIUser.ai_score}
                  </Badge>
                </div>
                
                <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                  <span>{currentAIUser.age}岁</span>
                  <span>•</span>
                  <span>{currentAIUser.city}</span>
                  <span>•</span>
                  <span>{currentAIUser.occupation}</span>
                </div>
                
                <p className="text-sm text-gray-700 mb-2">{currentAIUser.bio}</p>
                
                <div className="flex flex-wrap gap-1">
                  {currentAIUser.interests.map((interest, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {interest}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowUserSelector(!showUserSelector)}
                className="flex items-center space-x-2"
              >
                <Settings className="h-4 w-4" />
                <span>切换伙伴</span>
              </Button>
            </div>
          </div>
          
          {/* AI用户选择器 */}
          {showUserSelector && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-medium mb-3">选择AI聊天伙伴</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-60 overflow-y-auto">
                {aiUsers.map((aiUser) => (
                  <Button
                    key={aiUser.id}
                    variant={currentAIUser.id === aiUser.id ? "default" : "outline"}
                    onClick={() => handleAIUserChange(aiUser)}
                    className="flex items-start space-x-3 h-auto p-4 text-left"
                  >
                    <Avatar className="w-14 h-14 flex-shrink-0">
                      <AvatarImage src={aiUser.avatar} alt={aiUser.nickname} />
                      <AvatarFallback className="bg-gradient-to-br from-pink-100 to-purple-100">
                        <Bot className="h-7 w-7 text-purple-600" />
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <div className="font-medium text-sm">{aiUser.nickname}</div>
                        <Badge variant="outline" className="text-xs">
                          {aiUser.ai_score}分
                        </Badge>
                      </div>
                      <div className="text-xs text-gray-600 mb-1">
                        {aiUser.age}岁 • {aiUser.city} • {aiUser.occupation}
                      </div>
                      <div className="text-xs text-gray-500 line-clamp-2">{aiUser.bio}</div>
                    </div>
                  </Button>
                ))}
              </div>
            </div>
          )}
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-8">
              <Avatar className="w-24 h-24 mx-auto mb-4">
                <AvatarImage src={currentAIUser.avatar} alt={currentAIUser.nickname} />
                <AvatarFallback className="bg-gradient-to-br from-pink-100 to-purple-100">
                  <Bot className="h-12 w-12 text-purple-600" />
                </AvatarFallback>
              </Avatar>
              <h3 className="text-lg font-medium text-gray-900 mb-2">开始聊天吧！</h3>
              <p className="text-gray-500 mb-2">
                我是{currentAIUser.nickname}，{currentAIUser.age}岁，来自{currentAIUser.city}
              </p>
              <p className="text-gray-500 text-sm">
                {currentAIUser.bio}
              </p>
            </div>
          )}
          
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`flex items-end space-x-2 max-w-[70%] ${
                  message.sender === "user" ? "flex-row-reverse space-x-reverse" : ""
                }`}
              >
                {message.sender === "ai" && (
                  <Avatar className="w-16 h-16 flex-shrink-0">
                    <AvatarImage src={currentAIUser.avatar} alt={currentAIUser.nickname} />
                    <AvatarFallback className="bg-gradient-to-br from-pink-100 to-purple-100">
                      <Bot className="h-8 w-8 text-purple-600" />
                    </AvatarFallback>
                  </Avatar>
                )}

                <div
                  className={`rounded-lg px-4 py-2 ${
                    message.sender === "user"
                      ? "bg-gradient-to-r from-pink-500 to-purple-600 text-white"
                      : "bg-gradient-to-r from-purple-100 to-pink-100 text-purple-900 border border-purple-200"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className={`text-xs ${message.sender === "user" ? "text-white/70" : "text-purple-600"}`}>
                      {formatTime(message.timestamp)}
                    </p>
                    {message.sender === "ai" && (
                      <div className="flex items-center space-x-1">
                        <Sparkles className="h-3 w-3 text-purple-500" />
                        <span className="text-xs text-purple-600">
                          {message.persona}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="flex items-end space-x-2">
                <Avatar className="w-16 h-16">
                  <AvatarImage src={currentAIUser.avatar} alt={currentAIUser.nickname} />
                  <AvatarFallback className="bg-gradient-to-br from-pink-100 to-purple-100">
                    <Bot className="h-8 w-8 text-purple-600" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-gradient-to-r from-purple-100 to-pink-100 rounded-lg px-4 py-2 border border-purple-200">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4">
          <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
            <Button type="button" variant="outline" size="icon" disabled={isLoading}>
              <Smile className="h-4 w-4" />
            </Button>
            <Button type="button" variant="outline" size="icon" disabled={isLoading}>
              <ImageIcon className="h-4 w-4" />
            </Button>
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={`和${currentAIUser.nickname}聊天...`}
              className="flex-1"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              className="bg-gradient-to-r from-pink-500 to-purple-600"
              disabled={isLoading || !inputMessage.trim()}
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>

          <div className="mt-2 text-xs text-gray-500 text-center">
            <div className="flex items-center justify-center space-x-2">
              <Sparkles className="h-3 w-3" />
              <span>正在与{currentAIUser.nickname}聊天</span>
              <span>•</span>
              <span>基于阿里云通义千问AI</span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}
