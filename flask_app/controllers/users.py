from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.car import Car

from flask_bcrypt import Bcrypt 


bcrypt = Bcrypt(app)


# home page
@app.route("/")
def index():
    return render_template("login_page.html")


# register user route
@app.route("/register", methods = ["POST"])
def register_user():

    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }

    isvalid = User.validate_user(data)

    if isvalid:
        new_email = {    
        "email": request.form["email"]
         }
        user = User.get_user(new_email)
        if user == None:     
            user_id = User.register_user(data)
            session['user_first_name'] = request.form["first_name"]
            session['user_id'] = user_id
            return redirect("/dashboard") 
        else:
            flash("Your email has already been registered!")
            return redirect("/")

    return redirect("/")

#Login route
@app.route("/login", methods = ["POST"] )
def login_user():

    data= {
        "email": request.form["email"],
        "password": request.form["password"]
       
    }
    #check for validations
    isvalid = User.validate_login(data)

    if isvalid:
        new_data = {    
        "email": request.form["email"]
         }
        user = User.get_user(new_data)
        if user == None:
            flash("Your email is invalid!")
            return redirect('/')
        
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Your Password is incorrect!')
            return redirect('/')
        
        session['user_id'] = user.id
        session['user_first_name'] = user.first_name
        session['user_email']= user.email
        return redirect("/dashboard")  
    else:
        return redirect('/')

#main page/car route
@app.route("/dashboard")
def main_page():

    if not session.get("user_first_name") is None:

        all_cars = User.get_cars_and_sellers()
        
        return render_template("dashboard.html", car_list = all_cars) 
    else:
        return redirect('/')


#Log out route
@app.route("/logout")
def logout_user():
    #clear sessions
    session.clear()
    # redirect back to login page
    return redirect("/")

#route for editing user
@app.route("/users/edit/<int:user_id>",  methods=["GET","POST"] )
def edit_user_form(user_id):
    if not session.get("user_first_name") is None:
       
        data={
            "id":user_id
        }
        print('.....................................')
        print('.......................in edit .................')
        my_user= User.get_one_user(data)
        user_car = Car.get_car(data)      
        return render_template("update_user.html", user = my_user, car = user_car)
     
    else:
        return redirect('/')

# update user route
@app.route("/users/update", methods=["GET","POST"] )
def update_user():

    if not session.get("user_first_name") is None:     
        data={
            "fn": request.form["fname"],
            "ln": request.form["lname"],
            "email": request.form["email"],
            "id":request.form["id"]
        }
        User.update_user(data)
        return redirect("/dashboard")
    else:
        return redirect('/')






