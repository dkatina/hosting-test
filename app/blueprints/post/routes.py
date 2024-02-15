from . import post
from .forms import CreatePostForm
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user
from app.models import Posts, db
#create post route
@post.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm()
    if request.method == 'POST' and form.validate_on_submit:
        img = form.img.data
        caption = form.caption.data
        location = form.location.data
        new_post = Posts(img=img, caption=caption, location=location, user_id=current_user.id)
        new_post.save()
        flash('SUCCESS! Post Created', 'success')
        return render_template('create_post.html', form=form)
    else:
        return render_template('create_post.html', form=form)


#feed route displaying all posts
@post.route('/feed')
def feed():
    posts = Posts.query.all()
    return render_template('feed.html', posts=posts)

#edit post route.
@post.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Posts.query.get(post_id)
    form = CreatePostForm()
    if post and post.user_id == current_user.id:
        if request.method == 'POST' and form.validate_on_submit():
            img = form.img.data
            caption = form.caption.data
            location = form.location.data

            post.img = img
            post.caption = caption
            post.location = location

            post.save()
            return redirect(url_for('post.feed'))
        else:
            return render_template('edit_post.html', form=form, post=post)
    else:
        flash("Don't be a Snake", 'danger')
        return redirect(url_for('posts.feed'))
    

@post.route('/delete/<post_id>')
def delete_post(post_id):
    print(post_id)
    post = Posts.query.get(post_id)
    print(post)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('post.feed'))
    else:
        flash("Don't be a Snake", 'danger')
        return redirect(url_for('posts.feed'))