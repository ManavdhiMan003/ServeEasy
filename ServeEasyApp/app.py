from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import MySQLdb


app=Flask(__name__)

import yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQ_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db'] 
mysql = MySQL(app)


user_details=()
@app.route('/home')
def home():
    return render_template('home.html',user_details=())

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/home/<int:user_id>')
def user_home(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
        cursor.execute(query)
        user_details = cursor.fetchall()
        return render_template('home.html',user_details=user_details)
    except Exception as e:
        return str(e)


@app.route('/sign_up',methods=['POST','GET'])
def sign_up():
    if(request.method=='POST'):
        user_details = request.form
        name = user_details['name']
        username = user_details['username']
        email = user_details['email']
        password = user_details['password']
        phone = user_details['phone']
        
        cur = mysql.connection.cursor()
        cur.execute("insert into user value(%s,%s,%s,%s,%s)",(name,0,username,email,phone))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/home')
    return render_template('sign_up.html')

@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if(request.method=='POST'):
        user_details = request.form
        username = user_details['username']
        user_password = user_details['password']
        # print(username,password)
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query="SELECT user_id AS user_id ,password AS password FROM user WHERE username ="+"'"+username+"'"
            cursor.execute(query)
            password_id_details = cursor.fetchall()
            print(password_id_details)
            if(len(password_id_details)==0):
                return "user dosn't exist try another or sign up"
            else:
                if(user_password==password_id_details[0]['password']):
                    
                    url_for_user_home='/home/'+str(password_id_details[0]['user_id'])
                    return redirect(url_for_user_home, user_details=())
                else:
                    return "wrong password try again"
        except Exception as e:
            return str(e)
    return render_template('sign_in.html')


@app.route('/my_products/<user_id>',methods=['GET'])
def my_products(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        query="SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from all_products where owner_id = "+"'"+user_id+"'"
        cursor.execute(query)
        my_products = cursor.fetchall()
        return render_template('my_products.html',my_products=my_products,user_details=user_details)
    except Exception as e:
        return str(e)

@app.route('/products/all/<user_id>',methods=['GET'])
def all_product(user_id):
    user_id=int(user_id)
    try:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from all_products;")
        all_products = cursor.fetchall()
        # print(user_id)
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        print(user_details)
        return render_template('all_product.html',user_details=user_details,all_products=all_products)
    except Exception as e:
        return str(e)

@app.route('/products/programming/<int:user_id>',methods=['GET'])
def programming_products(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from programming_products;")
        programming_products = cursor.fetchall()
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        return render_template('programming_products.html',user_details=user_details,programming_products=programming_products)
    except Exception as e:
        return str(e)
    
@app.route('/products/freestyle/<int:user_id>',methods=['GET'])
def freestyle_products(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from freestyle_products;")
        freestyle_products = cursor.fetchall()
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        return render_template('freestyle_products.html',user_details=user_details,freestyle_products=freestyle_products)
    except Exception as e:
        return str(e)

@app.route('/products/design/<int:user_id>',methods=['GET'])
def design_products(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from design_products;")
        design_products = cursor.fetchall()
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        return render_template('design_products.html',user_details=user_details,design_products=design_products)
    except Exception as e:
        return str(e)

@app.route('/products/physical/<int:user_id>',methods=['GET'])
def physical_products(user_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name AS product_name, est_price as est_price, average_rating as average_rating, NO_OF_TIME as no_of_time from physical_products;")
        physical_products = cursor.fetchall()
        if(user_id!=-1):
            query="SELECT name,username,email,phone,user_id from user where user_id = "+str(user_id)
            cursor.execute(query)
            user_details = cursor.fetchall()
        else:
            user_details=()
        return render_template('physical_products.html',user_details=user_details,physical_products=physical_products)
    except Exception as e:
        return str(e)

if __name__=='__main__':
    app.run(debug=True)

