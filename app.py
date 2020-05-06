import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

# region App Initialization
from sqlalchemy import create_engine

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(16)
# login_manager = LoginManager()
# login_manager.init_app(app)

# endregion

# region Debugging
toolbar = DebugToolbarExtension(app)
# endregion

# region Database Initialization
DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DATABASE_URL, echo=False)


# endregion


@app.route('/')
def hello_world():
    return render_template('login-page.html')


if __name__ == '__main__':
    app.run()
