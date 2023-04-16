from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import request, url_for, redirect

from core.database.models import User, Token

from .connection import session

import flask_login as login
login_manager = login.LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            # flash('Please log in first...', 'error')
            print('ksjksds')
            return redirect(url_for('auth.login'))
        # import pdb;pdb.set_trace()
        if login.current_user.is_authenticated == True:
            return super(MyAdminIndexView,self).index()
        else:
            return redirect(url_for("admin"))

def admin_panel(app):
    # admin = Admin(app, engine, base_url="/admin/"+settings.SECRET_KEY)
    admin = Admin(app, name='APIS', template_mode='bootstrap3', endpoint="admin", index_view=MyAdminIndexView())
    
    admin.add_view(ModelView(User, session))
    admin.add_view(ModelView(Token, session))