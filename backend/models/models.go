package models

// This file ensures all models are properly exported and available for import

// Re-export all model types to make them available from a single import
type (
	// User models
	UserModel         = User
	UserPhotoModel    = UserPhoto
	UserInterestModel = UserInterest
	
	// Match models
	MatchModel = Match
	
	// Chat models
	ConversationModel   = Conversation
	MessageModel        = Message
	AIConversationModel = AIConversation
	
	// Circle models
	CircleModel      = Circle
	CircleMemberModel = CircleMember
	CirclePostModel   = CirclePost
	PostCommentModel  = PostComment
	PostLikeModel     = PostLike
) 