from flask import Flask,redirect, render_template,request,url_for,session
from datetime import datetime
import os
from os.path import join
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='static/'
app = Flask(__name__)
app.config['SECRET_KEY'] = b'r3t058rf3409tyh2g-rwigGWRIGh[g'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


# app.config['MAIL_USERNAME'] = os.environ.get('USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db=SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    child = db.relationship('User_profile', backref='parent', uselist=False)

class User_profile(db.Model):
    user_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String, default='I am SMedia user')
    profile_pic = db.Column(db.String)
    createddate = db.Column(db.DateTime,default = datetime.utcnow)
   #  profile_pic = db.Column(db.String, default=r'C:\Users\kaman\OneDrive\Desktop\Smedia_copy\Profile_pic\profile-icon-png-908.png')
    u_id = db.Column(db.ForeignKey('user.user_id'))
class Pending(db.Model):
    pendind_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', foreign_keys=[friend_id, user_id], backref='pending_relationship', primaryjoin="and_(Pending.friend_id==User.user_id, Pending.user_id==User.user_id)")

class Reject(db.Model):
    reject_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', foreign_keys=[friend_id, user_id], backref='reject_relationship', primaryjoin="and_(Reject.friend_id==User.user_id, Reject.user_id==User.user_id)")

class Accept(db.Model):
    accept_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    blocked = db.Column(db.Boolean, default=False)
    user = db.relationship('User', foreign_keys=[friend_id, user_id], backref='accept_relationship', primaryjoin="and_(Accept.friend_id==User.user_id, Accept.user_id==User.user_id)")


@app.route('/',methods=['POST', 'GET'])
def userlogin():
        if request.method == 'POST':
            email = request.form['email']
            session['login'] = email
            password = request.form['password']
            print("pasdsdsffsfsdf1",password)
            obj = User.query.filter_by(email=email).first()
            #   user = User.query.filter_by(email=email)
            print(obj.password)
            if obj:
                if obj.password == password:
                    
                    session['name'] = obj.username
                    session['s_id'] = obj.user_id
                    print("+++++++++++++++++++++++++++",session['s_id'] )
                    return redirect(url_for('home'))
                else:
                    return "please enter correct password"
            else:
                return "please register first"   
        else:
            return render_template('Login.html')
@app.route('/userregister',methods=['POST', 'GET'])
def userregister():
   
   if request.method == 'POST':
           username=request.form['username']  
           email=request.form['email'] 
           password=request.form['password'] 
           confirm_password = request.form['confirm_password']
           gender=request.form['gender']
           if password == confirm_password:
                user=User(username=username,email=email,password=password,gender=gender)
                db.session.add(user)
                db.session.commit()
                default_image_path = 'static/user.jpg'
                obj = User_profile(u_id=user.user_id,profile_pic=default_image_path)
                db.session.add(obj)
                db.session.commit()
                return redirect(url_for('userlogin'))
           else:
              return "wrong password"
   else:
        return render_template('Registration.html')
   


    
@app.route('/userforget',methods=['POST', 'GET'])
def userforget():
   if request.method=='POST':
      email=request.form['email'] 
      session['email']=email   
      msg = Message(sender ='solankivaishali2001q@gmail.com',
                    recipients = [email])
      msg.html = '<a href="http://127.0.0.1:5000/resetpassword">Resetlink</a>'
      mail.send(msg)
      return 'Sent' 
   return render_template('ForgotPassword.html')  
    
@app.route('/userchange',methods=['POST', 'GET'])
def userchange():
   if request.method=='POST':
      email=request.form['email']
      oldpassword=request.form['Current_password']
      newpassword=request.form['New_password']
      conformpassword=request.form['retype_password']
      resetpassword = User.query.filter_by(email=email, password=oldpassword).first()
      if resetpassword != None:
            if newpassword == conformpassword:
                resetpassword.password = newpassword
                db.session.commit()   
                return redirect(url_for('userlogin'))
            else:
               return render_template('ChangePassword.html')
   return render_template('ChangePassword.html')
@app.route('/resetpassword',methods=['POST', 'GET'])
def userreset():
    if request.method=='POST':
      mail = session['email']
      newpassword=request.form['password'] 
      confrompassword=request.form['confirm_password']  
      if newpassword==confrompassword:
            obj = User.query.filter_by(email=mail).first()
            if obj is not None:
               obj.password = newpassword
               db.session.commit() 
            return redirect(url_for('userlogin'))
      else:
            return render_template('ResetPassword.html')
    
           
    return render_template('ResetPassword.html')  
