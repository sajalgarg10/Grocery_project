from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique = True)
    admin = db.Column(db.Boolean, nullable = False )
    cart = db.relationship('Cart', backref='User.user_id', cascade = "all, delete")

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, nullable = False)
    product = db.relationship('Product', backref='Category.category_id', cascade = "all, delete")

    #content = db.Column(db.String)
    #authors = db.relationship("User", secondary="article_authors")

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable = False)
    #manu_date = db.Column(db.DateTime, nullable=False)
    unit = db.Column(db.String, nullable = False)
    rate = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer,nullable = False )
    cat_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    cart = db.relationship('Cart', backref='Product.product_id', cascade = "all, delete")
    
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer,nullable = False  )
    amount = db.Column(db.Integer,nullable = False)

    
   

