from flask import Flask,render_template,redirect,request
from flask import current_app as app #it refers to the app object created

from .models import *# both resides in same folder

@app.route("/login",methods=["GET","POST"])#url with specific http method gives specific 
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()#LHS attribute name in table, RHS is data fetched from form 
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return render_template("admin_dash.html",username=username)#lhs>jinja, rhs>data variable
                else:
                    return render_template("user_dash.html",username=username)
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])#url with specific http method gives specific resource
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email= request.form.get("email")
        pwd = request.form.get("pwd")
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user = User(username=username,email=email,password=pwd)#LHS attribute name in table, RHS is data fetched from form 
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        


    return render_template("register.html")
