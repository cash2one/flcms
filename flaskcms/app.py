import os
import os.path as op
from flask import Flask, render_template
from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
from flaskcms.extensions import db, migrate, mail
from flaskcms.user.models import User, Role
from flaskcms.post.models import Post, Tag
from flaskcms.works.models import Works, Image, Category
from flaskcms.admin import MyModelView
from flaskcms.user.admin import UserView
from flaskcms.works.admin import WorksView, ImageView
from flaskcms.post.admin import PostAdmin

import flask_admin

from flaskcms.views import main_bp
from flaskcms.works.views import works_bp
from flaskcms.post.views import post_bp


def create_app(config=None):
    # Create application
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    stc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    app = Flask("flapp", template_folder=tmpl_dir, static_folder=stc_dir)

    #app.config.from_object('config.DevelopConfig')
    app.config.from_object(config)

    configure_blueprints(app)
    configure_extensions(app)
    configure_admin(app)
    configure_errorhandlers(app)

    return app


def configure_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    mail.init_app(app)


def configure_admin(app):

    admin = flask_admin.Admin(
        app,
        'Example: SQLAlchemy',
        base_template='my_master.html',
        template_mode='bootstrap3',
    )

    # Add views
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(MyModelView(Tag, db.session))
    admin.add_view(MyModelView(Category, db.session))
    admin.add_view(WorksView(Works, db.session))
    admin.add_view(PostAdmin(db.session))
    admin.add_view(ImageView(Image, db.session))

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
        )


def configure_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(works_bp)
    app.register_blueprint(post_bp)


def configure_errorhandlers(app):
    """Configures the error handlers."""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("404.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("404.html"), 500

'''
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, 'sample_db.sqlite')

    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    manager.run()
'''