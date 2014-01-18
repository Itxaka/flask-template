from flask_peewee.admin import Admin, ModelAdmin
from app import app
from auth import auth
from models import User


class UserView(ModelAdmin):
    columns = ('username', 'email',)

admin = Admin(app, auth)
auth.register_admin(admin)
admin.register(User, UserView)
admin.setup()