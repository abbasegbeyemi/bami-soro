import os

from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from flask_socketio import SocketIO, emit

from forms import UserRegistrationForm, UserLoginForm
from models import User, Channel, Message
from models import db

# region App Initialization
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# When deploying, make sure to add the external db url to the application config
DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
# Here we initialise the database and crete all the required tables
db.init_app(app)
db.app = app
db.create_all()
# Initialise Migrate
migrate = Migrate(app, db)
# Initialise the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
# Initialise SocketIO
socketio = SocketIO(app)


@login_manager.user_loader
def user_loader(user_id):
    """
    Given a user id, return a user from the database that matches. The good
    thing about this model over using core is that the user returned contains
    all the related information.
    :param user_id: int
    :return: User object
    """
    return User.query.get(int(user_id))


# We want to be able to play with the app in the shell without too much palave


# endregion


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    """
    Take care of user registration by either sending them the form, or
    registering them and signing them in.
    :return:
    """
    form = UserRegistrationForm()
    if request.method == 'POST':
        if not form.validate():
            # If the form isn't properly validated, return a json saying why
            return jsonify(
                {
                    'success': False,
                    'errors': form.errors
                }
            )
        new_user = User(
            firstname=form.name.data,
            lastname=form.surname.data,
            email=form.email.data,
            username=form.username.data,
        )
        new_user.set_password(password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'), code=307)

    return render_template('register-form.html', form=form)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    """
    Get requests return a log in form
    Post requests authenticate the user, and redirects to the home page.
    :return:
    """
    form = UserLoginForm()
    if request.method == 'POST':
        # When the request is post, we want to send a JSON back
        if not form.validate():
            # If the form isn't properly validated, return a json saying why
            return jsonify(
                {
                    'success': False,
                    'errors': form.errors
                }
            )

        # We get here if form has been validated, login the user
        user = User.query.filter_by(username=form.username.data).first()
        remember = form.remember
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return jsonify(
            {
                'success': True,
                'nextpage': next_page
            }
        )

    return render_template('login-form.html', form=form)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('authenticate.html')

    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/api/channels')
@login_required
def channels():
    channel_list = Channel.query.all()
    channels_data = [{'creator': channel.creator.username, 'name': channel.name} for channel in channel_list]
    return jsonify(channels_data)


@app.route('/api/room_messages/<room_name>')
@login_required
def messages(room_name):
    channel_name = str.split(room_name, '-')[1]
    channel = Channel.query.filter_by(name=channel_name).first()
    previous_messages = Message.query.filter_by(channel=channel)
    data_returned = [
        {
            'author': message.author.username,
            'message': message.text,
        }
        for message in previous_messages]
    return jsonify(data_returned)


# For every socket IO transmission, we expect a JSON and we emit a JSON
@socketio.on('handle messages')
def handle_messages(data):
    room = data['channelName']
    channel_name = str.split(room, '-')[1]
    message = data['message']
    user = current_user
    channel = Channel.query.filter_by(name=channel_name).first()

    if channel:
        new_message = Message(author=user, channel=channel, text=message)
        db.session.add(new_message)
        db.session.commit()

    emit(room,
         {
             'author': user.username,
             'message': message,
         },
         broadcast=True)


@app.route('/api/create_channel', methods=['POST'])
@login_required
def create_channel():
    req = request.get_json()
    name = req['name']
    creator = current_user
    # Check if the creator has created a channel with that name before
    bad_name = str.strip(name.lower()) in [channel.name.lower() for channel in creator.channels]
    if bad_name:
        return jsonify(
            {
                'success': False,
                'error': 'Channel name already exisits for this user'
            }
        )

    new_channel = Channel(name=name, creator=creator)
    db.session.add(new_channel)
    db.session.commit()

    socketio.emit('new channel',
                  {
                      'name': name,
                      'creator': current_user.username
                  },
                  broadcast=True
                  )
    return jsonify(
        {
            'success': True,
        }
    )


@app.route('/register')
@app.route('/login')
def missroad():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
