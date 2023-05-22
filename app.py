from flask import Flask,redirect, render_template,request,url_for,session
from flask_sqlalchemy import SQLAlchemy
import datetime

# app = Flask(__name__,template_folder='templete')
app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SECRET_KEY'] = "secret key"
    db = SQLAlchemy(app)
except Exception as e:
    print(e)
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
    profile_pic = db.Column(db.String, default=r'C:\Users\kaman\OneDrive\Desktop\Smedia_copy\Profile_pic\profile-icon-png-908.png')
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
                obj = User_profile(u_id=user.user_id)
                db.session.add(obj)
                db.session.commit()
                return redirect(url_for('userlogin'))
           else:
              return "wrong password"
   else:
        return render_template('Registration.html')

@app.route('/userlogin',methods=['POST', 'GET'])
def userlogin():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            print("pasdsdsffsfsdf1",password)
            obj = User.query.filter_by(email=email).first()
            #   user = User.query.filter_by(email=email)
            print(obj.password)
            if obj:
                if obj.password == password:
                    session['name'] = obj.username
                    session['s_id'] = obj.user_id
                    return redirect(url_for('home'))
                else:
                    return "please enter correct password"
            else:
                return "please register first"   
        else:
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
@app.route('/home',methods=['POST','GET'])
def home():
    name = session.get('name')
    return render_template('home.html',name=name)

@app.route('/sign_out', methods=["GET", "POST"])
def sign_out():
    del session['name']
    return redirect(url_for('userlogin'))

@app.route('/search_friend', methods=["GET", "POST"])
def search_friend():
    user = User.query.all()
    s_id = session['s_id']

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)
