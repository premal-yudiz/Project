from flask import Flask,redirect, render_template,request,url_for,session,flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from os.path import join
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from functools import wraps
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('userlogin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/',methods=['POST', 'GET'])
def userlogin():
        if request.method == 'POST':
            email = request.form['email']
            session['login'] = email
            password = request.form['password']
            
            print("pasdsdsffsfsdf1",password)
            obj = User.query.filter_by(email=email).first()
            #   user = User.query.filter_by(email=email)
            if obj:
                if obj.password == password:
                    
                    session['name'] = obj.username
                    session['s_id'] = obj.user_id
                    session['logged_in'] = True
                    return redirect(url_for('home'))
                else:
                    # flash ("please enter correct password")
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
                try:
                    obj = User.query.filter_by(email=email).first()
                    if obj == None:

                        user=User(username=username,email=email,password=password,gender=gender)
                        db.session.add(user)
                        db.session.commit()
                        default_image_path = 'static/user.jpg'
                        obj = User_profile(u_id=user.user_id,profile_pic=default_image_path)
                        db.session.add(obj)
                        db.session.commit()
                        return redirect(url_for('userlogin'))
                    else:
                        return "this email is already registered"
                except Exception as e:
                    print("error is ",e)
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
   logged_user=session.get('login')
   
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
                    flash("Please Enter Same Password")
                    return render_template('ChangePassword.html')
      else:
          flash("Please Enter Valid Password")
          return render_template('ChangePassword.html',logged_user=logged_user)

         

   return render_template('ChangePassword.html',    logged_user=logged_user)
@app.route('/resetpassword',methods=['POST', 'GET'])
def userreset():
    if request.method=='POST':
    #   mail = session['email']
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
@login_required
def viewprofile():
   email=session.get('login')
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
    user = User.query.all()
    if 'name' in session:
        name = session['name']
        return render_template('home.html', name=name,user=user)
    else:
        return redirect(url_for('userlogin'))

@app.route('/editprofile', methods=['POST', 'GET'])
@login_required
def editprofile():
    id = session['s_id']
    user = User_profile.query.filter_by(u_id=int(id)).first()
    if request.method == 'POST':
        user.bio = request.form['bio']
        profile_pic = request.files['profile_pic']
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.profile_pic = app.config['UPLOAD_FOLDER'] + filename
        db.session.commit()
        return redirect(url_for('viewprofile'))
    return render_template('editprofile.html', user=user)
@app.route('/sign_out', methods=["GET", "POST"])

def sign_out():
    session.clear()  # Clear the session data
    flash('You have been logged out.', 'success')  # Optional: Display a logout message
    return redirect('/')

# @app.route('/search_friend', methods=["GET", "POST"])
# def search_friend():
#     user = User.query.all()
#     s_id = session['s_id']
#     if request.method == 'POST':

#         for u in user:
#             print("username",u.username)
#             if u.username==request.form['search_friend']:
#                 if u.user_id != s_id:
#                 # print("user_iddddddd",s_id)
#                 # print("friend_iddddddd",u.user_id)
#                     user=Pending(friend_id=u.user_id,user_id = s_id)
#                     db.session.add(user)
#                     db.session.commit()
#                 else:
#                     return "You cannot send request to your self!"
#             # else:
#             #     return "user not found"
            
#         return redirect(url_for('home'))
#     else:
#         return redirect(url_for('home'))
    
@app.route('/search_friend', methods=["GET", "POST"])
@login_required
def search_friend():
    user = User.query.all()
    s_id = session['s_id']
    
    if request.method == 'POST':
        for u in user:
            uid =u.user_id
            print("username", u.username)
            if u.username == request.form['search_friend']:
                if u.user_id != s_id:
                    # Create a new pending request
                    pending_request = Pending(friend_id=u.user_id, user_id=s_id)
                    db.session.add(pending_request)
                    db.session.commit()
                    return redirect(url_for('send_req'))
                else:
                    return "You cannot send a request to yourself!"
        # User not found
        return "User not found"
  
    # Handle GET request method if needed
    return "This page is accessible via a form submission only."
    
@app.route('/pending_list')
@login_required
def pending_list():
   logged_user=session.get('s_id')
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

   if requested_person:
        print("!!!!!!!!!!!!!!!!!!!!!")
        return render_template('pending_list1.html',pending_users=p_list,requested_person=requested_person)
   else:
       flash("no pending list")
       return render_template('home.html')

@app.route('/accept_req/<id>', methods=["GET","POST"])
@login_required
def accept_req(id):
    logged_user=session.get('s_id') 
    if logged_user:
        user=Accept(friend_id=id,user_id=logged_user)
        user1 = Accept(user_id=id, friend_id=logged_user)

        db.session.add(user)   
        db.session.add(user1)

        db.session.commit()
    pendding = Pending.query.filter_by(user_id=id,friend_id=logged_user).delete()
    print("idididididididi",id) 
    print("pending....",pendding)
    if pendding:
        # db.session.delete(pendding)
        db.session.commit()
        return redirect(url_for('pending_list'))
    return "hello"



