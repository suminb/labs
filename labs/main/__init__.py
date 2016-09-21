from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from labs.models import Document, DocumentStatus


main_module = Blueprint('main', __name__, template_folder='templates')


@main_module.route('/')
@main_module.route('current')
def current():
    context = {
        'documents': Document.load_all(DocumentStatus.current)
    }
    return render_template('current.html', **context)


@main_module.route('discontinued')
def discontinued():
    context = {
        'documents': Document.load_all(DocumentStatus.discontinued)
    }
    return render_template('discontinued.html', **context)


@main_module.route('s/<page_name>')
def single_page(page_name):
    try:
        document = Document.load(page_name)
    except FileNotFoundError:
        raise NotFound(
            'The requested page \'{}\' is not found'.format(page_name))

    return render_template('single.html', **document.dump())
