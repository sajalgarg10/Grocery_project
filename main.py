import os
from flask import Flask, jsonify
from application import config
from application.config import LocalDevelopmentConfig
import json
from application.model import User, Product, Category, Cart
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import current_app as app
from application.validation import  BusinessValidationError
from application.database import  db


app = None
api = None


def create_app():
    app = Flask(__name__ )
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    with app.app_context():
      db.create_all()
    return app

app = create_app()

from flask import Flask, jsonify



###########------------------------ User-----------------------------------------------------------------------

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == 'POST':
      try:
        username = request.form['username']
        password = request.form['password']
        login_obj = User.query.filter_by(username = username).first()
        #db.session.query(User).filter(username = username).first()
        if login_obj:
          print("login obj is fine ")
          if password == login_obj.password:
            print("password condintion is right")
            return redirect(url_for('user_dashboard', username = username ))
          else:
            raise BusinessValidationError(status_code=400, error_message="password is invalid")
        else:
          raise BusinessValidationError(status_code=400, error_message="User is not present, please register.......")          
      except :
        print("Something went wrong")  
        return render_template('404.html' )
        

      
@app.route('/user_dashboard', methods = ['GET', 'POST'])
def user_dashboard():
  if request.method == 'GET':
    try:
      username = request.args.get('username')
      cat = Category.query.all()
      prod = Product.query.all()
      user_ = User.query.filter_by(username = username).first()
      return render_template("user_dashboard.html", categories = cat, products = prod, user = user_) 
    except BusinessValidationError as e:
        # Handle the custom exception
        return render_template("error_page.html", error=e)
  


##########################----------------------Admin---------------------------------------------------------
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    elif request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      try:
        admin_obj = User.query.filter_by(username = username).first()
        #admin_obj = db.session.query(User).filter_by(username = username).first()
        if admin_obj.admin:
          if password == admin_obj.password:
            return redirect(url_for('admin_dashboard'))
          else:
            raise BusinessValidationError(status_code=400, error_message="password is invalid")  
        else:
          raise BusinessValidationError(status_code=400, error_message="Not a admin")
      except BusinessValidationError as e:
        # Handle the custom exception
        return render_template("error_page.html", error=e)
      except:
        return render_template('404.html')
        
      
@app.route('/admin_dashboard', methods = ['GET', 'POST'])
def admin_dashboard():
  if request.method == 'GET':
    # try:
    cat = Category.query.all()
    prod = Product.query.all()
    print(prod)
    print(cat)
    # print(prod[0].manu_date)
    return render_template("dashboard.html", category = cat, products = prod)
    # return render_template("dashboard.html", category = cat)
      
    # except:
    #   print("error")
  else:
    print("something went wrong")
    return render_template('404.html')
    
#####------------------------------add_category---------------------------------------------------
@app.route('/add_category', methods = ['GET','POST'])
def add_category():
  if request.method == 'GET':
    return render_template("add_category.html")
  if request.method == 'POST':
    category_name = request.form['category_name']
    print(category_name)
    try:
      cat_obj = Category.query.filter_by(category_name = category_name).first()
      print(cat_obj)
      category = Category(category_name = category_name)
      print("query cate object in database")
      if cat_obj is None:
        print("if condition")
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
      else:
          raise BusinessValidationError(status_code=400, error_message="Category already exists......")    
    except:
      print("error")
      return render_template('404.html')
    
    
    
######------------------------------update_category-----------------------------------------------------------
@app.route('/update_category/<int:id>', methods = ['GET','POST'])
def update_category(id):
  category_to_update = Category.query.filter_by(category_id = id).first()
  if request.method == 'GET':
    return render_template("update_category.html", category_to_update = category_to_update)
  if request.method == 'POST':
    # category_name_old = request.form['category_name']
    print("post request")
    category_name_upadate = request.form['updated_category_name']
    try:
      if category_to_update:
        category_to_update.category_name = category_name_upadate
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    except:
      print("error")
      return render_template('404.html') 
  # else:
  #    return render_template("update_category.html", category_to_update = category_to_update)
        
      
      
