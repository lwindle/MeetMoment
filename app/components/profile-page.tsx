"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Textarea } from "@/components/ui/textarea"
import { Edit, Camera, MapPin, Briefcase, Heart, Star, Sparkles, TrendingUp } from "lucide-react"

interface ProfilePageProps {
  user: any
}

export default function ProfilePage({ user }: ProfilePageProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [profileData, setProfileData] = useState({
    nickname: user?.name || "用户昵称",
    age: 26,
    city: "北京",
    occupation: "产品设计师",
    bio: "热爱生活，喜欢摄影和旅行。希望能遇到有趣的灵魂，一起探索世界的美好。",
    hobbies: ["摄影", "旅行", "咖啡", "电影", "音乐"],
    photos: [
      "/placeholder.svg?height=300&width=300",
      "/placeholder.svg?height=300&width=300",
      "/placeholder.svg?height=300&width=300",
    ],
  })

  // AI评分和建议
  const aiAnalysis = {
    score: 85,
    completeness: 90,
    attractiveness: 80,
    suggestions: [
      "添加2-3张生活照可提升匹配率35%",
      "详细描述你的兴趣爱好能吸引更多同频好友",
      "完善职业信息有助于建立专业形象",
    ],
    matchedUsers: [
      {
        name: "小雨",
        avatar: "/placeholder.svg?height=60&width=60",
        matchRate: 92,
        commonInterests: ["摄影", "旅行"],
      },
      {
        name: "阿杰",
        avatar: "/placeholder.svg?height=60&width=60",
        matchRate: 88,
        commonInterests: ["电影", "音乐"],
      },
    ],
    aiCompanion: {
      name: "AI小雅",
      avatar: "/placeholder.svg?height=60&width=60",
      personality: "温柔体贴，善于倾听",
      specialties: ["情感陪伴", "生活建议", "兴趣分享"],
    },
  }

  const handleSave = () => {
    setIsEditing(false)
    // 这里可以调用API保存数据
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      {/* 个人资料卡片 */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>个人资料</CardTitle>
          <Button
            variant={isEditing ? "default" : "outline"}
            onClick={() => (isEditing ? handleSave() : setIsEditing(true))}
          >
            <Edit className="h-4 w-4 mr-2" />
            {isEditing ? "保存" : "编辑"}
          </Button>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex flex-col md:flex-row gap-6">
            {/* 头像和基本信息 */}
            <div className="flex flex-col items-center space-y-4">
              <div className="relative">
                <Avatar className="w-32 h-32">
                  <AvatarImage src={user?.avatar || "/placeholder.svg"} />
                  <AvatarFallback className="text-2xl">{profileData.nickname[0]}</AvatarFallback>
                </Avatar>
                {isEditing && (
                  <Button size="icon" className="absolute -bottom-2 -right-2 rounded-full">
                    <Camera className="h-4 w-4" />
                  </Button>
                )}
              </div>

              {!isEditing ? (
                <div className="text-center">
                  <h2 className="text-2xl font-bold">{profileData.nickname}</h2>
                  <div className="flex items-center justify-center space-x-4 text-gray-600 mt-2">
                    <span>{profileData.age}岁</span>
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-1" />
                      {profileData.city}
                    </div>
                    <div className="flex items-center">
                      <Briefcase className="h-4 w-4 mr-1" />
                      {profileData.occupation}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-3 w-full max-w-xs">
                  <div>
                    <Label>昵称</Label>
                    <Input
                      value={profileData.nickname}
                      onChange={(e) => setProfileData({ ...profileData, nickname: e.target.value })}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label>年龄</Label>
                      <Input
                        type="number"
                        value={profileData.age}
                        onChange={(e) => setProfileData({ ...profileData, age: Number.parseInt(e.target.value) })}
                      />
                    </div>
                    <div>
                      <Label>城市</Label>
                      <Input
                        value={profileData.city}
                        onChange={(e) => setProfileData({ ...profileData, city: e.target.value })}
                      />
                    </div>
                  </div>
                  <div>
                    <Label>职业</Label>
                    <Input
                      value={profileData.occupation}
                      onChange={(e) => setProfileData({ ...profileData, occupation: e.target.value })}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* 详细信息 */}
            <div className="flex-1 space-y-4">
              <div>
                <Label className="text-base font-semibold">个人简介</Label>
                {!isEditing ? (
                  <p className="text-gray-700 mt-2">{profileData.bio}</p>
                ) : (
                  <Textarea
                    value={profileData.bio}
                    onChange={(e) => setProfileData({ ...profileData, bio: e.target.value })}
                    className="mt-2"
                    rows={3}
                  />
                )}
              </div>

              <div>
                <Label className="text-base font-semibold">兴趣爱好</Label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {profileData.hobbies.map((hobby, index) => (
                    <Badge key={index} variant="secondary">
                      {hobby}
                    </Badge>
                  ))}
                  {isEditing && (
                    <Button variant="outline" size="sm">
                      + 添加
                    </Button>
                  )}
                </div>
              </div>

              <div>
                <Label className="text-base font-semibold">照片展示</Label>
                <div className="grid grid-cols-3 gap-3 mt-2">
                  {profileData.photos.map((photo, index) => (
                    <div key={index} className="relative aspect-square">
                      <img
                        src={photo || "/placeholder.svg"}
                        alt={`照片 ${index + 1}`}
                        className="w-full h-full object-cover rounded-lg"
                      />
                      {isEditing && (
                        <Button size="icon" variant="secondary" className="absolute top-1 right-1 h-6 w-6">
                          <Camera className="h-3 w-3" />
                        </Button>
                      )}
                    </div>
                  ))}
                  {isEditing && (
                    <div className="aspect-square border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center">
                      <Button variant="ghost" size="sm">
                        <Camera className="h-4 w-4 mr-2" />
                        添加
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI分析报告 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-yellow-500" />
            <span>AI智能分析</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* 评分 */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">{aiAnalysis.score}</div>
              <div className="text-sm text-blue-700">综合评分</div>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
              <div className="text-3xl font-bold text-green-600">{aiAnalysis.completeness}%</div>
              <div className="text-sm text-green-700">资料完整度</div>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
              <div className="text-3xl font-bold text-purple-600">{aiAnalysis.attractiveness}%</div>
              <div className="text-sm text-purple-700">吸引力指数</div>
            </div>
          </div>

          {/* 优化建议 */}
          <div>
            <h3 className="font-semibold mb-3 flex items-center">
              <TrendingUp className="h-4 w-4 mr-2 text-green-500" />
              优化建议
            </h3>
            <div className="space-y-2">
              {aiAnalysis.suggestions.map((suggestion, index) => (
                <div key={index} className="flex items-start space-x-2 p-3 bg-yellow-50 rounded-lg">
                  <Star className="h-4 w-4 text-yellow-500 mt-0.5" />
                  <span className="text-sm text-yellow-800">{suggestion}</span>
                </div>
              ))}
            </div>
          </div>

          {/* 匹配推荐 */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-3 flex items-center">
                <Heart className="h-4 w-4 mr-2 text-pink-500" />
                可能感兴趣的TA
              </h3>
              <div className="space-y-3">
                {aiAnalysis.matchedUsers.map((match, index) => (
                  <div key={index} className="flex items-center space-x-3 p-3 border rounded-lg">
                    <Avatar>
                      <AvatarImage src={match.avatar || "/placeholder.svg"} />
                      <AvatarFallback>{match.name[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{match.name}</span>
                        <Badge variant="secondary">{match.matchRate}% 匹配</Badge>
                      </div>
                      <div className="text-sm text-gray-500">共同兴趣: {match.commonInterests.join(", ")}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-3 flex items-center">
                <Sparkles className="h-4 w-4 mr-2 text-purple-500" />
                你的专属AI伙伴
              </h3>
              <div className="p-4 border rounded-lg bg-gradient-to-br from-purple-50 to-pink-50">
                <div className="flex items-center space-x-3 mb-3">
                  <Avatar>
                    <AvatarImage src={aiAnalysis.aiCompanion.avatar || "/placeholder.svg"} />
                    <AvatarFallback>{aiAnalysis.aiCompanion.name[0]}</AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="font-medium">{aiAnalysis.aiCompanion.name}</div>
                    <div className="text-sm text-gray-600">{aiAnalysis.aiCompanion.personality}</div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm font-medium">擅长领域:</div>
                  <div className="flex flex-wrap gap-1">
                    {aiAnalysis.aiCompanion.specialties.map((specialty, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {specialty}
                      </Badge>
                    ))}
                  </div>
                </div>
                <Button className="w-full mt-3 bg-gradient-to-r from-purple-500 to-pink-500">开始聊天</Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
