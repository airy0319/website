from app import app, login_signup, models, login_manager, post, faculty, page
from app.models import User, Post, Page, Faculty, Message
from flask_login import login_required
from flask import render_template, request, redirect

@app.route('/')
@app.route('/index/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("index.html", posts=posts)

@app.route('/page/<string:page_name>/')
def render_page(page_name):
    page = Page.query.filter_by(name=page_name).first();
    return render_template("page.html", page=page);

@app.route('/newpage/', methods=["GET", "POST"])
def new_page():
    return page.new_page()

@app.route('/news/')
def news():
    if request.args.get("postid"):
        post = Post.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_template("news/newsitem.html", post=post, heading="LASA News")
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("news/news.html", posts=posts, heading="LASA News")

@app.route('/messages/')
def messages():
    if request.args.get("postid"):
        post = Message.query.filter_by(id=request.args.get("postid")).first()
        if post:
            return render_template("news/newsitem.html", post=post, heading="Principal's Messages")
    posts = Message.query.order_by(Message.timestamp.desc())
    return render_template("news/news.html", posts=posts, heading="Principal's Messages")

@app.route('/message/')
def message():
    post = Message.query.order_by(Message.timestamp.desc()).first()
    if not post:
        return redirect("/newmessage")
    return render_template("news/newsitem.html", post=post, heading="Principal's Message")

@app.route('/faculty/')
def all_faculty():
    faculty = Faculty.query.order_by(Faculty.lastname.asc())
    return render_template("faculty/faculty.html", faculty=faculty, title="Faculty")

@app.route('/administration/')
def administration():
    administrators = Faculty.query.filter_by(category="admin").order_by(Faculty.lastname.asc())
    return render_template("faculty/faculty.html", faculty=administrators, title="Administration")

@app.route('/guidance/')
def guidance():
    counselors = Faculty.query.filter_by(category="guidance").order_by(Faculty.lastname.asc())
    return render_template("faculty/faculty.html", faculty=counselors, title="Guidance and Counseling")

@app.route('/teachers/')
def teachers():
    teachers = Faculty.query.filter_by(category="teaching").order_by(Faculty.lastname.asc())
    return render_template("faculty/faculty.html", faculty=teachers, title="Teachers")

@app.route('/support/')
def support():
    support = Faculty.query.filter_by(category="support").order_by(Faculty.lastname.asc())
    return render_template("faculty/faculty.html", faculty=support, title="Support Staff")

@app.route('/history/')
def history():
    return render_template("about/history.html")

@app.route('/profile/')
def profile():
    return render_template("about/profile.html")

@app.route('/accolades/')
def accolades():
    return render_template("about/accolades.html")

@app.route('/contact/')
def contact():
    return render_template("about/contact.html")

@app.route('/mission/')
@app.route('/vision/')
def mission():
    return render_template("about/mission.html")

@app.route('/probation/')
def probation():
    return render_template("academics/probation.html")

@app.route('/schedule/')
def schedule():
    return render_template("calendars/schedule.html")

@app.route('/calendar/')
def calendar():
    return render_template("calendars/master.html")

@app.route('/calendar/college/')
def calendar_college():
    return render_template("calendars/college.html")

@app.route('/calendar/athletic/')
def calendar_athletic():
    return render_template("calendars/athletic.html")

@app.route('/calendar/library/')
def calendar_library():
    return render_template("calendars/library.html")

@app.route('/college/')
def college():
    return render_template("academics/college.html")

@app.route('/college/sessions/')
def college_sessions():
    return render_template("academics/college/sessions.html")

@app.route('/college/reps/')
def college_reps():
    return render_template("academics/college/reps.html")

@app.route('/college/testing/')
def college_testing():
    return render_template("academics/college/testing.html")

@app.route('/college/faq/')
def college_faq():
    return render_template("academics/college/faq.html")

@app.route('/college/aid/')
def college_aid():
    return render_template("academics/college/aid.html")

@app.route('/college/naviance/')
def college_naviance():
    return render_template("academics/college/naviance.html")

@app.route('/courseguide/')
def course_guide():
    return render_template("academics/courseguide.html")

@app.route('/honorcode/')
def honor_code():
    return render_template("academics/honorcode.html")

@app.route('/magnetendorsement/')
def magnet_endorsement():
    return render_template("academics/magnetendorsement.html")

@app.route('/finearts/')
def fine_arts():
    return render_template("academics/finearts.html")

@app.route('/service/')
def students_service():
    return render_template("students/service.html")

@app.route('/ranking/')
def students_ranking():
    return render_template("students/ranking.html")

@app.route('/wellness/')
def students_wellness():
    return render_template("students/wellness.html")

@app.route('/wellness/issues/')
def wellness_issues():
    return render_template("students/wellness/issues.html")

@app.route('/wellness/when/')
def wellness_when():
    return render_template("students/wellness/when.html")

@app.route('/wellness/abuse/')
def wellness_abuse():
    return render_template("students/wellness/abuse.html")

@app.route('/howtoapply/')
def how_to_apply():
    return render_template("admissions/howtoapply.html")

@app.route('/shadowing/')
def shadowing():
    return render_template("admissions/shadowing.html")

@app.route('/coursefaq/')
def course_faq():
    return render_template("admissions/coursefaq.html")

@app.route('/signature/')
def signature_courses():
    return render_template("admissions/signature.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    return login_signup.login()

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    return login_signup.logout()

@app.route("/newpost/", methods=["GET", "POST"])
@login_required
def new_post():
    return post.new_post()

@app.route("/editpost/", methods=["GET", "POST"])
@login_required
def edit_post():
    return post.edit_post()

@app.route("/delpost/")
@login_required
def delete_post():
    return post.delete_post()

@app.route("/newmessage/", methods=["GET", "POST"])
@login_required
def new_message():
    return post.new_message()

@app.route("/editmessage/", methods=["GET", "POST"])
@login_required
def edit_message():
    return post.edit_message()

@app.route("/delmessage/")
@login_required
def delete_message():
    return post.delete_message()

@app.route("/newfaculty/", methods=["GET", "POST"])
@login_required
def new_faculty():
    return faculty.new_faculty()

@app.route("/editfaculty/", methods=["GET", "POST"])
@login_required
def edit_faculty():
    return faculty.edit_faculty()

@app.route("/delfaculty/")
@login_required
def delete_faculty():
    return faculty.delete_faculty()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
