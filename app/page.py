from app import app, db
from app.models import User, Page
from flask import Flask, redirect, render_template, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
import datetime, time

#custom widget for rendering a QuillJS input
def TinyMCE(field):
    return """  <script src="//cdn.tinymce.com/4/tinymce.min.js"></script>
         <script>tinymce.init({ 
            selector:'#editor', 
            theme: 'modern',
			plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'save table contextmenu directionality emoticons template paste textcolor autoresize'
            ],
            content_css: '/static/css/tinymce.css',
            toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor'
         });</script>
         <textarea id='editor'> %s </textarea>""" % field._value()

class NewPageForm(Form):
    title = StringField('Title:', validators=[validators.Length(min=0,max=1000)])
    body = TextAreaField('Body:', validators=[validators.Length(min=0,max=75000)], widget=TinyMCE)
    bodyhtml = HiddenField();


def new_page():
    form = NewPageForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data

        if len(title) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = body
            return render_template("editpage.html", form=form, title=title)

        name = "-".join(title.split(" ")).lower()

        newpage = Page(title=title, name=name, body=body)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5);
        return redirect("/page/" + name)

    return render_template("newpage.html", form=form)


def edit_page(page_name):
    if not page_name: 
        return render_template("404.html"), 404

    currentPage = Page.query.filter_by(name=page_name).first()
    if not currentPage:
        return render_template("404.html"), 404

    form = NewPageForm()

    title = currentPage.title
    bodyhtml = currentPage.body

    form.body.data = bodyhtml

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data

        if len(newtitle) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = newbody
            return render_template("editpage.html", form=form, title=newtitle)

        newname = "-".join(newtitle.split(" ")).lower()

        if newname != page_name:
            page = Page.query.filter_by(name=newname).first()
            if page:
                form.title.errors.append("A page with this name already exists.")
                form.body.data = newbody
                return render_template("editpage.html", form=form, title=newtitle)

        currentPage.title = newtitle
        currentPage.body = newbody
        currentPage.name = newname
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + newname)

    return render_template("editpage.html", form=form, title=title)


def delete_page(page_name):
    if not page_name:
        return render_template("404.html"), 404

    page = Page.query.filter_by(name=page_name)
    if not page:
        return render_template("404.html"), 404

    page.delete()
    db.session.commit()
    return redirect("/")

