from flask import Blueprint, render_template, request
from flaskcms.forms import ContactForm
from flask.ext.mail import Mail, Message
from flaskcms.extensions import mail


main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder='static', static_url_path='/static')


@main_bp.route('/')
def homepage():
    return render_template("index.html")


@main_bp.route('/contact/', methods=['GET', 'POST'])
def contactpage():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        msg = Message("New email from contact form", sender='contact@example.com', recipients=['romasport88@gmail.com'])
        msg.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
    return render_template('contact.html', form=form)


@main_bp.route('/about/')
def aboutpage():
    return render_template("about.html")

