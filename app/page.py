from app import app, db, utils
from app.models import User, Page
from flask import Flask, redirect, request
from flask_login import current_user
from flask_wtf import Form
from wtforms import validators, StringField, TextAreaField, HiddenField, SelectField, BooleanField
from flask_wtf.html5 import IntegerField
from wtforms.validators import DataRequired
import datetime, time

choices = [('none', 'None'),
                ('calendars', 'Calendars'),
                ('about', 'About Us'),
                ('academics', 'Academics'),
                ('students', 'Students'),
                ('parents', 'Parents'),
                ('admissions', 'Admissions')]

#custom widget for rendering a TinyMCE input
def TinyMCE(field):
    return """  <script src="//cdn.tinymce.com/4/tinymce.min.js"></script>
         <script>tinymce.init({ 
            selector:'#editor', 
            theme: 'modern',
            height: 800,
			plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'save table contextmenu directionality emoticons template paste textcolor'
            ],
            table_default_attributes: {
            class: 'table-condensed'
            },
            content_css: '/static/css/tinymce.css',
            toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor'
         });</script>
         <textarea id='editor'> %s </textarea>""" % field._value()

class NewPageForm(Form):
    title = StringField('Title:', validators=[validators.Length(min=0,max=1000)])
    category = SelectField('Category:', choices=choices)
    dividerBelow = BooleanField('Divider below page name in dropdown menu')
    index = IntegerField('Ordering index (lower is higher up):', validators=[validators.Optional()])
    body = TextAreaField('Body:', validators=[validators.Length(min=0,max=75000)], widget=TinyMCE)
    bodyhtml = HiddenField()


def new_page():
    form = NewPageForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.bodyhtml.data
        category = form.category.data
        dividerBelow = form.dividerBelow.data
        index = form.index.data

        if len(title) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)

        if index and (index<0 or index>100):
            form.index.errors.append("Number must be between 0 and 100.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)

        name = "-".join(title.split(" ")).lower()

        page = Page.query.filter_by(name=name).first()
        if page:
            form.title.errors.append("A page with this name already exists.")
            form.body.data = body
            return utils.render_with_navbar("newpage.html", form=form, title=title, index=index)


        newpage = Page(title=title, name=name, category=category, dividerBelow=dividerBelow, index=index, body=body)
        db.session.add(newpage)
        db.session.commit()
        time.sleep(0.5);
        return redirect("/page/" + name)

    return utils.render_with_navbar("newpage.html", form=form)


def edit_page(page_name):
    if not page_name: 
        return utils.render_with_navbar("404.html"), 404

    currentPage = Page.query.filter_by(name=page_name).first()
    if not currentPage:
        return utils.render_with_navbar("404.html"), 404


    title = currentPage.title
    bodyhtml = currentPage.body
    category = currentPage.category
    dividerBelow = currentPage.dividerBelow
    index = currentPage.index

    form = NewPageForm(category=category, dividerBelow=dividerBelow)

    form.body.data = bodyhtml

    if form.validate_on_submit():
        newtitle = form.title.data
        newbody = form.bodyhtml.data
        newcategory = form.category.data
        newdividerBelow = form.dividerBelow.data
        newindex = form.index.data

        if len(newtitle) < 1:
            form.title.errors.append("This field is required.")
            form.body.data = newbody
            return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        if index and (index<0 or index>100):
            form.index.erros.append("Number must be between 0 and 100.")
            form.body.data = newbody
            return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        newname = "-".join(newtitle.split(" ")).lower()

        if newname != page_name:
            page = Page.query.filter_by(name=newname).first()
            if page:
                form.title.errors.append("A page with this name already exists.")
                form.body.data = newbody
                return utils.render_with_navbar("editpage.html", form=form, title=newtitle, index=newindex)

        currentPage.title = newtitle
        currentPage.body = newbody
        currentPage.name = newname
        currentPage.category = newcategory
        currentPage.dividerBelow = newdividerBelow
        currentPage.index = newindex
        db.session.commit()
        time.sleep(0.5)
        return redirect("/page/" + newname)

    return utils.render_with_navbar("editpage.html", form=form, title=title, index=index)


def delete_page(page_name):
    if not page_name:
        return utils.render_with_navbar("404.html"), 404

    page = Page.query.filter_by(name=page_name)
    if not page:
        return utils.render_with_navbar("404.html"), 404

    page.delete()
    db.session.commit()
    return redirect("/")
