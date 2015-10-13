from flask import Blueprint, render_template
from flaskcms.post.models import Post

post_bp = Blueprint('post_bp', __name__)


@post_bp.route('/blog/')
def blog_page():
    posts = Post.query.all()
    return render_template("blog.html", posts=posts)


@post_bp.route('/blog/<id>-<slug>/')
def post_page(id, slug=None):
    post = Post.query.filter_by(id=id).first_or_404()
    return render_template("post.html", post=post)