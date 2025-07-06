"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Input } from "@/components/ui/input"
import { Heart, MessageCircle, Users, Sparkles, MapPin, Search, Filter, ChevronDown } from "lucide-react"
import AuthModal from "./components/auth-modal"
import ChatInterface from "./components/chat-interface"
import ProfilePage from "./components/profile-page"
import SocialCircles from "./components/social-circles"

// API 基础URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api'

// 类型定义
interface User {
  id: number
  name: string
  nickname?: string
  age: number
  city: string
  occupation: string
  hobbies: string[]
  avatar: string
  photos: string[]
  isOnline: boolean
  aiScore: number
  bio?: string
  verified?: boolean
  gender?: number
  isAI?: boolean
}

interface AuthData {
  token: string
  user: any
}

export default function HomePage() {
  const [currentPage, setCurrentPage] = useState("home")
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [recommendedUsers, setRecommendedUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [currentPageNum, setCurrentPageNum] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const [totalUsers, setTotalUsers] = useState(0)
  const [selectedCity, setSelectedCity] = useState("")
  const [selectedAge, setSelectedAge] = useState("")
  
  const USERS_PER_PAGE = 20

  // 获取推荐用户数据
  const fetchRecommendedUsers = async (page = 1, append = false) => {
    setLoading(true)
    try {
      // 暂时直接从Supabase获取用户数据来测试显示
      const SUPABASE_URL = 'https://odnalktszcfoxpcvmshw.supabase.co'
      const SUPABASE_SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9kbmFsa3RzemNmb3hwY3Ztc2h3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTE5MDczMSwiZXhwIjoyMDY2NzY2NzMxfQ.sa4_2LydNNhr2QckFKiqHOrXMBkKCaoHL_mYkR76aw8'
      
      const offset = (page - 1) * USERS_PER_PAGE
      const response = await fetch(`${SUPABASE_URL}/rest/v1/users?gender=eq.2&limit=${USERS_PER_PAGE}&offset=${offset}&select=id,nickname,age,city,occupation,bio,avatar,verified,is_online,ai_score&order=created_at.desc`, {
        headers: {
          'apikey': SUPABASE_SERVICE_ROLE_KEY,
          'Authorization': `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`,
          'Content-Type': 'application/json',
          'Prefer': 'count=exact'
        }
      })
      
      if (response.ok) {
        const users = await response.json()
        const contentRange = response.headers.get('content-range')
        const total = contentRange ? parseInt(contentRange.split('/')[1]) : users.length
        setTotalUsers(total)
        
        // 获取用户兴趣
        const usersWithInterests = await Promise.all(users.map(async (user: any) => {
          try {
            const interestsResponse = await fetch(`${SUPABASE_URL}/rest/v1/user_interests?user_id=eq.${user.id}&select=tag`, {
              headers: {
                'apikey': SUPABASE_SERVICE_ROLE_KEY,
                'Authorization': `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`,
                'Content-Type': 'application/json'
              }
            })
            
            const interests = interestsResponse.ok ? await interestsResponse.json() : []
            
            return {
              id: user.id,
              name: user.nickname,
              age: user.age,
              city: user.city,
              occupation: user.occupation,
              hobbies: interests.map((interest: any) => interest.tag),
              avatar: user.avatar || "/placeholder.svg?height=200&width=200",
              photos: [user.avatar || "/placeholder.svg?height=300&width=300"],
              isOnline: user.is_online,
              aiScore: user.ai_score,
              bio: user.bio,
              verified: user.verified,
              gender: 2
            }
          } catch (error) {
            console.error('Error fetching interests for user', user.id, error)
            return {
              id: user.id,
              name: user.nickname,
              age: user.age,
              city: user.city,
              occupation: user.occupation,
              hobbies: [],
              avatar: user.avatar || "/placeholder.svg?height=200&width=200",
              photos: [user.avatar || "/placeholder.svg?height=300&width=300"],
              isOnline: user.is_online,
              aiScore: user.ai_score,
              bio: user.bio,
              verified: user.verified,
              gender: 2
            }
          }
        }))
        
        if (append) {
          setRecommendedUsers(prev => [...prev, ...usersWithInterests])
        } else {
          setRecommendedUsers(usersWithInterests)
        }
        
        setHasMore(users.length === USERS_PER_PAGE && offset + USERS_PER_PAGE < total)
      } else {
        console.error('Failed to fetch users:', response.status)
        if (!append) {
          setRecommendedUsers(getDefaultUsers())
        }
      }
    } catch (error) {
      console.error('Error fetching users:', error)
      if (!append) {
        setRecommendedUsers(getDefaultUsers())
      }
    } finally {
      setLoading(false)
    }
  }

  // 加载更多用户
  const loadMoreUsers = () => {
    if (!loading && hasMore) {
      const nextPage = currentPageNum + 1
      setCurrentPageNum(nextPage)
      fetchRecommendedUsers(nextPage, true)
    }
  }

  // 搜索和过滤用户
  const filterUsers = () => {
    let filtered = recommendedUsers

    if (searchTerm) {
      filtered = filtered.filter(user => 
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.occupation.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.hobbies.some(hobby => hobby.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    if (selectedCity) {
      filtered = filtered.filter(user => user.city === selectedCity)
    }

    if (selectedAge) {
      const [minAge, maxAge] = selectedAge.split('-').map(Number)
      filtered = filtered.filter(user => user.age >= minAge && user.age <= maxAge)
    }

    setFilteredUsers(filtered)
  }

  // 获取所有城市列表
  const getCities = () => {
    const cities = [...new Set(recommendedUsers.map(user => user.city))]
    return cities.sort()
  }

  // 默认用户数据（作为fallback）
  const getDefaultUsers = () => [
    {
      id: 1,
      name: "小雨",
      age: 26,
      city: "北京",
      occupation: "设计师",
      hobbies: ["摄影", "旅行", "咖啡"],
      avatar: "/placeholder.svg?height=200&width=200",
      photos: ["/placeholder.svg?height=300&width=300"],
      isOnline: true,
      aiScore: 85,
    },
    {
      id: 2,
      name: "阿杰",
      age: 29,
      city: "上海",
      occupation: "产品经理",
      hobbies: ["健身", "电影", "美食"],
      avatar: "/placeholder.svg?height=200&width=200",
      photos: ["/placeholder.svg?height=300&width=300"],
      isOnline: false,
      aiScore: 92,
    },
    {
      id: 3,
      name: "AI小助手",
      age: 25,
      city: "深圳",
      occupation: "智能伙伴",
      hobbies: ["聊天", "陪伴", "倾听"],
      avatar: "/placeholder.svg?height=200&width=200",
      photos: ["/placeholder.svg?height=300&width=300"],
      isOnline: true,
      isAI: true,
      aiScore: 98,
    },
  ]

  // 检查登录状态
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const userData = localStorage.getItem('user_data')
    
    if (token && userData) {
      setIsAuthenticated(true)
      setCurrentUser(JSON.parse(userData))
    }
  }, [])

  // 页面加载时获取推荐用户
  useEffect(() => {
    fetchRecommendedUsers()
  }, [])

  // 搜索和过滤效果
  useEffect(() => {
    filterUsers()
  }, [searchTerm, selectedCity, selectedAge, recommendedUsers])

  const handleLogin = (userData: any) => {
    setIsAuthenticated(true)
    setCurrentUser(userData)
    setShowAuthModal(false)
    
    // 保存登录信息到localStorage
    localStorage.setItem('auth_token', userData.token)
    localStorage.setItem('user_data', JSON.stringify(userData.user))
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setCurrentUser(null)
    setRecommendedUsers([])
    setFilteredUsers([])
    
    // 清除localStorage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  }

  const renderNavigation = () => (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <Heart className="h-8 w-8 text-pink-500" />
            <span className="text-2xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
              AI缘分
            </span>
          </div>

          {isAuthenticated ? (
            <div className="flex items-center space-x-6">
              <Button
                variant={currentPage === "home" ? "default" : "ghost"}
                onClick={() => setCurrentPage("home")}
                className="flex items-center space-x-2"
              >
                <Heart className="h-4 w-4" />
                <span>发现</span>
              </Button>
              <Button
                variant={currentPage === "circles" ? "default" : "ghost"}
                onClick={() => setCurrentPage("circles")}
                className="flex items-center space-x-2"
              >
                <Users className="h-4 w-4" />
                <span>圈子</span>
              </Button>
              <Button
                variant={currentPage === "chat" ? "default" : "ghost"}
                onClick={() => setCurrentPage("chat")}
                className="flex items-center space-x-2"
              >
                <MessageCircle className="h-4 w-4" />
                <span>聊天</span>
              </Button>
              <Button
                variant={currentPage === "profile" ? "default" : "ghost"}
                onClick={() => setCurrentPage("profile")}
              >
                <Avatar className="h-8 w-8">
                  <AvatarImage src={currentUser?.avatar || "/placeholder.svg"} />
                  <AvatarFallback>{currentUser?.nickname?.[0] || currentUser?.name?.[0]}</AvatarFallback>
                </Avatar>
              </Button>
              <Button
                variant="ghost"
                onClick={handleLogout}
                className="text-gray-600 hover:text-gray-800"
              >
                退出
              </Button>
            </div>
          ) : (
            <Button onClick={() => setShowAuthModal(true)} className="bg-gradient-to-r from-pink-500 to-purple-600">
              登录/注册
            </Button>
          )}
        </div>
      </div>
    </nav>
  )

  const renderHomePage = () => (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div>
        {!isAuthenticated && (
          // 未登录首页介绍
          <div className="text-center mb-12">
            <div className="mb-12">
              <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
                AI智能交友，遇见真实的缘分
              </h1>
              <p className="text-xl text-gray-600 mb-8">融合AI陪伴与真人社交，让每一次聊天都充满惊喜</p>
              <div className="flex justify-center space-x-4 mb-12">
                <div className="flex items-center space-x-2 text-gray-600">
                  <Sparkles className="h-5 w-5 text-yellow-500" />
                  <span>AI智能匹配</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <Heart className="h-5 w-5 text-pink-500" />
                  <span>真实社交</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <Users className="h-5 w-5 text-blue-500" />
                  <span>兴趣圈子</span>
                </div>
              </div>
              <Button
                size="lg"
                onClick={() => setShowAuthModal(true)}
                className="bg-gradient-to-r from-pink-500 to-purple-600 text-white px-8 py-3 text-lg"
              >
                立即开始交友之旅
              </Button>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mt-16">
              <Card className="p-6 text-center">
                <Sparkles className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">AI智能陪伴</h3>
                <p className="text-gray-600">24小时在线，理解你的心情，陪你聊天解闷</p>
              </Card>
              <Card className="p-6 text-center">
                <Heart className="h-12 w-12 text-pink-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">真人社交</h3>
                <p className="text-gray-600">遇见真实的人，建立有意义的情感连接</p>
              </Card>
              <Card className="p-6 text-center">
                <Users className="h-12 w-12 text-blue-500 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">兴趣圈子</h3>
                <p className="text-gray-600">加入同好圈子，找到志同道合的朋友</p>
              </Card>
            </div>
          </div>
        )}

        {/* 推荐用户部分 - 始终显示 */}
        <div>
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-3xl font-bold mb-2">为你推荐</h2>
                <p className="text-gray-600">
                  基于你的兴趣和偏好，这些人可能和你很合拍
                  {totalUsers > 0 && (
                    <span className="ml-2 text-sm bg-pink-100 text-pink-600 px-2 py-1 rounded-full">
                      共{totalUsers}人
                    </span>
                  )}
                </p>
              </div>
            </div>

            {/* 搜索和过滤栏 */}
            <div className="bg-white rounded-lg p-4 shadow-sm mb-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="搜索姓名、职业、城市或兴趣..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <div className="flex gap-2">
                  <select
                    value={selectedCity}
                    onChange={(e) => setSelectedCity(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  >
                    <option value="">所有城市</option>
                    {getCities().map(city => (
                      <option key={city} value={city}>{city}</option>
                    ))}
                  </select>
                  <select
                    value={selectedAge}
                    onChange={(e) => setSelectedAge(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
                  >
                    <option value="">所有年龄</option>
                    <option value="18-25">18-25岁</option>
                    <option value="26-30">26-30岁</option>
                    <option value="31-35">31-35岁</option>
                    <option value="36-40">36-40岁</option>
                    <option value="41-50">41-50岁</option>
                  </select>
                </div>
              </div>
              
              {(searchTerm || selectedCity || selectedAge) && (
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-sm text-gray-600">
                    找到 {filteredUsers.length} 个匹配结果
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setSearchTerm("")
                      setSelectedCity("")
                      setSelectedAge("")
                    }}
                  >
                    清除筛选
                  </Button>
                </div>
              )}
            </div>

            {loading && currentPageNum === 1 && (
              <div className="flex items-center justify-center space-x-2 py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-pink-500"></div>
                <span className="text-gray-500">正在加载推荐用户...</span>
              </div>
            )}
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {(filteredUsers.length > 0 ? filteredUsers : recommendedUsers).map((user) => (
              <Card key={user.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                <div className="relative">
                  <img 
                    src={user.avatar || "/placeholder.svg"} 
                    alt={user.name} 
                    className="w-full h-64 object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "/placeholder.svg?height=200&width=200"
                    }}
                  />
                  {user.isAI && (
                    <Badge className="absolute top-2 right-2 bg-gradient-to-r from-purple-500 to-pink-500">
                      <Sparkles className="h-3 w-3 mr-1" />
                      AI伙伴
                    </Badge>
                  )}
                  {user.isOnline && !user.isAI && (
                    <div className="absolute top-2 right-2 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                  )}
                  {user.verified && (
                    <Badge className="absolute top-2 left-2 bg-blue-500">
                      ✓ 已验证
                    </Badge>
                  )}
                </div>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-xl font-semibold">{user.name}</h3>
                    <span className="text-gray-500">{user.age}岁</span>
                  </div>
                  <div className="flex items-center text-gray-600 mb-2">
                    <MapPin className="h-4 w-4 mr-1" />
                    <span>{user.city}</span>
                    <span className="mx-2">•</span>
                    <span>{user.occupation}</span>
                  </div>
                  {user.bio && (
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                      {user.bio}
                    </p>
                  )}
                  <div className="flex flex-wrap gap-1 mb-4">
                    {user.hobbies.slice(0, 3).map((hobby, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {hobby}
                      </Badge>
                    ))}
                    {user.hobbies.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{user.hobbies.length - 3}
                      </Badge>
                    )}
                  </div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-1">
                      <Sparkles className="h-4 w-4 text-yellow-500" />
                      <span className="text-sm text-gray-600">匹配度: {user.aiScore}%</span>
                    </div>
                    {user.gender === 2 && (
                      <span className="text-pink-500 text-sm">♀</span>
                    )}
                    {user.gender === 1 && (
                      <span className="text-blue-500 text-sm">♂</span>
                    )}
                  </div>
                  <div className="flex space-x-2">
                    <Button className="flex-1" onClick={() => setCurrentPage("chat")}>
                      <MessageCircle className="h-4 w-4 mr-2" />
                      聊天
                    </Button>
                    <Button variant="outline" size="icon">
                      <Heart className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* 加载更多按钮 */}
          {hasMore && !loading && recommendedUsers.length > 0 && (
            <div className="text-center mt-8">
              <Button
                onClick={loadMoreUsers}
                variant="outline"
                size="lg"
                className="px-8"
              >
                <ChevronDown className="h-4 w-4 mr-2" />
                加载更多 ({totalUsers - recommendedUsers.length} 人待加载)
              </Button>
            </div>
          )}

          {/* 加载中状态 */}
          {loading && currentPageNum > 1 && (
            <div className="flex items-center justify-center space-x-2 py-8">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-pink-500"></div>
              <span className="text-gray-500">加载更多用户中...</span>
            </div>
          )}

          {/* 空状态 */}
          {recommendedUsers.length === 0 && !loading && (
            <div className="text-center py-12">
              <Heart className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">暂无推荐用户</h3>
              <p className="text-gray-500">请稍后再试，或完善你的个人资料以获得更好的推荐</p>
            </div>
          )}

          {/* 搜索无结果 */}
          {filteredUsers.length === 0 && recommendedUsers.length > 0 && (searchTerm || selectedCity || selectedAge) && (
            <div className="text-center py-12">
              <Search className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">没有找到匹配的用户</h3>
              <p className="text-gray-500">尝试调整搜索条件或清除筛选</p>
              <Button
                variant="outline"
                className="mt-4"
                onClick={() => {
                  setSearchTerm("")
                  setSelectedCity("")
                  setSelectedAge("")
                }}
              >
                清除所有筛选
              </Button>
            </div>
          )}

          {/* 已加载完所有用户 */}
          {!hasMore && recommendedUsers.length > 0 && !loading && (
            <div className="text-center py-8 text-gray-500">
              <p>已显示所有 {totalUsers} 位用户</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      {renderNavigation()}

      {currentPage === "home" && renderHomePage()}
      {currentPage === "chat" && isAuthenticated && <ChatInterface />}
      {currentPage === "profile" && isAuthenticated && <ProfilePage user={currentUser} />}
      {currentPage === "circles" && isAuthenticated && <SocialCircles />}

      {showAuthModal && <AuthModal onClose={() => setShowAuthModal(false)} onLogin={handleLogin} />}
    </div>
  )
}
