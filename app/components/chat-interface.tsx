"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Send, Smile, ImageIcon, Sparkles } from "lucide-react"

interface Message {
  id: number
  content: string
  sender: "user" | "other"
  timestamp: Date
  isAI?: boolean
  senderName?: string
  senderAvatar?: string
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      content: "你好！很高兴认识你 😊",
      sender: "other",
      timestamp: new Date(Date.now() - 300000),
      isAI: false,
      senderName: "小雨",
      senderAvatar: "/placeholder.svg?height=40&width=40",
    },
  ])
  const [inputMessage, setInputMessage] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [currentChatPartner, setCurrentChatPartner] = useState({
    name: "小雨",
    avatar: "/placeholder.svg?height=40&width=40",
    isOnline: true,
    isAI: false,
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // 模拟AI与真人切换的聊天伙伴
  const chatPartners = [
    {
      name: "小雨",
      avatar: "/placeholder.svg?height=40&width=40",
      isOnline: true,
      isAI: false,
      responses: ["哈哈，你说得对！", "我也是这么想的", "有意思，继续聊聊？", "你的想法很有趣"],
    },
    {
      name: "AI小助手",
      avatar: "/placeholder.svg?height=40&width=40",
      isOnline: true,
      isAI: true,
      responses: [
        "我理解你的感受，想聊聊这个话题吗？",
        "这确实是个有趣的观点！你是怎么想到的？",
        "听起来你今天心情不错呢 😊",
        "我很好奇你对这件事的看法，能详细说说吗？",
      ],
    },
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // 模拟智能切换逻辑
  const getResponsePartner = () => {
    // 模拟切换策略：随机选择AI或真人回复
    const shouldUseAI = Math.random() > 0.6 // 40% 概率使用AI
    return shouldUseAI ? chatPartners[1] : chatPartners[0]
  }

  const simulateResponse = async (userMessage: string) => {
    setIsTyping(true)

    // 模拟响应延迟
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 2000))

    const partner = getResponsePartner()
    const responses = partner.responses
    const randomResponse = responses[Math.floor(Math.random() * responses.length)]

    // 更新当前聊天伙伴（模拟无感知切换）
    setCurrentChatPartner(partner)

    const newMessage: Message = {
      id: Date.now(),
      content: randomResponse,
      sender: "other",
      timestamp: new Date(),
      isAI: partner.isAI,
      senderName: partner.name,
      senderAvatar: partner.avatar,
    }

    setMessages((prev) => [...prev, newMessage])
    setIsTyping(false)
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputMessage.trim()) return

    const userMessage: Message = {
      id: Date.now(),
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputMessage("")

    // 模拟对方回复
    await simulateResponse(inputMessage)
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)]">
      <Card className="h-full flex flex-col">
        <CardHeader className="border-b">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Avatar>
                <AvatarImage src={currentChatPartner.avatar || "/placeholder.svg"} />
                <AvatarFallback>{currentChatPartner.name[0]}</AvatarFallback>
              </Avatar>
              <div>
                <CardTitle className="flex items-center space-x-2">
                  <span>{currentChatPartner.name}</span>
                  {currentChatPartner.isAI && (
                    <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                      <Sparkles className="h-3 w-3 mr-1" />
                      AI
                    </Badge>
                  )}
                </CardTitle>
                <p className="text-sm text-gray-500">{currentChatPartner.isOnline ? "在线" : "离线"}</p>
              </div>
            </div>
            <div className="text-xs text-gray-400">智能匹配中...</div>
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`flex items-end space-x-2 max-w-[70%] ${
                  message.sender === "user" ? "flex-row-reverse space-x-reverse" : ""
                }`}
              >
                {message.sender === "other" && (
                  <Avatar className="w-8 h-8">
                    <AvatarImage src={message.senderAvatar || "/placeholder.svg"} />
                    <AvatarFallback>{message.senderName?.[0]}</AvatarFallback>
                  </Avatar>
                )}

                <div
                  className={`rounded-lg px-4 py-2 ${
                    message.sender === "user"
                      ? "bg-gradient-to-r from-pink-500 to-purple-600 text-white"
                      : message.isAI
                        ? "bg-purple-100 text-purple-900 border border-purple-200"
                        : "bg-gray-100 text-gray-900"
                  }`}
                >
                  <p>{message.content}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className={`text-xs ${message.sender === "user" ? "text-white/70" : "text-gray-500"}`}>
                      {formatTime(message.timestamp)}
                    </p>
                    {message.sender === "other" && message.isAI && (
                      <Sparkles className="h-3 w-3 text-purple-500 ml-2" />
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="flex items-end space-x-2">
                <Avatar className="w-8 h-8">
                  <AvatarImage src={currentChatPartner.avatar || "/placeholder.svg"} />
                  <AvatarFallback>{currentChatPartner.name[0]}</AvatarFallback>
                </Avatar>
                <div className="bg-gray-100 rounded-lg px-4 py-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
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
            <Button type="button" variant="outline" size="icon">
              <Smile className="h-4 w-4" />
            </Button>
            <Button type="button" variant="outline" size="icon">
              <ImageIcon className="h-4 w-4" />
            </Button>
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="输入消息..."
              className="flex-1"
            />
            <Button type="submit" className="bg-gradient-to-r from-pink-500 to-purple-600">
              <Send className="h-4 w-4" />
            </Button>
          </form>

          <div className="mt-2 text-xs text-gray-500 text-center">
            <Sparkles className="h-3 w-3 inline mr-1" />
            AI正在智能为你匹配最合适的聊天伙伴
          </div>
        </div>
      </Card>
    </div>
  )
}