@app.route('/viewprofile',methods=['POST','GET'])
def viewprofile():
   email=session['login']
   user_view=guests=db.session.query(User,User_profile).filter(User.email==email).filter(User.user_id == User_profile.u_id).first()
   data=dict()
   data['profile_pic']=user_view.User_profile.profile_pic   
   data['bio']=user_view.User_profile.bio
   data['user_id']=user_view.User.user_id
   data['username']=user_view.User.username
   data['gender']=user_view.User.gender
   data['createddate']=user_view.User_profile.createddate
   return render_template('dash.html',user_view=data) 

@app.route('/home',methods=['POST', 'GET'])
def home():
   user_view=User.query.all()
   name=session.get('name')
   return render_template('home.html',name=name)  


@app.route('/editprofile', methods=['POST','GET'])
def editprofile():
   id=session['s_id']
   user = User_profile.query.filter_by(u_id=int(id)).first()
   if request.method=='POST':
      user.profile_pic = request.files['profile_pic']
      user.bio = request.form['bio']     
      filename=secure_filename(user.profile_pic.filename)
      user.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      user.profile_pic=app.config['UPLOAD_FOLDER']+filename
      db.session.commit()
      return redirect(url_for('viewprofile'))
   return render_template('editprofile.html', user=user)

@app.route('/sign_out', methods=["GET", "POST"])
def sign_out():
    del session['name']
    return redirect(url_for('userlogin'))

@app.route('/search_friend', methods=["GET", "POST"])
def search_friend():
    user = User.query.all()
    s_id = session['s_id']
    if request.method == 'POST':

        for u in user:
            print("username",u.username)
            if u.username==request.form['search_friend']:
                if u.user_id != s_id:
                # print("user_iddddddd",s_id)
                # print("friend_iddddddd",u.user_id)
                    user=Pending(friend_id=u.user_id,user_id = s_id)
                    db.session.add(user)
                    db.session.commit()
                else:
                    return "You cannot send request to your self!"
            # else:
            #     return "user not found"
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    
@app.route('/pending_list')
def pending_list():
   logged_user=session.get('s_id')
   # user = User.query.get(logged_user).user_id
   # user.user_id
   p_list =Pending.query.filter_by(friend_id=logged_user)
   
   # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",p_list.first())
   requested_person = {}
   for p in p_list:
        # print("+++++++++++++++++++++++++++++++",p.user_id)
        uid = p.user_id
        # print("uid", uid)
        uname = User.query.get(uid).username
        # print("Uname",uname)
        requested_person[uid] = uname
        # print("-------------------",requested_person)
        # print(requested_person.uname) k
#    for uid, uname in requested_person.items():
#     print("User ID:", uid)
#     print("Username:", uname)    

   if requested_person:
        print("!!!!!!!!!!!!!!!!!!!!!",requested_persond)
        return render_template('pending_list.html',pending_users=p_list,requested_person=requested_person)
   else:
       return "no pending list"

@app.route('/accept_req/<id>', methods=["GET","POST"])
def accept_req(id):
    logged_user=session.get('s_id') 
    if logged_user:
        user=Accept(friend_id=id,user_id=logged_user)
        db.session.add(user)     
        db.session.commit()
    pendding = Pending.query.filter_by(user_id=id,friend_id=logged_user).delete()
    print("idididididididi",id) 
    print("pending....",pendding)
    if pendding:
        # db.session.delete(pendding)
        db.session.commit()
        return redirect(url_for('pending_list'))
    return "hello"

    

@app.route('/reject_req/<id>', methods=["GET","POST"])
def reject_req(id):
    # reject = Pending.query.get(id)
    # try:
    #     db.session.delete(reject)
    #     db.session.commit()
    #     return redirect(url_for('pending_list'))

    # except Exception as e:
    #     print(e)
    logged_user=session.get('s_id') 
    pendding = Pending.query.filter_by(user_id=id,friend_id=logged_user).delete()
    if pendding:
        db.session.commit()
        return redirect(url_for('pending_list'))
    return "hello"

@app.route('/show_user')
def show_user():
    u_list =User.query.all()
    for u in u_list:
        print("SMedia User..", u.username)
            
        
with app.app_context():
    db.create_all()
if __name__ == "__main__":     
   app.run(debug=True) 