###############------------------------delete_category--------------------------------------------------------
@app.route('/delete_category/<int:id>', methods = ['GET','POST'])
def delete_category(id):
  category_to_delete = Category.query.filter_by(category_id = id).first()
  if request.method == 'GET':
    return render_template("delete_category.html", category_to_delete = category_to_delete)
  if request.method == 'POST':
    # category_name_old = request.form['category_name']
    print("post request")
    try:
      if category_to_delete:
        print("dhfgdsjhgdsjjdshgcjhgdchjgshgxhggdjgjhddf")
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    except:
      print("error") 
      return render_template('404.html')
  
#####-----------------------------------add_product-----------------------------------------------------------

@app.route('/add_product/<int:id>', methods = ['GET','POST'])
def add_product(id):
  category = Category.query.filter_by(category_id = id).first()
  print(category)
  if request.method == 'GET':
    return render_template("add_product.html", category = category)
  if request.method == 'POST':
    product_name = request.form['product_name']
    unit = request.form['unit']
    #manu_date = request.form['manu_date']
    rate = request.form['rate']
    quantity = request.form['quantity']
    try:
      prod_obj = Product.query.filter_by(product_name = product_name).first()
      print(prod_obj)
      print("woking the cat")
      if prod_obj is None:
        print("if condition worked")
        #print(manu_date) manu_date = datetime.strptime(manu_date, '%Y-%m-%d') datetime.strptime(product_manu_update, '%Y-%m-%d')
        prod = Product(product_name = product_name,  unit = unit, rate = rate, quantity = quantity, cat_id = id)
        db.session.add(prod)
        db.session.commit()
        # return True
        return redirect(url_for('admin_dashboard'))
      else:
        raise BusinessValidationError(status_code=400, error_message="product already exists......")  
    except:
      print("error")
      return render_template('404.html')




#####-----------------------------------update_product-----------------------------------------------------------
@app.route('/update_product/<int:id>', methods = ['GET','POST'])
def update_product(id):
  product_to_update = Product.query.filter_by(product_id = id).first()
  if request.method == 'GET':
    return render_template("update_product.html", product_to_update = product_to_update)
  if request.method == 'POST':
    print("post request")
    product_name_upadate = request.form['update_product_name']
    product_unit_update = request.form['update_unit']
    product_rate_update = request.form['update_rate']
    product_quantity_update = request.form['update_quantity']
    try:
      if product_to_update:
        print("inside if condition")
        product_to_update.product_name = product_name_upadate
        product_to_update.unit = product_unit_update
        product_to_update.rate = product_rate_update
        product_to_update.quantity = product_quantity_update
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    except:
      print("error") 
      return render_template('404.html')
      
      
      
###############------------------------delete_product--------------------------------------------------------
@app.route('/delete_product/<int:id>', methods = ['GET','POST'])
def delete_product(id):
  product_to_delete = Product.query.filter_by(product_id = id).first()
  if request.method == 'GET':
    return render_template("delete_product.html", product_to_delete = product_to_delete)
  if request.method == 'POST':
    # category_name_old = request.form['category_name']
    print("post request")
    try:
      if product_to_delete:
        print("inside if condition")
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    except:
      print("error") 
      return render_template('404.html')


########################-----register admin and user -----------------------------------------------------------
  
@app.route("/register", methods = ['GET','POST'])
def register():
    print("********************************") 
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == 'POST':
        secret_key = "qwerty"
        print("Register initial",request.form)
        username = request.form['username']
        password = request.form['password']
        key = request.form['key']
        repeat_password = request.form['repeat_password']
        print("post request")
        try:
          if " " in username:
            print("if for user")
            raise BusinessValidationError(status_code=400, error_message="invalid username")   
          if len(password) < 8:
            print("if for password")
            raise BusinessValidationError(status_code=400, error_message="password does not complete the requirement") 
          if password != repeat_password:
            print("password match condition")
            raise BusinessValidationError(status_code=400, error_message="password does not match") 
          user_ = User.query.filter_by(username = username).first()
          if user_ is None:
            print("Register initial----",request.form)
            if secret_key == key:
              new_user = User(username=username, admin=True,password=password)
            else:
              new_user = User(username=username, admin=False,password=password)
            db.session.add(new_user)
            db.session.commit() 
            return redirect(url_for('login')) 
          else:
             raise BusinessValidationError(status_code=400, error_message="user exist........")
          # else:
          #   print("fehjsdhj")
          #   raise BusinessValidationError(status_code=400, error_message="user already exist") 
        except:
          print("error") 
          return render_template('404.html')    
        
        

