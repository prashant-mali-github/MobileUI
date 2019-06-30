from flask import Blueprint, render_template, redirect, request,flash,url_for,session,g
from models.create_models import User,Customer
import functools
from werkzeug.security import check_password_hash
from app import db

customer = Blueprint('customer', __name__, template_folder='template')


@customer.route("/home")
def home():
    return render_template("static priya mobile/orders/dashboard.html")




@customer.route("/viewcustomers")
def viewcustomers():
    customers = Customer.query.all()
    return render_template('static priya mobile/customers/viewcustomers.html',customers=customers)

@customer.route("/totalcustomer")
def totalcustomer():
    customers = Customer.query.all()
    customer = len(customers)
    return render_template('static priya mobile/customers/viewcustomers.html',customers=customers,customer=customer)


@customer.route('/addcustomer/', methods=['GET', 'POST'])
def addcustomer():
    if request.method == "POST":
        error=None

        first_name = request.form['fname']
        last_name = request.form['lname']
        address = request.form['address']
        mno = request.form['mno']
        email = request.form['email']

        if not first_name or not last_name or not address or not mno or not email:
            flash('Please enter all the fields', 'error')
        else:
            name = str(first_name) +"  " + str(last_name)
            # for i in range(50):
            customer = Customer(customer_name=name, c_address=address, c_mobileno=mno, c_email=email)
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customer.viewcustomers'))
    return render_template("static priya mobile/customers/addcustomer.html")


@customer.route('/<int:id>/updatecustomer', methods=('GET', 'POST'))
def updatecustomer(id):
    error = None
    customer = Customer.query.filter_by(c_id=int(id)).first()

    # print("................post",post.title)
    if request.method == 'POST':

        cname = request.form['cname']
        address = request.form['address']
        mno = request.form['mno']
        email = request.form['email']

        error = None

        if not cname or not address or not mno or not email:
            flash(error)
        if error is not None:
            flash(error)
        else:
            customer.customer_name = cname
            customer.c_address = address
            customer.c_mobileno = mno
            customer.c_email = email
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customer.viewcustomers'))
    return render_template('static priya mobile/customers/editcustomer.html', customer=customer)


@customer.route('/<int:id>/deletecustomer', methods=('GET', 'POST'))
def deletecustomer(id):
    error = None
    customer = Customer.query.filter_by(c_id=int(id)).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customer.viewcustomers'))

@customer.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        error = None
        uname = request.form["username"]
        passw = request.form["password"]

        user = User.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, passw):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('customer.home'))
        else:
            error = "Please enter valid credential"
            flash(error,".......errtor")
            print(error,"...............")
    return render_template("static priya mobile/users/loginuser.html")



@customer.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@customer.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('customer.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('customer.login'))
        return view(**kwargs)
    return wrapped_view
