import peewee as pw
from dbtables import User, Like, Music

def createLike(user_id, post_id, owner_id, artist, title):
	user, _ = User.get_or_create(user_id=user_id)
	music, _ = Music.get_or_create(post_id=post_id, 
		owner_id=owner_id, artist=artist, title=title)
	Like.create(user=user, music=music)
	return
