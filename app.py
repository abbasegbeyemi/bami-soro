import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

# region App Initialization
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# login_manager = LoginManager()
# login_manager.init_app(app)

# endregion

# region Debugging
toolbar = DebugToolbarExtension(app)


# endregion

# region Database Initialization
# DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
# engine = create_engine(DATABASE_URL, echo=False)


# endregion

@app.route('/')
def hello_world():
    return render_template('login-page.html')


@app.route('/<name>')
def hello_name(name):
    return f"hello {name}!"


if __name__ == '__main__':
    app.run()
    print(os.environ['APP_SETTINGS'])
