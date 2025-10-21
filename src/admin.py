import os
from flask_admin import Admin
from models import db, User, Planet, Character, Vehicle, Favorite, Comment
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    # hide password from list view and forms
    column_exclude_list = ['password']
    form_excluded_columns = ['favorites', 'created_at']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here. Example: add the User model with a small customization
    admin.add_view(UserAdmin(User, db.session))

    # Register other models (duplicate/add as needed)
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(Favorite, db.session))
    admin.add_view(ModelView(Comment, db.session))
