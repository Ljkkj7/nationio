from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance
import flask
import os

secret_key = os.urandom(16).hex()

app = flask.Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/game')
def game():
    data = flask.session.get('game_instance')
    if not data:
        return flask.redirect(flask.url_for('game'))

    game_instance = GameInstance.from_dict(data)
    return flask.render_template('game.html', game_instance=game_instance)

@app.route('/game/next-hint', methods=['POST'])
def next_hint():
    data = flask.session.get('game_instance')
    if not data:
        return flask.redirect(flask.url_for('game'))

    game_instance = GameInstance.from_dict(data)
    game_instance.show_next_hint()

    flask.session['game_instance'] = game_instance.to_dict()
    return flask.redirect(flask.url_for('game'))

@app.route('/game/guess', methods=['POST'])
def guess():
    data = flask.session.get('game_instance')
    if not data:
        return flask.redirect(flask.url_for('game'))

    game_instance = GameInstance.from_dict(data)
    guess = flask.request.form['guess']
    game_instance.guess(guess)
    flask.session['game_instance'] = game_instance.to_dict()
    return flask.redirect(flask.url_for('game'))

@app.route('/game/new')
def new_game():
    game_instance = GameInstance()
    game_instance.init_new_round()
    game_instance.start()
    flask.session['game_instance'] = game_instance.to_dict()
    return flask.redirect(flask.url_for('game'))


if __name__ == '__main__':
    app.run(debug=True)

