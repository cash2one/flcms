#!/usr/bin/env python

"""
    flascms.manage


"""

from flaskcms import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from flaskcms.config import DevelopConfig


app = create_app(DevelopConfig)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
