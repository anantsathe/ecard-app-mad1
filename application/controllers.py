from flask import Flask,render_template,redirect,request
from flask import current_app as app #it refers to the app object created

from .models import *# both resides in same folder
import random
import string
#imports for graphs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

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
    users= len(User.query.all())-1
    requests = len(Info.query.filter_by(atr_value="requested").all())
    generated = len(Info.query.filter_by(atr_value="generated").all())
    return render_template("admin_dash.html", this_user=this_user, all_info=all_info,users=users,requests=requests,generated=generated)

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
    
@app.route("/update_status/<card>/<int:user_id>",methods=["GET","POST"])
def update_status(card,user_id):
    details = Info.query.filter_by(user_id=user_id,c_name=card).all()
    detail= Info.query.filter_by(user_id=user_id,c_name=card,atr_name="status").first()
    if request.method == "POST":
        status= request.form.get("status")
        detail.atr_value = status
        db.session.commit()
        return redirect("/admin")

    return render_template("update_status.html",user_id=user_id,card=card,details=details)

@app.route("/generate/<card>/<int:user_id>")
def generate(card,user_id):
    detail= Info.query.filter_by(user_id=user_id,c_name=card,atr_name="status").first()
    detail.atr_value = "generated"
    db.session.commit()
    key = ""
    if card == "aadhar":
        key = random.randint(10**11, 10**12 - 1)
        # key = random.randint(1,10)
    elif card == "pan":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=5))
        middle_part = ''.join(random.choices(string.digits, k=4))
        last_part = random.choice(string.ascii_uppercase)
        key = first_part + middle_part + last_part
    elif card == "driving":
        part1 = ''.join(random.choices(string.ascii_uppercase, k=2))
        part2 = ''.join(random.choices(string.digits, k=2))
        part3 = ''.join(random.choices(string.digits, k=7))
        key = part1+"-"+part2+"-2025-"+part3
    elif card== "election":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        last_part = ''.join(random.choices(string.digits, k=7))
        key = first_part + last_part
    info1 = Info(atr_name="key",atr_value=key,c_name=card,user_id=user_id)
    db.session.add(info1)
    db.session.commit()
    return redirect("/admin")

@app.route("/view/<card>/<int:user_id>")
def view(card,user_id):
    details = Info.query.filter_by(user_id=user_id,c_name=card).all()
    if card == "aadhar":
        return render_template("view_aadhar.html",details=details)
    elif card == "pan":
        return render_template("view_pan.html",details=details)
    elif card == "driving":
        return render_template("view_drive.html",details=details)
    elif card == "election":
        return render_template("view_elec.html",details=details)
    
@app.route("/results")
def search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if key == "user":
        results = User.query.filter_by(username= search_word).all()
    else:
        results = Info.query.filter_by(atr_name="status",c_name = search_word.lower()).all()
    return render_template("results.html",results=results,key=key)

@app.route("/summary")
def summary():
    #requested cards
    ra = len(Info.query.filter_by(atr_value="requested",c_name="aadhar").all())
    rp = len(Info.query.filter_by(atr_value="requested",c_name="pan").all())
    rd = len(Info.query.filter_by(atr_value="requested",c_name="driving").all())
    re = len(Info.query.filter_by(atr_value="requested",c_name="election").all())
    #cards under verification
    uva = len(Info.query.filter_by(atr_value = "under_verification",c_name="aadhar").all())
    uvp = len(Info.query.filter_by(atr_value = "under_verification",c_name="pan").all())
    uvd = len(Info.query.filter_by(atr_value = "under_verification",c_name="driving").all())
    uve = len(Info.query.filter_by(atr_value = "under_verification",c_name="election").all())
    # verified cards
    va = len(Info.query.filter_by(atr_value="verified",c_name="aadhar").all())
    vp = len(Info.query.filter_by(atr_value="verified",c_name="pan").all())
    vd = len(Info.query.filter_by(atr_value="verified",c_name="driving").all())
    ve = len(Info.query.filter_by(atr_value="verified",c_name="election").all())
    #generated cards
    ga = len(Info.query.filter_by(atr_value="generated",c_name="aadhar").all())
    gp = len(Info.query.filter_by(atr_value="generated",c_name="pan").all())
    gd = len(Info.query.filter_by(atr_value="generated",c_name="driving").all())
    ge = len(Info.query.filter_by(atr_value="generated",c_name="election").all())

    #graphs
    #pie chart (generated cards)
    labels = ["Aadhar","Pan","Driving","Election"]
    sizes =[ga,gp,gd,ge]
    colors = ["red","yellow","blue","green"]
    plt.pie(sizes,labels=labels,colors=colors,autopct = "%1.1f%%")
    plt.title("Generated Cards")
    plt.savefig("static/pie.png")
    plt.clf()
    #bar graph (requested cards)
    labels = ["Aadhar","Pan","Driving","Election"]
    sizes = [ra,rp,rd,re]
    plt.bar(labels,sizes)
    plt.xlabel("Requested Cards")
    plt.ylabel("No of Cards")
    plt.title("Requested Cards Distribution")
    plt.savefig("static/bar.png")
    plt.clf()

    return render_template("summary.html",ra=ra,rp=rp,rd=rd,re=re,
                           uva=uva,uvp=uvp,uvd=uvd,uve=uve,
                           va=va,vp=vp,vd=vd,ve=ve,
                           ga=ga,gp=gp,gd=gd,ge=ge)