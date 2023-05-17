from flask import Flask,redirect, render_template,request,url_for
import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='templete')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
db=SQLAlchemy(app)
class User(db.Model):
   user_id=db.Column(db.Integer,primary_key=True)
   username=db.Column(db.String,nullable=False)  
   email=db.Column(db.String,unique=True,nullable=False)
   password=db.Column(db.Integer,nullable=False)
   gender=db.Column(db.String,nullable=False)
class Useredit(db.Model):
    useredit_id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,nullable=False)
    profile_pic=db.Column(db.String)   
    bio=db.Column(db.String)
    createdate=db.Column(db.DateTime)
class pending(db.Model):
   pendind_id=db.Column(db.Integer,primary_key=True)
   friend_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user=db.relationship('User')

class reject(db.Model):
   reject_id=db.Column(db.Integer,primary_key=True)
   friends_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user=db.relationship('User')
class accept(db.Model):
   accept_id=db.Column(db.Integer,primary_key=True)
   friend_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForignKey('user.user_id'))
   user=db.relationship('User')
class block(db.Model):
   block_id=db.Column(db.Integer,primary_key=True)
   blockaccept_id=db.Column(db.Integer,db.ForignKey('accept.accept_id'))
   accept=db.relationship('accept')
  




@app.route('/',methods=['POST', 'GET'])
def userregister():
   if request.method == 'POST':
           firstname=request.form['firstname']  
           lastname=request.form['lastname'] 
           email=request.form['email'] 
           password=request.form['password'] 
           user=User(firstname=firstname,lastname=lastname,email=email,password=password)
           db.session.add(user)
           db.session.commit()
           return redirect(url_for('userlogin'))
   return render_template('Register.html')
@app.route('/userlogin',methods=['POST', 'GET'])
def userlogin():
   if request.method == 'POST':
           
    return render_template('Login.html')    
@app.route('/userforget',methods=['POST', 'GET'])
def userforget():
   if request.method == 'POST':
           
    return render_template('ForgetPassword.html')    
@app.route('/userchange',methods=['POST', 'GET'])
def userchange():
   if request.method == 'POST':
           
    return render_template('ChangePassword.html')  
@app.route('/userresetpassword',methods=['POST', 'GET'])
def userreset():
   if request.method == 'POST':
           
    return render_template('ResetPassword.html')          
with app.app_context():
    db.create_all()
