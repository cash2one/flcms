# -*- coding: utf-8 -*-
import os.path as op
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_admin import Admin


#database
db = SQLAlchemy()


#migrate
migrate = Migrate()


file_path = op.join(op.dirname(__file__), 'static')


init_admin = Admin()


