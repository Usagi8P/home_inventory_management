from flask import Flask, request, render_template, redirect
import os
# from dotenv import load_dotenv

def create_app(test_config=None):
    # load_dotenv()
    app = Flask(__name__, instance_relative_config=True,
                static_folder='static',
                template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY = os.getenv('SECRET_KEY','dev'),
        ENV = os.getenv('ENV','dev'),
        DATABASE = os.path.join(app.instance_path,'home_inventory_db.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # This is needed later for building a front end.
    # if app.config['ENV'] == 'dev':
    #     CORS(app)

    from . import db
    db.init_app(app)

    @app.route('/')
    def root():
        return redirect('/inventory')
    
    from . import view_inventory
    app.register_blueprint(view_inventory.bp)

    from . import manage_inventory
    app.register_blueprint(manage_inventory.bp)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    return app