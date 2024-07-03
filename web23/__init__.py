from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'daf8d5e8cDGEe=[]ddsoFDpDdDGsjg'


    # from .views import views
    from .LLMchangs import changs
 

    # app.register_blueprint(views, url_prefix='/admin')
    app.register_blueprint(changs, url_prefix='/')


    return app