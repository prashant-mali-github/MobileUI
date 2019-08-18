from flask import Blueprint, render_template, redirect, request,flash,url_for,session,g
from models.create_models import User
import functools
from werkzeug.security import check_password_hash,generate_password_hash
from app import db

auth = Blueprint('auth', __name__, template_folder='template')

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        error=None
        username = request.form['username']
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['confirm_password']

        if password == c_password:
            user = User.query.filter_by(username=username).first()
            if not user:
                register = User(username=username,role=role, password=password,email=email)
                db.session.add(register)
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                error = "Username already exist"
                flash(error)
        else:
            error="Password and confirm password not match"
            flash(error)
    return render_template("static priya mobile/users/adduser.html")



@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        error = None
        uname = request.form["username"]
        passw = request.form["password"]
        user = User.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, passw):
            session['user_id'] = user.id
            return redirect(url_for('order.totalsale'))
        else:
            error = "Please enter valid credential"
            flash(error,".......errtor")
            print(error,"...............")
            return render_template("static priya mobile/users/loginuser.html")
    return render_template("static priya mobile/users/loginuser.html")

@auth.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        error = None
        uname = request.form["username"]
        passw = request.form["password"]
        new_password = request.form['new_password']
        user = User.query.filter_by(username=uname).first()
        user_pass = user.password
        if check_password_hash(user_pass,new_password):
            error = "password exist"
            flash(error)
            return render_template("static priya mobile/users/forgot_password.html")
        else:
            user.password = generate_password_hash(new_password)
            db.session.add(user)
            db.session.commit()
            session.clear()
            return render_template("static priya mobile/users/loginuser.html")
    return render_template("static priya mobile/users/forgot_password.html")


@auth.route('/users')
def view_users():
    users = User.query.all()
    return render_template('static priya mobile/users/view_users.html', users=users)

@auth.route('/<int:id>/deleteuser')
def delete_user(id):
    user = User.query.get(int(id))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.view_users'))




@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
