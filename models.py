"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
	db.app = app
	db.init_app(app)

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	image_url = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"< User {self.first_name} {self.last_name} {self.image_url} >"

class Post(db.Model):
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.Text, nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	user = db.relationship('User', backref='posts')
	# hashtags = db.relationship('PostTag', backref='post')

	def __repr__(self):
		return f"< Post {self.title} {self.content} {self.created_at} {self.user_id} >"

class PostTag(db.Model):
	__tablename__ = 'posts_tags'

	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

	def __repr__(self):
		return f"< PostTag {self.post_id} {self.tag_id} >"

class Tag(db.Model):
	__tablename__ = 'tags'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.Text, unique=True, nullable=False)

	posts = db.relationship('Post', secondary='posts_tags', backref='tags')

	def __repr__(self):
		return f"< Tag {self.name} {self.posts} >"

