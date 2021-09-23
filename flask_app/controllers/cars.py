from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.car import Car
from flask_app.models.user import User
from flask_bcrypt import Bcrypt 



@app.route("/cars/new" )
def add_car():

    if not session.get("user_first_name") is None:
        return render_template("new_car.html")
    else:
        return redirect('/')



# register user route
@app.route("/cars/create", methods = ["POST"])
def create_car():

    print(session['user_id'])

    # if len(request.form["price"]) !=0: 
    #     price= int(request.form["price"])
    #      # flash("check the errors!")
    #     return redirect("/cars/new")
    
    price = int(request.form["price"])

    data={
        "user_id": session['user_id'],
        "price": price,
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
      
    }

    isvalid = Car.validate_car(data)

    if isvalid: 
            Car.create_car(data)      
            return redirect("/dashboard") 
    else:
        # flash("check the errors!")
        return redirect("/cars/new")
   

@app.route("/cars/<int:car_id>", methods=["GET"] )
def show_car(car_id):

    data={
            "id": car_id
        }
    car = Car.get_car(data)

    # car.year = str(car.year)

    user_id = car.user_id  
    sec_data={
            "id": user_id
        }
    user = User.get_one_user(sec_data)
    return render_template("car_info.html", car = car, user=user)


@app.route("/cars/edit/<int:car_id>",  methods=["GET","POST"] )
def edit_car_form(car_id):
    if not session.get("user_first_name") is None:
       
        data={
            "id":car_id
        }

        car_info = Car.get_car(data)      
        return render_template("update_car.html", car = car_info)
     
    else:
        return redirect('/')

@app.route("/cars/delete/<int:car_id>", methods = ["GET","POST"])
def del_car(car_id):

    data={
            "id": car_id
        }

    Car.delete_car(data)

    return redirect("/dashboard")

# update user route
@app.route("/cars/update", methods=["GET","POST"] )
def update_car():

    if not session.get("user_first_name") is None:
        car_id = request.form["id"] 
        if request.form['price'] != '':
            price = int(request.form["price"])
        else:
            return redirect("/cars/edit/{{car_id}}") 
    
        
        data={
            "id": request.form['id'],
            "user_id": session['user_id'],
            "price": price,
            "model": request.form["model"],
            "make": request.form["make"],
            "year": request.form["year"],
            "description": request.form["description"]
      
        }
        isvalid = Car.validate_car(data)

        if isvalid: 
            Car.update_car(data)    
            return redirect("/dashboard") 
    else:
        # flash("check the errors!")
        return redirect("/cars/edit/{{car_id}}")









