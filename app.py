from flask import Flask,redirect, render_template,request,url_for
from datetime import datetime
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
    useredit_id = db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.ForeignKey('user.user_id'))
    profile_pic=db.Column(db.String, default="/Users/yudiz/Desktop/Project/static/image/user.jpeg")   
    bio=db.Column(db.String(255),default="i am whatapp using")
    createdate=db.Column(db.DateTime,default=datetime.utcnow())  
    user=db.relationship('User')
class pending(db.Model):
   pending_id=db.Column(db.Integer,primary_key=True)
   friend_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user=db.relationship('User')
class reject(db.Model):
   reject_id=db.Column(db.Integer,primary_key=True)
   friends_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user=db.relationship('User')
class accept(db.Model):
   accept_id=db.Column(db.Integer,primary_key=True)
   friend_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
   user=db.relationship('User')
class block(db.Model):
   block_id=db.Column(db.Integer,primary_key=True)
   blockaccept_id=db.Column(db.Integer,db.ForeignKey('accept.accept_id'))
   accept=db.relationship('accept')
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
            obj=Useredit(user_id=user)
            db.session.add(obj)
            db.session.commit()
            return redirect(url_for('userlogin'))
         else:
            return "wrong password"
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
@app.route('/viewprofile',methods=['POST','GET'])
def viewprofile():
   user_view=User.query.all()
   return render_template('dashboard.html',user_view=user_view) 

if __name__ == "__main__":     
   app.run(debug=True) 
with app.app_context():
    db.create_all()



 
