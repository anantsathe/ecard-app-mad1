from flask import current_app as app,request,jsonify
from .models import User
from .database import db

@app.post("/api/login")
def api_login():
    username = request.json.get("username")
    password = request.json.get("password")
    try:
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == password: 
                if this_user.type == "admin":
                    return jsonify(message="admin logged in successfully")
                else:
                    return jsonify(message="user logged in successfully")
            else:
                return jsonify(error="Incorrect password"),400
        else:
            return jsonify(error="User not found"),404
    except:
        return jsonify(error="Internal Server Error"),500

@app.post("/api/register")
def api_register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user_name = User.query.filter_by(username = username).first()
        user_email = User.query.filter_by(email = email).first()
        if user_name or user_email:
            return jsonify(message="user already exists"),400
        else:
            new_user = User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message="user created successfully"),201
    except:
        return jsonify(error= "Internal server error"),500
    
@app.put("/api/update/<int:user_id>")
def api_update(user_id):
    try:
        this_user = User.query.get(user_id)
        if this_user:
            this_user.username = request.json.get("username")
            this_user.email = request.json.get("email")
            this_user.password = request.json.get("password")
            db.session.commit()
            return jsonify(message="user updated successfully"),200
        else:
            return jsonify(error="Incorrect user id"),400
    except:
        return jsonify(error = "Internal server error"),500
    
@app.delete("/api/delete/<int:user_id>")
def api_delete(user_id):
    try:
        this_user = User.query.get(user_id)
        if this_user:
            db.session.delete(this_user)
            db.session.commit()
            return jsonify(message ="user deleted successfully"),200
        else:
            return jsonify(error="Incorrect user id"),400
    except:
        return jsonify(error= "Internal server error"),500
               