@app.route('/accept_list')
@login_required
def Acceptfriend_list():
   logged_user = session.get('s_id')
   a_list = Accept.query.filter_by(friend_id=logged_user)
   user_view = guests = db.session.query(User, User_profile).filter(User.user_id == User_profile.u_id).first()
   data = dict()
   data['profile_pic'] = user_view.User_profile.profile_pic

   requested_person = {}
   for p in a_list:
        uid = p.user_id
        uname = User.query.get(uid).username
       
        u_gender = User.query.get(uid).gender

        profile_pic = User_profile.query.get(uid).profile_pic
        # Retrieve the profile picture for the user
        user_bio = User_profile.query.get(uid).bio
        # Retrieve the profile picture for the user
        requested_person[uid] = {'username': uname, 'profile_pic': profile_pic,'bio':user_bio,'gender':u_gender}
        # print("~~~~~~~~~~~~~~~~~~~~~~",requested_person)

   return render_template('index.html', pending_users=a_list, requested_person=requested_person, user_view=data)


                

@app.route('/reject_req/<id>', methods=["GET","POST"])
@login_required
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
@login_required
def show_user():
    # # u_list =User.query.all()
    # for u in u_list:
    #     print("SMedia User..", u.username)
    # user_view1 = guests = db.session.query(User, User_profile).filter(
    #     User.user_id == User_profile.u_id).first()
    # print-("user----------------------",user_view1)
    logged_user = session.get('s_id')
    login = User.query.filter_by(user_id = logged_user)
    accept = Accept.query.filter_by(friend_id = logged_user)
    print("acerlkgmgngnfnfnfgf----------",accept)
    query = Accept.query.filter(
        db.or_(Accept.user_id == logged_user, Accept.friend == logged_user))
    # users = db.session.query(User, Accept).filter(User.user_id == Accept.user_id)
    users = User.query.all()

@app.route('/redirect/<id>')
def redirect_home():
    return redirect(url_for('dashobrd.html')) 

@app.route('/remove_friend/<id>')
@login_required
def remove_friend(id):
    logged_user=session.get('s_id') 
    remove_frd = Accept.query.filter_by(user_id=id,friend_id=logged_user).delete()
    remove_frd = Accept.query.filter_by(friend_id=id,user_id=logged_user).delete()

    if remove_frd:
        db.session.commit()
        return redirect(url_for('Acceptfriend_list'))
    return "hello"


@app.route('/non_friend', methods=["GET", "POST"])
@login_required
def non_friend():
    user = User.query.all()
    s_id = session['s_id']
    name=session.get('name')

    
    if request.method == 'POST':
        search_query = request.form['search_friend']
        non_friends = []

        for u in user:
            if search_query == name:
                return "You cannot send a request to yourself!"
            elif u.username != search_query and u.user_id != s_id:
                non_friends.append(u)

        if non_friends:
            return render_template('non_friends.html', non_friends=non_friends)
        else:
            return "No non-friend users found."

    return render_template('search_friend.html')

@app.route('/send_req', methods=["GET", "POST"])
def send_req():
    all_user = User.query.all() # want to ignore/remove objects from all_user which are in a_list = Accept.query.filter_by(friend_id=logged_user)
    logged_user = session['s_id']
    user = User.query.get(logged_user)
    # name=session.get('name')
    a_list = Accept.query.filter_by(friend_id=logged_user)
    p_list = Pending.query.filter_by(user_id=logged_user)
    for p in p_list:
     print("++++++++++++++++++++++++++++++",p.friend_id)

    all_user = User.query.all()
    a_list_ids = set(accept.user_id for accept in a_list)
    a_pending = set(pending.friend_id for pending in p_list)
    

    user_view = guests = db.session.query(User, User_profile).filter(User.user_id == User_profile.u_id).first()
    data = dict()
    filtered_users = []
    for user in all_user:
        if user.user_id not in a_list_ids and user.user_id not in a_pending and user.user_id!=logged_user:
            filtered_users.append(user)
            # print(user.user_id)
            uname=User.query.get(user.user_id).username
            # print(uname)
  
        
    requested_person = {}
    for p in filtered_users:
        uid = p.user_id
        uname = User.query.get(uid).username
        u_gender = User.query.get(uid).gender
        profile_pic = User_profile.query.get(uid).profile_pic
        # Retrieve the profile picture for the user
        user_bio = User_profile.query.get(uid).bio
        # Retrieve the profile picture for the user
        requested_person[uid] = {'username': uname, 'profile_pic': profile_pic,'bio':user_bio,'gender':u_gender}
        # print("~~~~~~~~~~~~~~~~~~~~~~",requested_person)
    return render_template('send_req.html',requested_person=requested_person)


@app.route('/sent_req/<id>', methods=["GET","POST"])
@login_required
def sent_req(id):  
    logged_user = session['s_id']
    try:
        pending_request = Pending(friend_id=id, user_id=logged_user)
        db.session.add(pending_request)
        db.session.commit()
        return redirect(url_for('send_req'))  
    except Exception as e:
        print(e)





with app.app_context():
    db.create_all()
if __name__ == "__main__":     
   app.run(debug=True) 
