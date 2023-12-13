from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

from app import app
import models

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return User(email=email)

class User(UserMixin):
    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email

    def info(self): #### THIS ALLOWS CURRENT USER DETAILS TO BE DISPLAYED ON SIDE BAR 
        user_info = models.read_appUser(self.email)
        return user_info
        
def userLogin(email):
    user = User(email=email)
    login_user(user)

def userLogout():
    logout_user()