##################################buy_product_user-------------------------------------------------------------
@app.route('/buy_product/<int:id>/user/<int:u_id>', methods = ['GET','POST'])
def buy_product(id, u_id):
  g_user = User.query.filter_by(user_id = u_id).first()
  product_to_buy = Product.query.filter_by(product_id = id).first()
  if request.method == 'GET':
    return render_template("buy_product.html", product_to_buy = product_to_buy, g_user = g_user )
  if request.method == 'POST':
    # category_name_old = request.form['category_name']
    print("post request")
    try:
      if product_to_buy:
        print("inside if condition ")
        buy_quantity = int(request.form["buy_quantity"])
        print(buy_quantity)
        amount = product_to_buy.rate * int(buy_quantity)
        print(amount)
        if buy_quantity > product_to_buy.quantity:
          print("if condition for buy_quantity")
          print(buy_quantity)
          return render_template("out_of_stock.html", user = g_user)
        
        product_to_buy.quantity  = product_to_buy.quantity - int(buy_quantity)
        print(product_to_buy.quantity)
        cart = Cart(user_id = u_id, product_id = id, quantity = buy_quantity, amount = amount)
        print(cart)
        db.session.add(cart)
        print("successffuly added")
        db.session.commit()
        return redirect(url_for('user_dashboard', username = g_user.username ))
    except:
      print("error") 
      return render_template('404.html')



@app.route('/cart/<int:id>', methods = ['GET','POST'])
def  cart(id):
  if request.method == "GET":
    print("get request")
    print(id)
    user = User.query.filter_by(user_id = id).first()
    print(user)
    cart = []
    cart_obj = Cart.query.filter_by(user_id = id).all()
    print(cart_obj)
    for i in cart_obj:
      j = {}
      j["product_id"] = i.product_id
      j["quantity"] = i.quantity
      j["amount"] = i.amount
      prod = Product.query.filter_by(product_id = i.product_id).first()
      # print(prod)
      j["product_name"] = prod.product_name
      cart.append(j)
    return render_template("cart.html", cart = cart , user = user)


@app.route('/search/<int:id>', methods=["GET", "POST"])
def search(id):
  if request.method == "POST":
    user = User.query.filter_by(user_id = id).first()
    print(user.user_id)
    sea = request.form["search"]
    cat = Category.query.filter(Category.category_name.like('%'+ sea + '%')).all()
    if cat:
      result = []
      for i in cat:
        results = Product.query.filter_by(cat_id = i.category_id).all()
        print(results)
        for prod in results:
          j = {}
          j["product_name"] = prod.product_name
          j["product_id"] = prod.product_id
          j["category_name"] = i.category_name
          j["rate"] = prod.rate
          j["quantity"] = prod.quantity
          j["unit"] = prod.unit
          print(j)
          result.append(j)
          print(result)
    if cat ==[]:    
      results = Product.query.filter(Product.product_name.like('%'+ sea + '%')).all()
      print(results)
      result = []
      for prod in results:
            cat_p =  Category.query.filter_by(category_id = prod.cat_id).first()
            j = {}
            j["product_id"] = prod.product_id
            j["product_name"] = prod.product_name
            j["category_name"] = cat_p.category_name
            j["rate"] = prod.rate
            j["quantity"] = prod.quantity
            j["unit"] = prod.unit
            result.append(j)
            print(j)
            print(result)
    return render_template("search.html", result  = result, user = user)         


#######-----------------------------------Summary-----------------------------------------------------------
@app.route('/summary', methods=['GET', 'POST'])
def summary():
  try:
    cart = Cart.query.all()
    print("cart object")
    cart_l = [["Product","amount earned per product"]]
    dic_cart = {}
    for i in cart:
      print("in side loop")
      prod = Product.query.filter_by(product_id = i.product_id).first()
      print(prod)
      print("product list")
      if prod.product_name in dic_cart:
        dic_cart[prod.product_name] = dic_cart[prod.product_name] + i.amount
      else:  
        dic_cart[prod.product_name] = i.amount  
    print("loop has ended")  
    print(dic_cart) 
    for j in dic_cart.items():
      l = []
      l.append(j[0])
      l.append(j[1])
      cart_l.append(l)
    print(cart_l)
    return render_template('summary.html', cart_l = cart_l)
  except:
    return render_template('404.html')
  
  
  



if __name__ == '__main__':
  # Run the Flask app
  app.run()
