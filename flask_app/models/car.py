from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
 



class Car:
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create_car(cls,data):
        query = "INSERT INTO cars (user_id,price,model,make,year,description) VALUES (%(user_id)s,%(price)s,%(model)s,%(make)s,%(year)s,%(description)s);"
        my_db = connectToMySQL("car_deals_schema")
        car_id = my_db.query_db(query,data)
     
        return car_id

    @classmethod
    def get_car(cls, data):

        query= "SELECT * FROM cars WHERE id= %(id)s;"
        my_db = connectToMySQL("car_deals_schema")
        car_info = my_db.query_db(query,data)

        if len(car_info) <= 0:
            return None
        else:
            car_info = car_info[0]
            return Car(car_info)


    @classmethod
    def get_cars(cls, data):

        query= "SELECT * FROM cars WHERE user_id= %(id)s;"
        my_db = connectToMySQL("car_deals_schema")
        car_info = my_db.query_db(query,data)
        cars = []
        print('inside get cars.......')
        print(car_info)
        if car_info == False:
            return None
        for u in car_info:
            cars.append(cls(u))
        return cars

    @classmethod
    def delete_car(cls,data):
        query= " DELETE FROM cars WHERE id= %(id)s;"
        my_db = connectToMySQL("car_deals_schema")
        my_db.query_db(query,data)
        return

    
    @classmethod
    def update_car(cls,data):         
        query = "UPDATE cars SET price = %(price)s ,model = %(model)s , make = %(make)s, year = %(year)s, description = %(description)s   WHERE id = %(id)s;"
        my_db = connectToMySQL("car_deals_schema")
        my_db.query_db(query,data)
        return

    
    @staticmethod
    def validate_car(data):
        is_valid = True 
      
        if data['price'] <= 0:
            flash("Price must be more than zero.")
            is_valid = False
        if len(data['year']) <=0:
            flash("Year must be more than zero")
            is_valid = False
        # if len(data['price']) < 1:
        #     flash("price cannot be blank.")
        #     is_valid = False
        # if len(data['year']) < 1:
        #     flash("year cannot be blank.")
            # is_valid = False
        if len(data['model']) < 1:
            flash("model cannot be blank.")
            is_valid = False
        if len(data['make']) < 1:
            flash("make cannot be blank.")
            is_valid = False
        if len(data['description']) < 1:
            flash(" cannot be blank.")
            is_valid = False

        return is_valid

     

        