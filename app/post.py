import time
import datetime

from app import db, utils
from app.models import Post, Message
from flask import redirect, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField, HiddenField


class NewPostForm(Form):
    title = StringField('Title:', validators=[validators.DataRequired(), validators.Length(min=0, max=1000)])
    body = TextAreaField('Body:', validators=[validators.Length(min=0, max=30000)], widget=utils.TinyMCE)
    bodyhtml = HiddenField()


def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data

        newpost = Post(title=title, body=body, author=current_user.id_, timestamp=datetime.datetime.now())
        db.session.add(newpost)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/news")

    return utils.render_with_navbar("news/newpost.html", form=form, heading="News Item")

def new_message():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data

        newpost = Message(title=title, body=body, author=current_user.id_, timestamp=datetime.datetime.now())
        db.session.add(newpost)
        db.session.commit()
        time.sleep(0.5)
        return redirect("/message")

    return utils.render_with_navbar("news/newpost.html", form=form, heading="Principal's Message")



def edit_post():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/newpost")

    current_post = Post.query.filter_by(id_=postid).first()
    if not current_post:
        return redirect("/newpost")

    form = NewPostForm()

    title = current_post.title
    body = current_post.body
    form.body.data = body

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data
        current_post.title = newtitle
        current_post.body = newbody
        db.session.commit()
        time.sleep(0.5)
        return redirect("/news?postid="+postid)

    return utils.render_with_navbar("news/editpost.html", form=form, title=title, heading="News Item")

def edit_message():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/messages")

    current_post = Message.query.filter_by(id_=postid).first()
    if not current_post:
        return redirect("/messages")

    form = NewPostForm()

    title = current_post.title
    body = current_post.body
    form.body.data = body

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data
        current_post.title = newtitle
        current_post.body = newbody
        db.session.commit()
        time.sleep(0.5)
        return redirect("/messages?postid="+postid)

    return utils.render_with_navbar("news/editpost.html", form=form, title=title, heading="Principal's Message")


def delete_post():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/news")

    post = Post.query.filter_by(id_=postid)
    post.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/news")

def delete_message():
    postid = request.args.get("postid")
    if not postid:
        return redirect("/messages")

    post = Message.query.filter_by(id_=postid)
    post.delete()
    db.session.commit()
    time.sleep(0.5)
    return redirect("/messages")
