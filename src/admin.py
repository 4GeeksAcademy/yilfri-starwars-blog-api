import os
from flask_admin import Admin
from models import db, User, Character, Planet, Favorite_Planet, Favorite_Character
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class Favorite_CharacterAdmin(ModelView):
        column_list = ('id', 'user', 'character')
        form_columns = ('user', 'character')

    class Favorite_PlanetAdmin(ModelView):
        column_list = ('id', 'user', 'planet')
        form_columns = ('user', 'planet')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    # admin.add_view(ModelView(Favorite_Character, db.session))
    admin.add_view(Favorite_CharacterAdmin(Favorite_Character, db.session))
    admin.add_view(Favorite_PlanetAdmin(Favorite_Planet, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
