import os

from flask import Flask


__version__ = '2.0.0'


def create_app(name=__name__):
    app = Flask(name)

    from labs.main import main_module

    app.register_blueprint(main_module, url_prefix='/')

    return app


app = create_app()


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8029))
    debug = bool(os.environ.get('DEBUG', False))
    app.run(host=host, port=port, debug=debug)
