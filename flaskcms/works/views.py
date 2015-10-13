from flask import Blueprint, render_template
from flaskcms.works.models import Works

works_bp = Blueprint('works_bp', __name__)


@works_bp.route('/works/')
def works_page():
    data = Works.query.all()
    category = {}
    works = []

    for item in data:
        d = {
            'name': item.name,
            'path': item.path,
            'type': item.category.getcode()
        }
        category[item.category.getcode()] = item.category
        works.append(d)

    return render_template("works.html", works=works, category=category)

