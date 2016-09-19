from flask import Blueprint, render_template


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
@main_module.route('wifi-gps')
def wifi_gps():
    return render_template('wifi-gps.html')


@main_module.route('better-translator')
def better_translator():
    context = {
        'year': 2013,
        'authors': ['Sumin Byeon'],
        'link': 'http://better-translator.com',
    }
    return render_template('better-translator.html', **context)


@main_module.route('hanja')
def hanja():
    return render_template('hanja.html')
