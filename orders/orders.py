from flask import Blueprint, render_template, redirect, request,flash,url_for,session,g
from models.create_models import SalesItems,Customer,Items, Bill
import functools
from werkzeug.security import check_password_hash
from app import db

order = Blueprint('order', __name__, template_folder='template')

# import random
# @order.route('/addorder/', methods=['GET', 'POST'])
# def addorders():
#     if request.method == "POST":
#         error=None
#         c_id = request.form['c_id']
#         i_id = request.form['i_id']
#         quantity = request.form['quantity']
#         if not c_id or not i_id or not quantity:
#             flash('Please enter all the fields', 'error')
#         else:
#             customer = Customer.query.filter_by(c_id=int(c_id)).first()
#             item = Items.query.filter_by(i_id=i_id).first()
#
#             if not customer:
#                 error = "Invalid customer ID"
#                 flash(error)
#             if not item:
#                 error = "Invalid Item ID"
#                 flash(error)
#
#             available_quantity = int(item.item_quantity)
#             sale_quantity = int(quantity)
#
#             bill_amount = int(item.item_price) * int(sale_quantity)
#             order_id = random.randint(1000000000,999999999999)
#             if available_quantity > sale_quantity:
#                 order = SalesItems(id=order_id, c_id=c_id, i_id=i_id, sale_quantity=sale_quantity)
#                 db.session.add(order)
#                 db.session.commit()
#                 item.item_quantity = available_quantity - sale_quantity
#                 bill = Bill(i_id=i_id, c_id=i_id,o_id=order_id,bill_amount=bill_amount)
#                 db.session.add_all([item,bill])
#                 db.session.commit()
#                 return redirect(url_for('order.home'))
#             else:
#                 error="Please enter less sale quantity than available quantity"
#                 flash(error)
#
#     return render_template("static priya mobile/orders/createorder.html")


@order.route('/vieworders')
def vieworders():
    orders = SalesItems.query.all()
    sum = 0
    for order in orders:
        bill = Bill.query.filter_by(o_id=int(order.id)).first()
        sum += int(bill.bill_amount)
    bills = Bill.query.all()
    return render_template('static priya mobile/orders/vieworders.html',orders=orders,bills=bills)

@order.route('/viewbills')
def viewbills():
    bills = Bill.query.all()
    return render_template('static priya mobile/orders/viewbills.html',bills=bills)


@order.route('/<int:id>/deletebill')
def deletebills(id):
    bill = Bill.query.filter_by(id=int(id)).first()
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for('order.viewbills'))

@order.route('/totalsales')
def totalsale():
    orders = SalesItems.query.all()
    customers = Customer.query.all()
    items = Items.query.all()
    customers = len(customers)
    items = len(items)
    sum = 0
    for order in orders:
        bill = Bill.query.filter_by(o_id=int(order.id)).first()
        sum += int(bill.bill_amount)
    bills = Bill.query.all()
    return render_template('static priya mobile/orders/dashboard.html',sum=sum,customers=customers,items=items)

@order.route('/searchorders')
def searchorders():
    orders = SalesItems.query.all()
    return render_template('static priya mobile/base.html',orders=orders)

