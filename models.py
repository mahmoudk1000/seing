from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
 
login = LoginManager()
db = SQLAlchemy()
 
class User(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(80), unique=True)
    username = db.Column('username', db.String(100))
    password_hash = db.Column('password_hash', db.String())

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash
 
    def set_password(self, password):
         self.password_hash = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))