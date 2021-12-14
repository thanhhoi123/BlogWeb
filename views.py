import os
from flask import Blueprint, render_template, request, redirect
from flask.helpers import flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from models import Post, User, Comment, Follow
from initial import db
from werkzeug.utils import secure_filename  

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET', 'POST'])
# @login_required
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if request.method == 'POST':
        post = request.form.get('post')
        pic = request.files['image']
        picdata = ""
        if not pic:
            picdata = ""
        else:
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(".\static",filename))
            picdata = filename
        if len(post) < 1:
            flash('post is too short!', category='error')
        else:
            new_post = Post(body = post, author_id = current_user.id, img = picdata)
            db.session.add(new_post)
            db.session.commit()
            flash('Post is created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('home/index.html', user= current_user, posts= posts)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/edit-post/<id>", methods = ['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author_id:
        flash('You do not have permission to delete this post.', category='error')
    elif request.method == 'POST':
        body = request.form.get('post')
        pic = request.files['image']
        picdata = ""
        if not pic:
            picdata = ""
        else:
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(".\static",filename))
            picdata = filename
        if len(body) < 1:
            flash('post is too short!', category='error')
        else:
            # new_post = Post(body = body, author_id = current_user.id, img = picdata)
            post.body = body
            post.img = picdata
            # db.session.add(new_post)
            db.session.commit()
            flash('Post is updated!', category='success')
            return redirect(url_for('views.home'))
    return render_template('edit-post.html', user= current_user, post= post)


@views.route("/posts/<author_id>")
def posts(author_id):
    user = User.query.filter_by(id=author_id).first()
    username = user.username

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author_id=user.id).all()
    return render_template("userpost.html", user=current_user, posts=posts, username=username, author=user)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                content=text, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.user_id and current_user.id != comment.post_comment.author_id:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/profile/<author_id>")
def profile(author_id):
    user = User.query.filter_by(id=author_id).first()
    follower = current_user
    hasfollow = Follow()
    if follower.is_authenticated:
        hasfollow = Follow.query.filter_by(follower_id=follower.id, followed_id=user.id).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    return render_template("userprofile.html", Blogger = user,user = current_user, hasfollow = hasfollow)


@views.route("/follow_user/<user_id>", methods=['GET'])
@login_required
def follow(user_id):
    followed = User.query.filter_by(id=user_id).first()
    follower = current_user
    hasfollow = Follow.query.filter_by(follower_id=follower.id, followed_id=followed.id).first()
    if not follower:
        flash('User does not exists.', category='error')
    elif hasfollow:
        db.session.delete(hasfollow)
        db.session.commit()
    else:
        hasfollow = Follow(follower_id= follower.id, followed_id=followed.id)
        db.session.add(hasfollow)
        db.session.commit()
    return redirect(url_for('views.profile', author_id = followed.id))

@views.errorhandler(404)
def page_not_found(e):
    return render_template('404/index.html'), 404

@views.errorhandler(500)
def page_not_found(e):
    return render_template('500/index.html'), 500
