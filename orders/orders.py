from flask import Blueprint, render_template, redirect, request,flash,url_for,session,g
from models.create_models import SalesItems,Customer,Items, Bill,User,Customer_Orders
import functools
from werkzeug.security import check_password_hash
from app import db
import random

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
    # db.session.query(SalesItems).delete()
    # db.session.commit()
    orders = SalesItems.query.all()
    sum = 0
    for order in orders:
        bill = Bill.query.filter_by(o_id=int(order.id)).first()
        #sum += int(bill.bill_amount)
    bills = Bill.query.all()
    return render_template('static priya mobile/orders/vieworders.html',orders=orders,bills=bills)

@order.route('/viewbills')
def viewbills():
    # db.session.query(Bill).delete()
    # db.session.commit()
    # db.session.query(Customer_Orders).delete()
    # db.session.commit()
    bills = Bill.query.all()
    return render_template('static priya mobile/orders/viewbills.html',bills=bills)


@order.route('/<int:id>/deletebill')
def deletebills(id):
    bill = Bill.query.filter_by(id=int(id)).first()
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for('order.viewbills'))

@order.route('/sale_item', methods=['GET', 'POST'])
def sale_items():
    global customers
    customers = Customer.query.all()
    items = Items.query.all()
    if request.method == "POST":
        customer_name = request.form.get('c_id')
        item_names = request.form.getlist('i_id')
        quantities = request.form.getlist('quantity')
        one_quantity = quantities[0]
        print(quantities,"....quantities")
        #print(item_names, "....i_name")
        quantities = str(quantities)
        #print(quantities.strip("[']'").split(','),"....quantity")
        ql = quantities.strip("[']'").split(',')
        if not customer_name or not item_names or not quantities:
            flash('Please enter all the fields', 'error')
        customer = Customer.query.filter_by(customer_name=customer_name).first()
        print(len(items),"....length")
        if len(item_names) == 1:
            item = Items.query.filter_by(item_name=str(item_names[0])).first()
            print(item.item_quantity,"....quantity")
            if not customer:
                error = "Invalid customer ID"
                flash(error)
            if not item:
                error = "Invalid Item ID"
                flash(error)
            available_quantity = int(item.item_quantity)
            print(quantities[0],"..qu0")
            sale_quantity = int(one_quantity)
            bill_amount = int(item.item_price) * int(sale_quantity)
            import pyqrcode
            url = pyqrcode.create(
                f"{item.item_name}------\n---{item.item_price}--\n----{item.item_quantity}---\n--Total={bill_amount}")
            url.png('orders/bill.png', scale=8)
            with open("orders/bill.png", "rb+") as f:
                x = f.read()
            if available_quantity >= sale_quantity:
                order_id = random.randint(1000000000, 999999999999)
                order = SalesItems(id=order_id, c_id=customer.c_id, i_id=item.i_id, sale_quantity=sale_quantity)
                customer_order = Customer_Orders(c_id=customer.c_id, o_id=order_id)
                db.session.add_all([order, customer_order])
                db.session.commit()
                item.item_quantity = available_quantity - sale_quantity
                bill = Bill(o_id=order_id, bill_amount=bill_amount, bill_barcode=x)
                db.session.add_all([item, bill])
                db.session.commit()
                return redirect(url_for('order.vieworders'))

        elif len(item_names) > 1 and len(quantities) > 1:
            bills =[]
            orders = []
            bills_amount = []
            items = []
            item_quantities = dict(zip(item_names, ql))
            print(item_quantities,"......dictioanry")
            for item_name , quantity in item_quantities.items():
                item = Items.query.filter_by(item_name=str(item_name)).first()
                print(item.item_quantity,"....quantity")
                print(item_name, "....item_name")
                available_quantity = int(item.item_quantity)
                sale_quantity = int(quantity)
                bill_amount = int(item.item_price) * int(sale_quantity)
                print(bill_amount,"....bill_amount")
                #bills_amount.append(bill_amount)
                #bills_amounts = sum(bills_amount)
                order_id = random.randint(1000000000, 999999999999)
                import pyqrcode
                url = pyqrcode.create(
                    f"{item.item_name}------\n---{item.item_price}--\n----{item.item_quantity}---\n--Total={bill_amount}")
                url.png('orders/bill.png', scale=8)
                with open("orders/bill.png", "rb+") as f:
                    x = f.read()
                if available_quantity >= sale_quantity:
                    order = SalesItems(id=order_id, c_id=customer.c_id, i_id=item.i_id, sale_quantity=sale_quantity)
                    print(order_id, ".....order_id")
                    print(item.item_name, "...name")
                    # orders.append(order_id)
                    db.session.add(order)
                    db.session.commit()
                    customer_order = Customer_Orders(c_id=customer.c_id, o_id=order_id)
                    db.session.add(customer_order)
                    item.item_quantity = available_quantity - sale_quantity
                    print("order", order_id)
                    bill = Bill(o_id=order_id, bill_amount=bill_amount, bill_barcode=x)
                    db.session.add_all([item,bill])
                    #orders.append(order)
                    #items.append(item)
                    #db.session.commit()
            db.session.commit()
            print(orders, "..orders")
            print(items, "...items")
            return redirect(url_for('order.vieworders'))
                # else:
                #     error = "Please enter less sale quantity than available quantity"
                #     flash(error)

    return render_template('static priya mobile/orders/sale_item.html', customers=customers, items=items)

@order.route('/totalsales')
def totalsale():
    orders = SalesItems.query.all()
    customers = Customer.query.all()
    user = User.query.all()
    items = Items.query.all()
    customers = len(customers)
    items = len(items)
    sum = 0
    for order in orders:
        bill = Bill.query.filter_by(o_id=int(order.id)).first()
        sum += int(bill.bill_amount)
    bills = Bill.query.all()
    total_orders = len(orders)
    users = len(user)
    return render_template('static priya mobile/orders/dashboard.html', sum=sum, customers=customers, items=items, total_orders=total_orders, users=users)

@order.route('/searchorders')
def searchorders():
    orders = SalesItems.query.all()
    return render_template('static priya mobile/orders/find_order.html', orders=orders)


def customer_orders_details(customer_id):
    customer_items = []
    customer_orders = SalesItems.query.filter_by(c_id=customer_id).all()
    print(customer_orders, "...corders")
    sum = 0
    for order in customer_orders:
        bill = Bill.query.filter_by(o_id=int(order.id)).first()
        customer_items.append(order.i_id)
        sum += int(bill.bill_amount)
    return customer_items, customer_orders


@order.route('/customerbills', methods = ['GET', 'POST'])
def customer_bills():
    orders = SalesItems.query.all()
    customers = Customer.query.all()
    customer_info = zip(orders, customers)
    customer_data = {}
    customer_items = []
    global customer_name
    if request.method == "POST":
        customer_name = request.form.get('c_id')
        customer = Customer.query.filter_by(customer_name=customer_name).first()
        customer_orders = SalesItems.query.filter_by(c_id=customer.c_id).all()
        sum = 0
        for order in customer_orders:
            bill = Bill.query.filter_by(o_id=int(order.id)).first()
            customer_items.append(order.i_id)
            sum += int(bill.bill_amount)
        customer_data[customer_name] = customer_items
        return render_template('static priya mobile/orders/customer_orders.html', customers=customers, sum=sum, customername = customer_name)
    return render_template('static priya mobile/orders/customer_orders.html', customers=customers)