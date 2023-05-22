from flask import Flask,redirect, render_template,request,url_for,session
from datetime import datetime
import os
from os.path import join
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='static/'
app = Flask(__name__, template_folder='templete')
app.config['SECRET_KEY'] = b'r3t058rf3409tyh2g-rwigGWRIGh[g'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db=SQLAlchemy(app)
class User(db.Model):
   user_id=db.Column(db.Integer,primary_key=True)
   username=db.Column(db.String,nullable=False)  
   email=db.Column(db.String,unique=True,nullable=False)
   password=db.Column(db.Integer,nullable=False)
   gender=db.Column(db.String,nullable=False)
class Userprofile(db.Model):
   useredit_id = db.Column(db.Integer,primary_key=True)
   user_id=db.Column(db.ForeignKey('user.user_id'))
   profile_pic=db.Column(db.String)   
   bio=db.Column(db.String(255), default="i am using whatapps")
   createdate=db.Column(db.DateTime, default=datetime.utcnow)  
   user=db.relationship('User')
# class pending(db.Model):
#    pending_id=db.Column(db.Integer,primary_key=True)
#    friend_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user=db.relationship('User')
# class reject(db.Model):
#    reject_id=db.Column(db.Integer,primary_key=True)
#    friends_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user=db.relationship('User')
# class accept(db.Model):
#    accept_id=db.Column(db.Integer,primary_key=True)
#    friend_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
#    user=db.relationship('User')
# class block(db.Model):
#    block_id=db.Column(db.Integer,primary_key=True)
#    blockaccept_id=db.Column(db.Integer,db.ForeignKey('accept.accept_id'))
#    accept=db.relationship('accept')
@app.route('/',methods=['POST', 'GET'])
def userregister():
   if request.method == 'POST':  
      username=request.form['username'] 
      email=request.form['email'] 
      password=request.form['password'] 
      conpassword=request.form['con_password'] 
      gender=request.form['gender']  
      if password==conpassword:
         user=User(username=username,email=email,password=password,gender=gender)
         db.session.add(user)
         db.session.commit()
         default_image_path ='static/user.jpg'
         edit = Userprofile(user_id=user.user_id, profile_pic=default_image_path)
         db.session.add(edit)
         db.session.commit()
         return redirect(url_for('userlogin'))
      else:
         return "wrong password"
   return render_template('Register.html')
@app.route('/userlogin',methods=['POST', 'GET'])
def userlogin():
   if request.method == 'POST':
         email = request.form['email']
         session['login']= email
         password = request.form['password']
         obj = User.query.filter_by(email=email,password=password).first()
         if obj:
               session['name']=obj.username
               return redirect(url_for('home'))   
         else:
            return "please enter valid email and password"   
   else:
      return render_template('Login.html')
    
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
   user_view=guests=db.session.query(User,Userprofile).filter(User.email==email).filter(User.user_id == Userprofile.user_id).first()
   data=dict()
   data['profile_pic']=user_view.Userprofile.profile_pic   
   data['bio']=user_view.Userprofile.bio
   data['user_id']=user_view.User.user_id
   data['username']=user_view.User.username
   data['gender']=user_view.User.gender
   data['createdate']=user_view.Userprofile.createdate
 
   return render_template('dash.html',user_view=data) 
@app.route('/home',methods=['POST', 'GET'])
def home():
   user_view=User.query.all()
   name=session.get('name')
   return render_template('home.html',name=name)  
@app.route('/editprofile/<id>', methods=['POST','GET'])
def editprofile(id):
   user = Userprofile.query.filter_by(user_id=int(id)).first()
   if request.method=='POST':
      user.profile_pic = request.files['profile_pic']
      user.bio = request.form['bio']     
      filename=secure_filename(user.profile_pic.filename)
      user.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      user.profile_pic=app.config['UPLOAD_FOLDER']+filename
      db.session.commit()
   return render_template('editprofile.html', user=user)
if __name__ == "__main__":     
   app.run(debug=True) 
with app.app_context():
    db.create_all()
