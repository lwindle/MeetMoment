"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Search, Users, MessageCircle, Sparkles } from "lucide-react"

export default function SocialCircles() {
  const [searchQuery, setSearchQuery] = useState("")
  const [activeTab, setActiveTab] = useState("discover")

  // 模拟圈子数据
  const circles = [
    {
      id: 1,
      name: "摄影爱好者",
      description: "分享摄影作品，交流拍摄技巧",
      category: "兴趣",
      memberCount: 1248,
      postCount: 3567,
      cover: "/placeholder.svg?height=200&width=300",
      isJoined: false,
      tags: ["摄影", "艺术", "创作"],
      recentPosts: [
        {
          id: 1,
          author: "小明",
          avatar: "/placeholder.svg?height=40&width=40",
          content: "今天在公园拍到的夕阳，分享给大家！",
          image: "/placeholder.svg?height=200&width=300",
          likes: 23,
          comments: 8,
          timestamp: "2小时前",
        },
      ],
    },
    {
      id: 2,
      name: "北京朝阳区",
      description: "朝阳区的朋友们一起聊天交友",
      category: "地域",
      memberCount: 892,
      postCount: 2134,
      cover: "/placeholder.svg?height=200&width=300",
      isJoined: true,
      tags: ["北京", "朝阳区", "同城"],
      recentPosts: [
        {
          id: 2,
          author: "小雨",
          avatar: "/placeholder.svg?height=40&width=40",
          content: "周末有人想一起去三里屯逛街吗？",
          likes: 15,
          comments: 12,
          timestamp: "1小时前",
        },
      ],
    },
    {
      id: 3,
      name: "音乐分享",
      description: "分享好听的音乐，讨论音乐话题",
      category: "兴趣",
      memberCount: 2156,
      postCount: 5432,
      cover: "/placeholder.svg?height=200&width=300",
      isJoined: false,
      tags: ["音乐", "分享", "讨论"],
      recentPosts: [
        {
          id: 3,
          author: "AI音乐助手",
          avatar: "/placeholder.svg?height=40&width=40",
          content: "根据大家的喜好，推荐几首最近很火的歌曲 🎵",
          likes: 45,
          comments: 23,
          timestamp: "30分钟前",
          isAI: true,
        },
      ],
    },
  ]

  // 模拟推荐圈子
  const recommendedCircles = [
    {
      id: 4,
      name: "健身打卡",
      reason: "基于你的运动兴趣推荐",
      memberCount: 567,
      cover: "/placeholder.svg?height=150&width=200",
    },
    {
      id: 5,
      name: "美食探店",
      reason: "你可能感兴趣的话题",
      memberCount: 834,
      cover: "/placeholder.svg?height=150&width=200",
    },
  ]

  const handleJoinCircle = (circleId: number) => {
    // 模拟加入圈子
    console.log("加入圈子:", circleId)
  }

  const renderCircleCard = (circle: any) => (
    <Card key={circle.id} className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="relative">
        <img src={circle.cover || "/placeholder.svg"} alt={circle.name} className="w-full h-48 object-cover" />
        <div className="absolute top-2 right-2">
          <Badge variant="secondary">{circle.category}</Badge>
        </div>
      </div>
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-lg font-semibold">{circle.name}</h3>
          {circle.isJoined && <Badge className="bg-green-100 text-green-800">已加入</Badge>}
        </div>
        <p className="text-gray-600 text-sm mb-3">{circle.description}</p>

        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
          <div className="flex items-center">
            <Users className="h-4 w-4 mr-1" />
            {circle.memberCount} 成员
          </div>
          <div className="flex items-center">
            <MessageCircle className="h-4 w-4 mr-1" />
            {circle.postCount} 动态
          </div>
        </div>

        <div className="flex flex-wrap gap-1 mb-3">
          {circle.tags.map((tag: string, index: number) => (
            <Badge key={index} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        {circle.recentPosts && circle.recentPosts.length > 0 && (
          <div className="border-t pt-3 mb-3">
            <div className="text-xs text-gray-500 mb-2">最新动态</div>
            {circle.recentPosts.map((post: any) => (
              <div key={post.id} className="flex items-start space-x-2">
                <Avatar className="w-6 h-6">
                  <AvatarImage src={post.avatar || "/placeholder.svg"} />
                  <AvatarFallback>{post.author[0]}</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-1">
                    <span className="text-xs font-medium">{post.author}</span>
                    {post.isAI && <Sparkles className="h-3 w-3 text-purple-500" />}
                    <span className="text-xs text-gray-500">{post.timestamp}</span>
                  </div>
                  <p className="text-xs text-gray-700 truncate">{post.content}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        <Button
          className="w-full"
          variant={circle.isJoined ? "outline" : "default"}
          onClick={() => handleJoinCircle(circle.id)}
        >
          {circle.isJoined ? "进入圈子" : "加入圈子"}
        </Button>
      </CardContent>
    </Card>
  )

  return (
    <div className="max-w-7xl mx-auto p-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">社交圈子</h1>
        <p className="text-gray-600">发现有趣的圈子，遇见志同道合的朋友</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <TabsList>
            <TabsTrigger value="discover">发现圈子</TabsTrigger>
            <TabsTrigger value="joined">我的圈子</TabsTrigger>
            <TabsTrigger value="recommended">推荐</TabsTrigger>
          </TabsList>

          <div className="flex items-center space-x-2 w-full sm:w-auto">
            <div className="relative flex-1 sm:w-64">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="搜索圈子..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button variant="outline">筛选</Button>
          </div>
        </div>

        <TabsContent value="discover" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{circles.map(renderCircleCard)}</div>
        </TabsContent>

        <TabsContent value="joined" className="space-y-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {circles.filter((circle) => circle.isJoined).map(renderCircleCard)}
          </div>
          {circles.filter((circle) => circle.isJoined).length === 0 && (
            <div className="text-center py-12">
              <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">还没有加入任何圈子</h3>
              <p className="text-gray-500 mb-4">去发现页面找找感兴趣的圈子吧</p>
              <Button onClick={() => setActiveTab("discover")}>去发现圈子</Button>
            </div>
          )}
        </TabsContent>

        <TabsContent value="recommended" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-yellow-500" />
                <span>AI智能推荐</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                {recommendedCircles.map((circle) => (
                  <div key={circle.id} className="flex items-center space-x-4 p-4 border rounded-lg">
                    <img
                      src={circle.cover || "/placeholder.svg"}
                      alt={circle.name}
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <h4 className="font-medium">{circle.name}</h4>
                      <p className="text-sm text-gray-500 mb-1">{circle.reason}</p>
                      <div className="flex items-center text-xs text-gray-400">
                        <Users className="h-3 w-3 mr-1" />
                        {circle.memberCount} 成员
                      </div>
                    </div>
                    <Button size="sm" onClick={() => handleJoinCircle(circle.id)}>
                      加入
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{circles.slice(0, 3).map(renderCircleCard)}</div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
