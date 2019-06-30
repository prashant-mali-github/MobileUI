from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()


def create_app(main=True):

    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'prashantmali.info@gmail.com'
    app.config['MAIL_PASSWORD'] = "Prashant@#123"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobileshop.db'
    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True

    db.init_app(app)

    # Setup Marshmallow

    # Setup Flask-Mail
    mail.init_app(app)

    migrate.init_app(app, db)

    from users.adduser import auth
    app.register_blueprint(auth)

    from customers.customers import customer
    app.register_blueprint(customer)

    from items.items import item
    app.register_blueprint(item)

    from orders.orders import order
    app.register_blueprint(order)

    app.add_url_rule('/', endpoint='auth.login')
    return app
