from flask import abort, request, redirect, url_for
from flask_admin.contrib import sqla
from flask_security import current_user
from flaskcms.user.models import User
from flaskcms.post.models import Post, Tag
from flaskcms.works.models import Image
from wtforms import validators
from flask_admin.contrib.sqla import filters


# Customized Post model admin
class PostAdmin(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    # Visible columns in the list view
    column_exclude_list = ['text', 'user', 'image']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    column_sortable_list = ('title', 'date')

    # Rename 'title' columns to 'Post Title' in list view
    column_labels = dict(title='Post Title')

    column_searchable_list = ('title', User.email)

    column_filters = ('title',
                      'date',
                      filters.FilterLike(Post.title, 'Fixed Title', options=(('test1', 'Test 1'), ('test2', 'Test 2'))))

    # Pass arguments to WTForms. In this case, change label for text field to
    # be 'Big Text' and add required() validator.
    form_args = dict(
        text=dict(label='Big Text', validators=[validators.required()]),
        title=dict(label='Post title', validators=[validators.required()])
    )

    form_ajax_refs = {
        'user': {
            'fields': (User.first_name, User.email)
        },
        'tags': {
            'fields': (Tag.name,)
        },
        'image': {
            'fields': (Image.name,)
        }
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(PostAdmin, self).__init__(Post, session)

