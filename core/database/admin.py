from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect, render_template, flash, request
from flask_admin.menu import MenuLink

from core.database.models import User, Token

from .connection import session

import flask_login as adminLogin
login_manager = adminLogin.LoginManager()


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return adminLogin.current_user.is_authenticated    
    
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not adminLogin.current_user.is_authenticated:
            return redirect(url_for('admin.login'))
        return super(MyAdminIndexView,self).index()
        
    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        if request.method == 'GET':
            return render_template("login.html")
        else:
            user_obj = session.query(User).filter_by(email=request.form['email']).first()
            
            exists = user_obj is not None and user_obj.verify_password(request.form['password'])
            if exists:
                adminLogin.login_user(user_obj)
                return redirect(url_for('admin.index'))
            else:
                flash('Invalid Credentials!', 'danger')
            return redirect(url_for('admin.index'))
        
    @expose('/logout')
    @adminLogin.login_required
    def logout(self):
        adminLogin.logout_user()
        return redirect(url_for('admin.login'))   

def admin_panel(app):
    # admin = Admin(app, name='APIS', template_mode='bootstrap3', endpoint="admin")
    admin = Admin(app, name='APIS', template_mode='bootstrap3', index_view=MyAdminIndexView())
    
    admin.add_view(ModelView(User, session))
    admin.add_view(ModelView(Token, session))
    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/admin/logout"))