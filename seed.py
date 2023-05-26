"""Seed file to make sample data for blogly db"""

from models import db, User, Post, PostTag, Tag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
PostTag.query.delete()
Tag.query.delete()

# ******* USERS **************

# Add users
tess = User(first_name='Tess', last_name='Servopoulos', image_url='https://news-cdn.softpedia.com/images/news2/The-Last-of-Us-Introduces-Tess-Joel-s-Partner-2.jpg')
joel = User(first_name='Joel', last_name='Miller', image_url='https://wallpapercave.com/wp/wp6849598.jpg')
ellie = User(first_name='Ellie', last_name='Williams', image_url='https://img5.goodfon.com/wallpaper/nbig/c/13/the-last-of-us-part-ii-ellie-games-ps4-naughty-dog.jpg')

# Add new users to session
db.session.add_all([tess, joel, ellie])
db.session.commit()

# ******* POSTS **************

# Add posts
feelings = Post(title='Not Sure', content="I'm not sure if I can act on these feelings.", user_id=tess.id)
navigation = Post(title='Navigation', content='I will teach you how to navigate the wilderness if you get lost.', user_id=joel.id)
my_girl = Post(title='My Girl', content='She reminds me of her so much.', user_id=joel.id)
trust = Post(title='Trust No One', content='Keep it a secret and you will live.', user_id=ellie.id)

# Add new posts to session
db.session.add_all([feelings, navigation, my_girl, trust])
db.session.commit()


# ******* TAGS **************

# Add tags
t1 = Tag(name='love', posts=[feelings])
t2 = Tag(name='survive', posts=[trust])

# Add new tags to session
db.session.add_all([t1, t2])
db.session.commit()
