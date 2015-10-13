import os
import os.path as op
from flaskcms.extensions import db, file_path
from sqlalchemy.event import listens_for
from flask_admin import form


work_category = db.Table('work_category',
    db.Column('works_id', db.Integer, db.ForeignKey('works.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), nullable=False)
    path = db.Column(db.Unicode(128), nullable=False, unique=True)

    def __unicode__(self):
        return self.name


class Works(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    path = db.Column(db.Unicode(128), nullable=False, unique=True)

    #category = db.relationship('Category', secondary=work_category)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('work', lazy='dynamic'))

    def __unicode__(self):
        return self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(120), nullable=False, unique=True)

    def __unicode__(self):
        return self.name

    def getcode(self):
        return self.code



@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass


