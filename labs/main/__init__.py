from flask import Blueprint, render_template

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


#
# Project pages (single-page ones)
#
@main_module.route('s/<module_name>')
def better_translator(module_name):
    document = Document.load(module_name)
    return render_template('single.html', **document.dump())


@main_module.route('wifi-gps')
def wifi_gps():
    return render_template('wifi-gps.html')


@main_module.route('hanja')
def hanja():
    return render_template('hanja.html')
