"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'flasksqlalchemyexercise'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# **************** USERS ***********************************

@app.route('/')
def redirect_to_list_users():
	"""Redirects to list of all users in db"""

	return redirect('/users')

@app.route('/users')
def list_all_users():
	"""Shows list of all users in db"""

	users = User.query.all()
	return render_template('user_list.html', users=users)

@app.route('/users/new')
def create_new_user():
	"""Shows a form to add a new user"""

	return render_template('create_user.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():
	"""Adds new user to the list of existing users"""

	first_name = request.form['first_name']
	last_name = request.form['last_name']
	img_url = request.form['img_url']

	new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
	db.session.add(new_user)
	db.session.commit()

	return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
	"""Shows details about a specific user"""

	user = User.query.get_or_404(user_id)
	posts = Post.query.filter_by(user_id=user_id)
	return render_template('user_details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
	"""Shows edit form for user"""

	user = User.query.get_or_404(user_id)
	return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
	"""Updates user from edit form to user list"""

	user = User.query.get_or_404(user_id)

	user.first_name = request.form['first_name']
	user.last_name = request.form['last_name']
	user.image_url = request.form['img_url']

	db.session.add(user)
	db.session.commit()	

	return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
	"""Delete user from db"""

	user = User.query.filter_by(id=user_id).delete()
	db.session.commit()

	return redirect('/users')


# **************** POSTS ***********************************

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
	"""Shows form to add a post for that user"""

	user = User.query.get_or_404(user_id)
	tags = Tag.query.all()
	return render_template('create_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
	"""Adds new post to list of posts by existing user"""

	user = User.query.get_or_404(user_id)
	tag_ids = [int(num) for num in request.form.getlist('tags')]
	tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

	title = request.form['title']
	content = request.form['content']

	new_post = Post(title=title, content=content, user=user, tags=tags)

	db.session.add(new_post)
	db.session.commit()

	return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
	"""Shows post created by a user"""

	post = Post.query.get_or_404(post_id)
	return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
	"""Shows form to edit existing post"""

	post = Post.query.get_or_404(post_id)
	tags = Tag.query.all()
	return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
	"""Updates existing post"""

	post = Post.query.get_or_404(post_id)
	tag_ids = [int(num) for num in request.form.getlist('tags')]
	post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

	post.title = request.form['title']
	post.content = request.form['content']
	post.user_id = post.user.id

	db.session.add(post)
	db.session.commit()

	return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
	"""Deletes post from db"""

	# user = User.query.get_or_404(user_id)
	post = Post.query.filter_by(id=post_id).delete()
	db.session.commit()

	return redirect(f'/users')
	# return redirect(f'/users/{user_id}')


# **************** TAGS ***********************************

@app.route('/tags')
def show_all_tags():
	"""Shows all current tags"""

	tags = Tag.query.all()
	return render_template('tag_list.html', tags=tags)


@app.route('/tags/new')
def create_new_tag():
	"""Shows form to create a new tag"""

	return render_template('create_tag.html')


@app.route('/tags/new', methods=['POST'])
def add_new_tag():
	"""Adds new tag to a post"""

	name = request.form['tagname']
	new_tag = Tag(name=name)

	db.session.add(new_tag)
	db.session.commit()

	return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
	"""Shows details of tag"""

	tag = Tag.query.get_or_404(tag_id)
	
	return render_template('tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
	"""Shows form to edit existing tag"""

	tag = Tag.query.get_or_404(tag_id)
	return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
	"""Updates existing tag"""

	tag = Tag.query.get_or_404(tag_id)

	tag.name = request.form['tagname']

	db.session.add(tag)
	db.session.commit()

	return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
	"""Deletes existing tag"""

	tag = Tag.query.filter_by(id=tag_id).delete()
	db.session.commit()

	return redirect('/tags')





