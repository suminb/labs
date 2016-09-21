from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from labs.models import Document


main_module = Blueprint('main', __name__, template_folder='templates')


@main_module.route('/')
def index():
    context = {}
    return render_template('index.html', **context)


@main_module.route('discontinued')
def discontinued():
    context = {}
    return render_template('discontinued.html', **context)


@main_module.route('s/<module_name>')
def better_translator(module_name):
    try:
        document = Document.load(module_name)
    except FileNotFoundError:
        raise NotFound(
            'The requested page \'{}\' is not found'.format(module_name))

    return render_template('single.html', **document.dump())
