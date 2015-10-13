from wtforms import Form, validators, StringField, TextAreaField


class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    message = TextAreaField('Message')