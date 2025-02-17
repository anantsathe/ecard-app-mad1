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
                    return redirect("/admin")
                else:
                    return render_template("user_dash.html",this_user= this_user)
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

@app.route("/admin")
def admin_dash():
    this_user = User.query.filter_by(type="admin").first()
    all_info = Info.query.all()
    return render_template("admin_dash.html", this_user=this_user, all_info=all_info)

@app.route("/home/<int:user_id>")
def user_dash(user_id):
    this_user = User.query.filter_by(id=user_id).first()
    return render_template("user_dash.html",this_user=this_user)

@app.route("/request_card/<int:user_id>",methods=["GET","POST"])
def request_card(user_id):
    if request.method == "POST":
        card = request.form.get("card")
        return redirect(f"/request/{card}/{user_id}")
        # if card == "aadhar":
        #     return render_template("aadhar.html",user_id=user_id)
    return render_template("select.html",user_id=user_id)

@app.route("/request/<card>/<int:user_id>",methods=["GET","POST"])
def card_details(card,user_id):
    this_user = User.query.filter_by(id=user_id).first()
    if card == "aadhar":
        if request.method == "POST":
            fullname = request.form.get("fullname")
            f_name = request.form.get("f_name")
            gender = request.form.get("gender")
            dob = request.form.get("dob")
            address = request.form.get("address")
            image = request.form.get("image")
            info1 = Info(atr_name="fullname", atr_value= fullname, c_name= card, user_id= user_id)
            info2 = Info(atr_name = "f_name", atr_value = f_name,c_name= card, user_id=user_id)
            info3 = Info(atr_name = "gender", atr_value = gender,c_name= card, user_id=user_id)
            info4 = Info(atr_name = "dob", atr_value = dob,c_name= card, user_id=user_id)
            info5 = Info(atr_name = "address", atr_value = address,c_name= card, user_id=user_id)
            info6 = Info(atr_name = "image", atr_value = image,c_name= card, user_id=user_id)
            info7 = Info(atr_name = "status", atr_value= "requested", c_name = card, user_id = user_id)
            db.session.add_all([info1,info2,info3,info4,info5,info6,info7])
            db.session.commit()
            return render_template("user_dash.html",this_user= this_user)

        return render_template("aadhar.html",user_id=user_id)
    elif card == "pan":
        if request.method == "POST":
            fullname = request.form.get("fullname")
            f_name = request.form.get("f_name")
            dob = request.form.get("dob")
            image = request.form.get("image")
            info1 = Info(atr_name="fullname", atr_value= fullname, c_name= card, user_id= user_id)
            info2 = Info(atr_name = "f_name", atr_value = f_name,c_name= card, user_id=user_id)
            # info3 = Info(atr_name = "gender", atr_value = gender,c_name= card, user_id=user_id)
            info4 = Info(atr_name = "dob", atr_value = dob,c_name= card, user_id=user_id)
            # info5 = Info(atr_name = "address", atr_value = address,c_name= card, user_id=user_id)
            info6 = Info(atr_name = "image", atr_value = image,c_name= card, user_id=user_id)
            info7 = Info(atr_name = "status", atr_value= "requested", c_name = card, user_id = user_id)
            db.session.add_all([info1,info2,info4,info6,info7])
            db.session.commit()
            return render_template("user_dash.html",this_user= this_user)

        return render_template("pan.html",user_id=user_id)
    
    elif card == "driving":
        if request.method == "POST":
            fullname = request.form.get("fullname")
            f_name = request.form.get("f_name")
            dob = request.form.get("dob")
            address = request.form.get("address")
            pin = request.form.get("pin")
            image = request.form.get("image")
            info1 = Info(atr_name="fullname", atr_value= fullname, c_name= card, user_id= user_id)
            info2 = Info(atr_name = "f_name", atr_value = f_name,c_name= card, user_id=user_id)
            info3 = Info(atr_name = "pin", atr_value = pin,c_name= card, user_id=user_id)
            info4 = Info(atr_name = "dob", atr_value = dob,c_name= card, user_id=user_id)
            info5 = Info(atr_name = "address", atr_value = address,c_name= card, user_id=user_id)
            info6 = Info(atr_name = "image", atr_value = image,c_name= card, user_id=user_id)
            info7 = Info(atr_name = "status", atr_value= "requested", c_name = card, user_id = user_id)
            db.session.add_all([info1,info2,info3,info4,info5,info6,info7])
            db.session.commit()
            return render_template("user_dash.html",this_user= this_user)

        return render_template("driving.html",user_id=user_id)
    
    elif card == "election":
            
            if request.method == "POST":
                fullname = request.form.get("fullname")
                w_name = request.form.get("w_name")
                gender = request.form.get("gender")
                dob = request.form.get("dob")
                # address = request.form.get("address")
                image = request.form.get("image")
                info1 = Info(atr_name="fullname", atr_value= fullname, c_name= card, user_id= user_id)
                info2 = Info(atr_name = "w_name", atr_value = w_name,c_name= card, user_id=user_id)
                info3 = Info(atr_name = "gender", atr_value = gender,c_name= card, user_id=user_id)
                info4 = Info(atr_name = "dob", atr_value = dob,c_name= card, user_id=user_id)
                # info5 = Info(atr_name = "address", atr_value = address,c_name= card, user_id=user_id)
                info6 = Info(atr_name = "image", atr_value = image,c_name= card, user_id=user_id)
                info7 = Info(atr_name = "status", atr_value= "requested", c_name = card, user_id = user_id)
                db.session.add_all([info1,info2,info3,info4,info6,info7])
                db.session.commit()
                return render_template("user_dash.html",this_user= this_user)

            return render_template("voter.html",user_id=user_id)
    

