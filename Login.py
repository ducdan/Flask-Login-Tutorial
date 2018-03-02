from flask import Flask,render_template,request,redirect,json
from flask.ext.login import UserMixin,LoginManager,login_user,current_user,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String
from hashlib import md5

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

app.secret_key='thisissecretkey'

db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_name=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

    def __init__(self,username,password):
        self.user_name=username
        self.setPassword(password)

    def setPassword(self,password):
        self.password=md5(password.encode()).hexdigest()

@login_manager.user_loader
def load_user(user_name):
    return User.query.get(user_name)


@app.route('/login',methods=['GET','POST'])
def login():
    message = ''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(user_name=username, password = md5(password.encode()).hexdigest()).first()
        if user:
            login_user(user=user)
        else:
            message = 'wrong username or password'
    # if(current_user.is_authenticated):
    #     return redirect('/home')
    # return render_template('login.html')

    if(current_user.is_authenticated):
        return redirect('/home')
    return render_template('index.html',message =message)

@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    db.session.add(User(username,password))
    db.session.commit()
    return redirect('/login')

@app.route('/home')
@login_required
def home():
    return "This is homepage"

@app.route('/info')
@login_required
def info():
    return "My Info"

@app.route('/')
def hello_world():
    db.create_all()
    return redirect('/login')

@app.route('/logout')
def logout():
    logout_user()
    return "Logout!"


@app.route('/query/<username>')
def query(username):
    user = User.query.filter_by(user_name=username).first()
    return json.dumps({'username':user.user_name,'password':user.password})
if __name__ == '__main__':
    app.run(debug=True)
